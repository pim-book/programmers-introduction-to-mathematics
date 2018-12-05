from assertpy import assert_that
import pytest

from neural_network import CachedNodeData
from neural_network import ConstantNode
from neural_network import InputNode
from neural_network import L2ErrorNode
from neural_network import LinearNode
from neural_network import NeuralNetwork
from neural_network import Node
from neural_network import ReluNode
from neural_network import SigmoidNode


def single_linear_relu(input_nodes, initial_weights=None):
    return ReluNode(LinearNode(input_nodes, initial_weights=initial_weights))


def single_linear_relu_network(node_count, initial_weights):
    input_nodes = InputNode.make_input_nodes(node_count)
    relu_node = single_linear_relu(
        input_nodes, initial_weights=initial_weights)
    error_node = L2ErrorNode(relu_node)
    return NeuralNetwork(relu_node, input_nodes, error_node=error_node)


def test_node_missing_output():
    node = Node()
    with pytest.raises(Exception):
        node.output


def test_cache_repr():
    cache = CachedNodeData()
    cache.output = 1
    cache.local_gradient = 2
    cache.global_gradient = 3
    cache.local_parameter_gradient = 4
    cache.global_parameter_gradient = 5
    expect = (
        "CachedNodeData(output=1, "
        "local_gradient=2, "
        "global_gradient=3, "
        "local_parameter_gradient=4, "
        "global_parameter_gradient=5)"
    )
    assert_that(repr(cache)).is_equal_to(expect)
    cache = eval(repr(cache))
    assert_that(repr(cache)).is_equal_to(expect)

def test_linear_node_bad_initialization():
    input_nodes = InputNode.make_input_nodes(3)
    inputs = [1, 2, 3]
    initial_weights = [4, 3, 2, 1, 1]
    with pytest.raises(Exception):
        linear_node = LinearNode(
            input_nodes, initial_weights=initial_weights)


def test_sigmoid_node_empty_parameters():
    node = SigmoidNode()
    assert_that(node.compute_local_parameter_gradient()).is_empty()
    assert_that(node.compute_global_parameter_gradient()).is_empty()


def test_pretty_print():
    const = ConstantNode()
    input_node = InputNode(0)
    sigmoid = SigmoidNode(const)
    sigmoid.evaluate([])
    relu = ReluNode(input_node)
    relu.evaluate([2])

    assert_that(sigmoid.pretty_print()).is_equal_to(
        "Sigmoid output=0.73\n  Constant(1)\n")
    assert_that(relu.pretty_print()).is_equal_to(
        "Relu output=2.00\n  InputNode(0) output = 2.00\n")

    network = single_linear_relu_network(3, [-20, 3, 2, 1])
    network.evaluate([1, 2, 3])
    network.compute_error([1, 2, 3], 1)
    assert_that(network.pretty_print()).is_equal_to(
        """Relu output=0.00
  Linear weights=-20.00,3.00,2.00,1.00 gradient=0.00,0.00,0.00,0.00 output=-10.00
    Constant(1)
    InputNode(0) output = 1.00
    InputNode(1) output = 2.00
    InputNode(2) output = 3.00

""")


def test_input_output():
    node = InputNode(0)
    assert_that(node.compute_output([3])).is_equal_to(3)
    assert_that(node.compute_output([-4])).is_equal_to(-4)


def test_relu_evaluate_negative():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    assert_that(relu.evaluate([-2])).is_equal_to(0)


def test_relu_evaluate_positive():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    assert_that(relu.evaluate([3])).is_equal_to(3)


def test_relu_local_gradient_positive():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    relu.evaluate([3])
    assert_that(relu.local_gradient_for_argument(input_node)).is_equal_to(1)


def test_relu_local_gradient_negative():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    relu.evaluate([-3])
    assert_that(relu.local_gradient_for_argument(input_node)).is_equal_to(0)


def test_relu_local_parameter_gradient_empty():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    relu.evaluate([3])
    assert_that(len(relu.local_parameter_gradient)).is_equal_to(0)


