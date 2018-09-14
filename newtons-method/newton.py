
def newton_sequence(f, f_derivative,  starting_x):
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
