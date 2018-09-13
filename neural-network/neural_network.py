import math
import random


class CachedNodeData:
    '''A simple cache for node-specific data used in evaluation and training
    for a single labeled example.

    For each field, the description of the field assumes the following:

    1. The node in question is a function f(w_1, w_2, ..., w_k, z_1, z_2, ..., z_m),
    where w_i are tunable parameters, and z_i are the inputs to the function
    being computed. For example, a linear node would have w_i be the weights, z_i
    be the inputs, k = m, with f defined as

        (z_1, ..., z_m) -> sum(w_i * z_i for i in range(m)).

    2. The global error function computed by the network is

        E(a_1, ..., a_M, x_1, ..., x_N, y),

    where the a_i are the collection of tunable parameters of all the nodes in the
    network, and the x_i are the inputs to the graph, and y is the expected label.

    3. A specific labeled example ((x_1, ..., x_N), y) to the entire graph is
    fixed, along with the current set of all tunable parameters. All derivatives
    are evaluated at these values.

    The values stored in the cache are:

    - output: the output of this node for the specific input
    - local_gradient: [∂f/∂z_1, ∂f/∂z_2, ..., ∂f/∂z_m]
    - global_gradient: ∂E/∂f
    - local_parameter_gradient: [∂f/∂w_1, ∂f/∂w_2, ..., ∂f/∂w_k]
    - global_parameter_gradient: [∂E/∂w_1, ∂E/∂w_2, ..., ∂E/∂w_k]
    '''

    def __init__(self):
        self.output = None
        self.local_gradient = None
        self.global_gradient = None
        self.local_parameter_gradient = None
        self.global_parameter_gradient = None

    def __repr__(self):
        return "{}".format(vars(self))


class Node:
    '''A node of a computation graph.

    Attributes

    arguments: a list of inputs to the Node, which are other Nodes whose
    outputs are inputs to the computation performed by this Node.

    successors: a list of Nodes that contain this node as input. Used for
    a Node to compute its error as a function of the errors of the Nodes that
    contain this Node as an argument.

    parameters: A list containing the tunable parameters of this node.

    has_parameters: A bool that is True if and only if there is a parameters
    list set.

    cache: values that are stored during evaluation and training to avoid
    recomputing intermediate values in the network.

    Children of this class implement

    compute_output: [float] -> float
    compute_local_gradient: None -> [float]
    compute_local_parameter_gradient: None -> [float]
    compute_global_parameter_gradient: None -> [float]

    The output of compute_*_parameter_gradient should correspond to the values
    of self.parameters index by index. The output of compute_local gradient should
    correspond to the input vector, index by index.

    If the Node is a terminal node (one that computes error for a training example)
    it must also have the following method

    compute_error: [float], int -> float
    '''

    def __init__(self, *arguments):
        self.has_parameters = False  # if this is True, child class must set self.parameters
        self.parameters = []
        self.arguments = arguments
        self.successors = []
        self.cache = CachedNodeData()

        # link argument successors to self
        for argument in self.arguments:
            argument.successors.append(self)

        '''Argument nodes z_i will query this node f(z_1, ..., z_k) for ∂f/∂z_i, so we need to keep
        track of the index for each argument node.'''
        self.argument_to_index = {node: index for (
            index, node) in enumerate(arguments)}

    def do_gradient_descent_step(self, step_size):
        '''The core gradient step subroutine: compute the gradient for each of this node's
        tunable parameters, step away from the gradient.'''
        if self.has_parameters:
            for i, gradient_entry in enumerate(self.global_parameter_gradient):
                # step away from the gradient
                self.parameters[i] -= step_size * gradient_entry

    '''Gradient computations which don't depend on the node's definition.'''

    def compute_global_gradient(self):
        '''Compute the derivative of the entire network with respect to this node.

        This method must be overridden for any output nodes that are terminal during
        training, such as an error node.
        '''
        return sum(
            successor.global_gradient *
            successor.local_gradient_for_argument(self)
            for successor in self.successors
        )

    def local_gradient_for_argument(self, argument):
        '''Return the derivative of this node with respect to a particular argument.'''
        argument_index = self.argument_to_index[argument]
        return self.local_gradient[argument_index]

    '''Cache lookups, computing on cache miss.'''

    def evaluate(self, inputs):
        if self.cache.output is None:
            self.cache.output = self.compute_output(inputs)
        return self.cache.output

    @property
    def output(self):
        if self.cache.output is None:
            raise Exception("Tried to query output not present in cache.")
        return self.cache.output

    @property
    def local_gradient(self):
        if self.cache.local_gradient is None:
            self.cache.local_gradient = self.compute_local_gradient()
        return self.cache.local_gradient

    @property
    def global_gradient(self):
        if self.cache.global_gradient is None:
            self.cache.global_gradient = self.compute_global_gradient()
        return self.cache.global_gradient

    @property
    def local_parameter_gradient(self):
        if self.cache.local_parameter_gradient is None:
            self.cache.local_parameter_gradient = self.compute_local_parameter_gradient()
        return self.cache.local_parameter_gradient

    @property
    def global_parameter_gradient(self):
        if self.cache.global_parameter_gradient is None:
            self.cache.global_parameter_gradient = self.compute_global_parameter_gradient()
        return self.cache.global_parameter_gradient

    def compute_output(self):
        raise NotImplementedError()

    def compute_local_parameter_gradient(self):
        raise NotImplementedError()

    def compute_local_gradient(self):
        raise NotImplementedError()

    def compute_global_parameter_gradient(self):
        raise NotImplementedError()


