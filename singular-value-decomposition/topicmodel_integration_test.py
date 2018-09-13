from assertpy import assert_that

from topicmodel import cluster_stories
from topicmodel import load


def test_end_to_end():
    # assert that the end to end test runs without error
    word_clusters, document_clusters = cluster_stories(load())
