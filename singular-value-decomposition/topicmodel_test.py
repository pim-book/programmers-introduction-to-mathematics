from assertpy import assert_that

from topicmodel import all_words
from topicmodel import cluster_stories
from topicmodel import load
from topicmodel import make_document_term_matrix
from topicmodel import normalize


def test_end_to_end():
    # assert that the end to end test runs without error
    word_clusters, document_clusters = cluster_stories(load())