def test_linear_evaluate():
    input_nodes = InputNode.make_input_nodes(3)
    inputs = [1, 2, 3]
    initial_weights = [4, 3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    assert_that(linear_node.evaluate(inputs)
                ).is_equal_to(4*1 + 3*1 + 2*2 + 3*1)


def test_linear_local_gradient():
    input_nodes = InputNode.make_input_nodes(3)
    initial_weights = [4, 3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    assert_that(linear_node.local_gradient).is_equal_to([4, 3, 2, 1])


def test_linear_local_parameter_gradient():
    input_nodes = InputNode.make_input_nodes(3)
    inputs = [1, 2, 3]
    initial_weights = [4, 3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    linear_node.evaluate(inputs)
    assert_that(linear_node.local_parameter_gradient).is_equal_to([1, 1, 2, 3])


def test_linear_with_relu_evaluate():
    input_nodes = InputNode.make_input_nodes(3)
    inputs = [1, 2, 3]
    initial_weights = [-20, 3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    relu_node = ReluNode(linear_node)
    assert_that(relu_node.evaluate(inputs)).is_equal_to(0)
    assert_that(linear_node.output).is_equal_to(-10)


def test_neural_network_evaluate():
    network = single_linear_relu_network(3, [-20, 3, 2, 1])
    assert_that(network.evaluate([1, 2, 3])).is_equal_to(0)


def test_neural_network_error():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    network = NeuralNetwork(relu, [input_node])

    inputs = [-2]
    label = 1
    assert_that(network.evaluate(inputs)).is_equal_to(0)
    assert_that(network.compute_error(inputs, label)).is_equal_to(1)


def test_neural_network_reset():
    network = single_linear_relu_network(2, [3, 2, 1])
    assert_that(network.evaluate([2, -2])).is_equal_to(5)
    assert network.evaluate([6, -2]) != 5


def test_neural_network_errors_on_dataset():
    network = single_linear_relu_network(2, [3, 2, 1])
    dataset = [((2, -2), 5), ((6, -2), 5)]
    assert_that(network.error_on_dataset(dataset)).is_close_to(0.5, 1e-9)


def test_neural_network_gradients():
    input_nodes = InputNode.make_input_nodes(2)
    initial_weights = [3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    relu_node = ReluNode(linear_node)
    error_node = L2ErrorNode(relu_node)
    network = NeuralNetwork(relu_node, input_nodes, error_node=error_node)

    example = [2, -2]
    label = 1

    '''
    l(w, x): linear node
    r(z): relu node
    f(w, x) = r(l(w, x))
    E(w, x, y): (r(l(w, x)) - y) ^ 2
    '''

    # f(w, x) = 5
    # E(w, x, y) = 16
    assert_that(network.evaluate(example)).is_equal_to(5)
    assert relu_node.output > 0
    assert_that(network.compute_error(example, label)).is_equal_to(16)

    # ∂E/∂E = 1, ∂E/∂f = 8
    assert_that(error_node.global_gradient).is_equal_to(1)
    assert_that(error_node.local_gradient).is_equal_to([8])

    # ∂E/∂z = 8, ∂r/∂z = 1
    assert_that(relu_node.global_gradient).is_equal_to(8)
    assert_that(relu_node.local_gradient).is_equal_to([1])
    assert_that(relu_node.global_parameter_gradient).is_equal_to([])
    assert_that(relu_node.local_parameter_gradient).is_equal_to([])

    # ∂E/∂l = 8, ∂l/∂x_i = [3, 2, 1]
    assert_that(linear_node.global_gradient).is_equal_to(8)
    assert_that(linear_node.local_gradient).is_equal_to([3, 2, 1])

    # ∂l/∂w_i = [1, 2, -2], ∂E/∂w_i = [8, 16, -16]
    assert_that(linear_node.local_parameter_gradient).is_equal_to([1, 2, -2])
    assert_that(linear_node.global_parameter_gradient).is_equal_to(
        [8, 16, -16])


def test_neural_network_backpropagation_step():
    input_nodes = InputNode.make_input_nodes(2)
    initial_weights = [3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    relu_node = ReluNode(linear_node)
    error_node = L2ErrorNode(relu_node)
    network = NeuralNetwork(relu_node, input_nodes, error_node=error_node)

    example = [2, -2]
    label = 1
    step_size = 0.5

    network.backpropagation_step(example, label, step_size=step_size)
    new_weights = [-1.0, -6.0, 9.0]

    # ∂E/∂w_i = [8, 16, -16], delta is [-4, -8, 8]
    assert_that(linear_node.weights).is_equal_to(new_weights)
