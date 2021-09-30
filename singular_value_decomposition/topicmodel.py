'''A simple topic model using singular value decomposition
applied to a corpus of CNN stories.
'''
import json
import numpy as np
from collections import Counter
from scipy.cluster.vq import kmeans2

# from numpy.linalg import svd
from svd import svd


def normalize(matrix):
    '''Normalize a document term matrix according to a local and
    global normalization factor.

    For this we chose a simple logarithmic local normalization
    with a global normalization based on entropy.
    '''
    num_words, num_docs = matrix.shape
    local_factors = np.log(np.ones(matrix.shape) + matrix.copy())

    probabilities = matrix.copy()
    row_sums = np.sum(matrix, axis=1)

    # divide each column by the row sums
    assert all(x > 0 for x in row_sums)
    probabilities = (probabilities.T / row_sums).T

    entropies = (probabilities * np.ma.log(probabilities).filled(0) /
                 np.log(num_docs))
    global_factors = np.ones(num_words) + np.sum(entropies, axis=1)

    # multiply each column by the global factors for the rows
    normalized_matrix = (local_factors.T * global_factors).T
    return normalized_matrix


def make_document_term_matrix(documents):
    '''Return the document-term matrix for the given list of stories.

    Arguments:
        documents: a list of dictionaries of the form

            {
                'words': [string]
                'text': string
            }

        The list of words include repetition.

    Returns:
        A document-term matrix. Entry [i, j] is the count of word i
        in story j.
    '''
    words = all_words(documents)
    word_to_index = dict((word, i) for i, word in enumerate(words))
    index_to_word = dict(enumerate(words))
    index_to_document = dict(enumerate(documents))

    matrix = np.zeros((len(words), len(documents)))
    for doc_id, document in enumerate(documents):
        doc_words = Counter(document['words'])
        for word, count in doc_words.items():
            matrix[word_to_index[word], doc_id] = count

    return matrix, (index_to_word, index_to_document)


def cluster(vectors):
    print(vectors)
    return kmeans2(vectors, k=len(vectors[0]))


def all_words(documents):
    '''Return a list of all unique words in the input list of documents.'''
    words = set()
    for entry in documents:
        words |= set(entry['words'])
    return list(sorted(words))


def load(filename='all_stories.json'):
    with open(filename, 'r') as infile:
        return json.loads(infile.read())


def cluster_stories(documents, k=10):
    '''Cluster a set of documents using a simple SVD-based topic model.

    Arguments:
        documents: a list of dictionaries of the form

            {
                'words': [string]
                'text': string
            }

        k: the number of singular values to compute.

    Returns:
        A pair of (word_clusters, document_clusters), where word_clusters
        is a clustering over the set of all words in all documents, and
        document_clustering is a clustering over the set of documents.
    '''
    matrix, (index_to_word, index_to_document) = make_document_term_matrix(
        documents)
    matrix = normalize(matrix)
    sigma, U, V = svd(matrix, k=k)

    projected_documents = np.dot(matrix.T, U)
    projected_words = np.dot(matrix, V.T)

    document_centers, document_clustering = cluster(projected_documents)
    word_centers, word_clustering = cluster(projected_words)

    word_clusters = tuple(
        tuple(index_to_word[i]
              for (i, x) in enumerate(word_clustering) if x == j)
        for j in range(len(set(word_clustering)))
    )

    document_clusters = tuple(
        tuple(index_to_document[i]['text']
              for (i, x) in enumerate(document_clustering) if x == j)
        for j in range(len(set(document_clustering)))
    )

    return word_clusters, document_clusters


if __name__ == "__main__":
    word_clusters, document_clusters = cluster_stories(load())
