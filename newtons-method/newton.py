
def newton_sequence(f, f_derivative,  starting_x):
    """Perform Newton's method to find the root of a differentiable funciton.

    Arguments:
        f: a callable specifying the function whose root is sought.
        f_derivative: a callable providing the derivative of f at any
        given input.
        starting_x: the starting guess for the root. If this value is too
        far from the true root (where "too far" depends on how chaotic
        f is near the root) then Newton's method may fail to converge to
        the root.

    Returns:
        A generator that yields the x values corresponding to
        steps of Newton's method.
    """
    x = starting_x
    while True:
        yield x
        x -= f(x) / f_derivative(x)


if __name__ == "__main__":
    def f(x):
        return x**5 - x - 1

    def f_derivative(x):
        return 5 * x**4 - 1

    starting_x = 1
    # starting_x = 0  # try this for a case that fails to converge

    approximation = []
    i = 0
    for x in newton_sequence(f, f_derivative, starting_x):
        approximation.append(x)
        i += 1
        if i == 100:
            break

    for x in approximation:
        print((x, f(x)))
