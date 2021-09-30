from neural_network import InputNode
from neural_network import L2ErrorNode
from neural_network import LinearNode
from neural_network import NeuralNetwork
from neural_network import ReluNode
from neural_network import SigmoidNode
from random import shuffle
import os


def load_1s_and_7s(filename):
    print('Loading data {}...'.format(filename))
    examples = []
    with open(filename, 'r') as infile:
        for line in infile:
            if line[0] in ['1', '7']:
                tokens = [int(x) for x in line.split(',')]
                label = tokens[0]
                example = [x / 255 for x in tokens[1:]]  # scale to [0,1]
                if label == 1:
                    examples.append([example, 0])
                elif label == 7:
                    examples.append([example, 1])
    print('Data loaded.')
    return examples


def print_example(example):
    for i, pixel in enumerate(example):
        if i % 28 == 0:
            print()
        print('%4d' % int(pixel * 255), end='')


def show_random_examples(network, test, n=5):
    test = test[:]
    shuffle(test)
    for i in range(n):
        example, label = test[i]
        print_example(example)
        print("\nExample with label {} is predicted to have label {}".format(
            label, network.evaluate(example)))


def build_network():
    input_nodes = InputNode.make_input_nodes(28*28)

    first_layer = [LinearNode(input_nodes) for i in range(10)]
    first_layer_relu = [ReluNode(L) for L in first_layer]

    second_layer = [LinearNode(first_layer_relu) for i in range(10)]
    second_layer_relu = [ReluNode(L) for L in second_layer]

    linear_output = LinearNode(second_layer_relu)
    output = SigmoidNode(linear_output)
    error_node = L2ErrorNode(output)
    network = NeuralNetwork(
        output, input_nodes, error_node=error_node, step_size=0.05)

    return network


cant_find_files = '''
Was unable to find the files {}, {}.

You may have to extract them from the gzipped tarball mnist/mnist.tar.gz.
'''


def train_mnist(data_dirname, num_epochs=5):
    train_file = os.path.join(data_dirname, 'mnist_train.csv')
    test_file = os.path.join(data_dirname, 'mnist_test.csv')
    try:
        train = load_1s_and_7s(train_file)
        test = load_1s_and_7s(test_file)
    except Exception:  # pragma: no cover
        print(cant_find_files.format(train_file, test_file))
        raise

    network = build_network()
    n = len(train)
    epoch_size = int(n/10)

    for i in range(num_epochs):
        shuffle(train)
        validation = train[:epoch_size]
        real_train = train[epoch_size: 2*epoch_size]

        print("Starting epoch of {} examples with {} validation".format(
            len(real_train), len(validation)))

        network.train(real_train, max_steps=len(real_train))

        print("Finished epoch. Validation error={:.3f}".format(
            network.error_on_dataset(validation)))

    print("Test error={:.3f}".format(network.error_on_dataset(test)))
    show_random_examples(network, test)
    return network


if __name__ == "__main__":
    data_dirname = os.path.join(os.path.dirname(__file__), 'mnist')
    network = train_mnist(data_dirname)
