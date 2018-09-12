from neural_network import InputNode
from neural_network import L2ErrorNode
from neural_network import LinearNode
from neural_network import NeuralNetwork
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


def test_input_output():
    node = InputNode(0)
    assert node.compute_output([3]) == 3
    assert node.compute_output([-4]) == -4


def test_relu_evaluate_negative():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    assert relu.evaluate([-2]) == 0


def test_relu_evaluate_positive():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    assert relu.evaluate([3]) == 3


def test_relu_local_gradient_positive():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    relu.evaluate([3])
    assert relu.local_gradient_for_argument(input_node) == 1


def test_relu_local_gradient_negative():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    relu.evaluate([-3])
    assert relu.local_gradient_for_argument(input_node) == 0


def test_relu_local_parameter_gradient_empty():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    relu.evaluate([3])
    assert len(relu.local_parameter_gradient) == 0


def test_linear_evaluate():
    input_nodes = InputNode.make_input_nodes(3)
    inputs = [1, 2, 3]
    initial_weights = [4, 3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    assert linear_node.evaluate(inputs) == 4*1 + 3*1 + 2*2 + 3*1


def test_linear_local_gradient():
    input_nodes = InputNode.make_input_nodes(3)
    initial_weights = [4, 3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    assert linear_node.local_gradient == [4, 3, 2, 1]


def test_linear_local_parameter_gradient():
    input_nodes = InputNode.make_input_nodes(3)
    inputs = [1, 2, 3]
    initial_weights = [4, 3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    linear_node.evaluate(inputs)
    assert linear_node.local_parameter_gradient == [1, 1, 2, 3]


def test_linear_with_relu_evaluate():
    input_nodes = InputNode.make_input_nodes(3)
    inputs = [1, 2, 3]
    initial_weights = [-20, 3, 2, 1]
    linear_node = LinearNode(input_nodes, initial_weights=initial_weights)
    relu_node = ReluNode(linear_node)
    assert relu_node.evaluate(inputs) == 0
    assert linear_node.output == -10


def test_neural_network_evaluate():
    network = single_linear_relu_network(3, [-20, 3, 2, 1])
    assert network.evaluate([1, 2, 3]) == 0


def test_neural_network_error():
    input_node = InputNode(0)
    relu = ReluNode(input_node)
    network = NeuralNetwork(relu, [input_node])

    inputs = [-2]
    label = 1
    assert network.evaluate(inputs) == 0
    assert network.compute_error(inputs, label) == 1


def test_neural_network_reset():
    network = single_linear_relu_network(2, [3, 2, 1])
    assert network.evaluate([2, -2]) == 5
    assert network.evaluate([6, -2]) != 5


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
    assert network.evaluate(example) == 5
    assert relu_node.output > 0
    assert network.compute_error(example, label) == 16

    # ∂E/∂E = 1, ∂E/∂f = 8
    assert error_node.global_gradient == 1
    assert error_node.local_gradient == [8]

    # ∂E/∂z = 8, ∂r/∂z = 1
    assert relu_node.global_gradient == 8
    assert relu_node.local_gradient == [1]
    assert relu_node.global_parameter_gradient == []
    assert relu_node.local_parameter_gradient == []

    # ∂E/∂l = 8, ∂l/∂x_i = [3, 2, 1]
    assert linear_node.global_gradient == 8
    assert linear_node.local_gradient == [3, 2, 1]

    # ∂l/∂w_i = [1, 2, -2], ∂E/∂w_i = [8, 16, -16]
    assert linear_node.local_parameter_gradient == [1, 2, -2]
    assert linear_node.global_parameter_gradient == [8, 16, -16]


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
    assert linear_node.weights == new_weights


'''
The remaining tests have some chance of failing due to the randomness in
their initialization. I have not fixed the seed in order to demonstrate
that the learning is heavily dependent on a lucky initial point.
'''


def test_learn_xor_sigmoid():
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
        assert abs(network.evaluate(example) - label) < 0.1


def test_learn_xor_relu():
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