class InputNode(Node):
    def __init__(self, input_index):
        super().__init__()
        self.input_index = input_index

    def compute_output(self, inputs):
        return inputs[self.input_index]

    @staticmethod
    def make_input_nodes(count):
        '''A helper function so the user doesn't have to keep track of
           the input indexes.
        '''
        return [InputNode(i) for i in range(count)]

    def pretty_print(self, tabs=0):
        prefix = "  " * tabs
        return "{}InputNode({}) output = {}".format(
            prefix, self.input_index, self.output)


class ReluNode(Node):
    '''A node for a rectified linear unit (ReLU), i.e. the one-input,
    one-output function relu(x) = max(0, x).
    '''

    def compute_output(self, inputs):
        argument_value = self.arguments[0].evaluate(inputs)
        return max(0, argument_value)

    def compute_local_gradient(self):
        last_input = self.arguments[0].output
        return [1 if last_input > 0 else 0]

    def compute_local_parameter_gradient(self):
        return []  # No tunable parameters

    def compute_global_parameter_gradient(self):
        return []  # No tunable parameters

    def pretty_print(self, tabs=0):
        prefix = "  " * tabs
        return "{}Relu output={:.2f}\n{}\n".format(
            prefix,
            self.output,
            self.arguments[0].pretty_print(tabs + 1))


class SigmoidNode(Node):
    '''A node for a classical sigmoid unit, i.e. the one-input,
    one-output function s(x) = max(0, x).
    '''

    def compute_output(self, inputs):
        argument_value = self.arguments[0].evaluate(inputs)
        exp_value = math.exp(argument_value)
        return exp_value / (exp_value + 1)

    def compute_local_gradient(self):
        last_output = self.output
        return [(1 - last_output) * last_output]

    def compute_local_parameter_gradient(self):
        return []  # No tunable parameters

    def compute_global_parameter_gradient(self):
        return []  # No tunable parameters

    def pretty_print(self, tabs=0):
        prefix = "  " * tabs
        return "{}Sigmoid output={:.2f}\n{}\n".format(
            prefix,
            self.output,
            self.arguments[0].pretty_print(tabs + 1))


class ConstantNode(Node):
    '''A constant (untrainable) node, used as the input to the "bias" entry
       of a linear node.'''

    def compute_output(self, inputs):
        return 1

    def pretty_print(self, tabs=0):
        prefix = "  " * tabs
        return "{}Constant(1)".format(prefix)


