import os

from topicmodel import cluster_stories
from topicmodel import load

stories_file = os.path.join(os.path.dirname(__file__), "all_stories.json")


def test_end_to_end():
    # assert that the end to end test runs without error
    word_clusters, document_clusters = cluster_stories(load(stories_file))
