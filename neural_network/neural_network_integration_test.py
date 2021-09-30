from assertpy import assert_that
import random

from neural_network import InputNode
from neural_network import L2ErrorNode
from neural_network import LinearNode
from neural_network import NeuralNetwork
from neural_network import ReluNode
from neural_network import SigmoidNode

'''
These tests have some chance of failing due to the randomness in
their initialization. Remove the fixing of the random seed to observe
that they sometimes fail.
'''


def test_learn_xor_sigmoid():
    random.seed(1)
    input_nodes = InputNode.make_input_nodes(2)
    linear_node_1 = LinearNode(input_nodes)
    linear_node_2 = LinearNode(input_nodes)
    linear_node_3 = LinearNode(input_nodes)
    sigmoid_node_1 = SigmoidNode(linear_node_1)
    sigmoid_node_2 = SigmoidNode(linear_node_2)
    sigmoid_node_3 = SigmoidNode(linear_node_3)
    linear_output = LinearNode(
        [sigmoid_node_1, sigmoid_node_2, sigmoid_node_3])
    output = SigmoidNode(linear_output)
    error_node = L2ErrorNode(output)
    network = NeuralNetwork(
        output, input_nodes, error_node=error_node, step_size=0.5)

    examples = [[0, 0], [0, 1], [1, 0], [1, 1]]
    labels = [0, 1, 1, 0]
    dataset = list(zip(examples, labels))

    network.train(dataset, max_steps=10000)
    for (example, label) in dataset:
        assert_that(network.evaluate(example)).is_close_to(label, 0.1)

    assert_that(network.error_on_dataset(dataset)).is_equal_to(0.0)


def test_learn_xor_relu():
    random.seed(1)
    input_nodes = InputNode.make_input_nodes(2)

    first_layer = [LinearNode(input_nodes) for i in range(10)]
    first_layer_relu = [ReluNode(L) for L in first_layer]

    second_layer = [LinearNode(first_layer_relu) for i in range(10)]
    second_layer_relu = [ReluNode(L) for L in second_layer]

    linear_output = LinearNode(second_layer_relu)
    output = linear_output
    error_node = L2ErrorNode(output)
    network = NeuralNetwork(
        output, input_nodes, error_node=error_node, step_size=0.05)

    examples = [[0, 0], [0, 1], [1, 0], [1, 1]]
    labels = [0, 1, 1, 0]
    dataset = list(zip(examples, labels))

    network.train(dataset, max_steps=1000)
    for (example, label) in dataset:
        assert abs(network.evaluate(example) - label) < 0.1

    assert_that(network.error_on_dataset(dataset)).is_equal_to(0.0)
