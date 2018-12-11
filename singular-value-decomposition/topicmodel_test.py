from assertpy import assert_that
import numpy
import random

from topicmodel import all_words
from topicmodel import cluster_stories
from topicmodel import make_document_term_matrix

EPSILON = 1e-9


def test_all_words_empty():
    assert_that(all_words([])).is_equal_to([])


def test_all_words_single_doc():
    document = {
        'words': ['b', 'c', 'a']
    }
    assert_that(all_words([document])).is_equal_to(['a', 'b', 'c'])


def test_all_words_many_docs():
    doc1 = {
        'words': ['b', 'c', 'a']
    }
    doc2 = {
        'words': ['b', 'd', 'a']
    }
    doc3 = {
        'words': ['b', 'd', 'e']
    }
    assert_that(all_words([doc1, doc2, doc3])).is_equal_to(
        ['a', 'b', 'c', 'd', 'e'])


def test_make_document_term_matrix_empty():
    matrix, (index_to_word, index_to_document) = make_document_term_matrix([])
    assert_that(index_to_document).is_equal_to({})
    assert_that(index_to_word).is_equal_to({})
    assert_that(matrix).is_equal_to(numpy.zeros((0, 0)))


def test_make_document_term_matrix():
    doc1 = {
        'words': ['b', 'c', 'a']
    }
    doc2 = {
        'words': ['b', 'd', 'a']
    }
    doc3 = {
        'words': ['b', 'd', 'e']
    }
    matrix, (index_to_word, index_to_document) = make_document_term_matrix(
        [doc1, doc2, doc3])
    assert_that(index_to_document).is_equal_to(
        dict(enumerate([doc1, doc2, doc3])))
    assert_that(index_to_word).is_equal_to(dict(enumerate('abcde')))

    expected_matrix = numpy.array([
        [1, 1, 0],
        [1, 1, 1],
        [1, 0, 0],
        [0, 1, 1],
        [0, 0, 1],
    ])

    flattened_actual = matrix.flatten()
    flattened_expected = expected_matrix.flatten()
    for (a, b) in zip(flattened_actual, flattened_expected):
        assert_that(a).is_close_to(b, EPSILON)


def test_cluster_stories():
    random.seed(1)
    numpy.random.seed(1)
    doc1 = {
        'words': ['b', 'c', 'a', 'd', 'e', 'c'],
        'text': 'doc1',
    }
    doc2 = {
        'words': ['b', 'd', 'a', 'e', 'e', 'c'],
        'text': 'doc2',
    }
    doc3 = {
        'words': ['x', 'y', 'z', 'x', 'y', 'w'],
        'text': 'doc3',
    }
    doc4 = {
        'words': ['w', 'y', 'z', 'y', 'z'],
        'text': 'doc4',
    }
    doc5 = {
        'words': ['z', 'w', 'z', 'w', 'w'],
        'text': 'doc5',
    }
    doc6 = {
        'words': ['c', 'c', 'a', 'e', 'e'],
        'text': 'doc6',
    }

    word_clusters, document_clusters = cluster_stories([
        doc1, doc2, doc3, doc4, doc5, doc6], k=2)
    assert_that(set(word_clusters)).contains_only(
        ('a', 'b', 'c', 'd', 'e'),
        ('w', 'x', 'y', 'z'))
    assert_that(set(document_clusters)).contains_only(
        ('doc1', 'doc2', 'doc6'),
        ('doc3', 'doc4', 'doc5'))