class LinearNode(Node):
    '''A node for a linear node, i.e., the function with n inputs and n weights that
       computes sum(w * x for (w, x) in zip(weights, inputs)).'''

    def __init__(self, arguments, initial_weights=None):
        '''If the initial_weights are provided, they must be one longer
        than the number of arguments, and the first entry must correspond
        to the bias.
        '''
        super().__init__(ConstantNode(), *arguments)
        self.initialize_weights(initial_weights)
        self.has_parameters = True
        self.parameters = self.weights  # name alias

    def initialize_weights(self, initial_weights):
        arglen = len(self.arguments)
        if initial_weights:
            if len(initial_weights) != arglen:
                raise Exception(
                    "Invalid initial_weights length {:d}".format(len(initial_weights)))
            self.weights = initial_weights
        else:
            # set the initial weights randomly, according to a heuristic distribution
            weight_bound = 1.0 / math.sqrt(arglen)
            self.weights = [
                random.uniform(-weight_bound, weight_bound) for _ in range(arglen)]

    def compute_output(self, inputs):
        return sum(
            w * x.evaluate(inputs)
            for (w, x) in zip(self.weights, self.arguments)
        )

    def compute_local_gradient(self):
        return self.weights

    def compute_local_parameter_gradient(self):
        return [arg.output for arg in self.arguments]

    def compute_global_parameter_gradient(self):
        return [
            self.global_gradient *
            self.local_parameter_gradient_for_argument(argument)
            for argument in self.arguments
        ]

    def local_parameter_gradient_for_argument(self, argument):
        '''Return the derivative of this node with respect to the weight
        associated with a particular argument.'''
        argument_index = self.argument_to_index[argument]
        return self.local_parameter_gradient[argument_index]

    def pretty_print(self, tabs=0):
        argument_strs = '\n'.join(arg.pretty_print(tabs + 1)
                                  for arg in self.arguments)
        prefix = "  " * tabs
        weights = ','.join(['%.2f' % w for w in self.weights])
        gradient = ','.join(
            ['%.2f' % w for w in self.global_parameter_gradient])
        return "{}Linear weights={} gradient={} output={:.2f}\n{}\n".format(
            prefix, weights, gradient, self.output, argument_strs)


class L2ErrorNode(Node):
    '''A node computing the squared deviation error function.

    The function is f(z(x), y) = (z(x) - y)^2, where (x, y) is a labeled
    example and z(x) is the rest of the computation graph.
    '''

    def compute_error(self, inputs, label):
        argument_value = self.arguments[0].evaluate(inputs)
        self.label = label  # cache the label
        return (argument_value - label) ** 2

    def compute_local_gradient(self):
        last_input = self.arguments[0].output
        return [2 * (last_input - self.label)]

    def compute_global_gradient(self):
        return 1


class NeuralNetwork:
    def __init__(self, terminal_node, input_nodes, error_node=None, step_size=None):
        self.terminal_node = terminal_node
        self.input_nodes = input_nodes
        self.error_node = error_node or L2ErrorNode(self.terminal_node)
        self.step_size = step_size or 1e-2
        self.reset()

    def for_each(self, func):
        '''Walk the graph and apply func to each node.'''
        nodes_to_process = set([self.error_node])
        processed = set()

        while nodes_to_process:
            node = nodes_to_process.pop()
            func(node)
            processed.add(node)
            nodes_to_process |= set(node.arguments) - processed

    def reset(self):
        def reset_one(node):
            node.cache = CachedNodeData()
        self.for_each(reset_one)

    def evaluate(self, inputs):
        self.reset()
        return self.terminal_node.evaluate(inputs)

    def compute_error(self, inputs, label):
        '''Compute the error for a given labeled example.'''
        self.reset()
        return self.error_node.compute_error(inputs, label)

    def backpropagation_step(self, inputs, label, step_size=None):
        self.compute_error(inputs, label)
        self.for_each(lambda node: node.do_gradient_descent_step(step_size))

    def train(self, dataset, max_steps=10000, callback=None):
        '''dataset is a list of pairs ([float], int) where the first entry is
        the data point and the second is the label.
        '''
        for i in range(max_steps):
            inputs, label = random.choice(dataset)
            self.backpropagation_step(inputs, label, self.step_size)

            if callback and i % 100 == 0:
                callback(self, dataset)
            elif i % int(max_steps / 10) == 0:
                print('{:2.1f}%'.format(100 * i / max_steps))

    def train_while_watching(self, dataset, max_steps):
        def callback(network, dataset):
            print()
            for (inputs, label) in dataset:
                print("network({}) = {} (should be {})".format(
                    inputs, network.evaluate(inputs), label))
            print(network.pretty_print())
            ans = input('Continue? [Y/n] ')
            if ans and ans[0].lower() == 'n':
                raise Exception("Stopping early.")

        self.train(dataset, max_steps, callback)

    def error_on_dataset(self, dataset):
        errors = 0
        total = len(dataset)

        for (example, label) in dataset:
            if round(self.evaluate(example)) != label:
                errors += 1

        return errors / total

    def pretty_print(self):
        return self.terminal_node.pretty_print()
