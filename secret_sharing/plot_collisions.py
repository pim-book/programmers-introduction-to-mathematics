if __name__ == "__main__":
    import matplotlib as mpl
    mpl.use('TkAgg')

    import numpy as np
    import matplotlib.pyplot as plt
    from interpolate import *

    # Create a figure of size 8x6 points, 80 dots per inch
    plt.figure(figsize=(8, 8), dpi=80)

    # starting from these base points, we compute different polynomials
    # passing through these two points with a whatever decoded "secret" we wish.
    points = [(2., 1083.), (5., 6609.)]

    f = interpolate(points + [(0., 533.)])
    x = np.linspace(-1.0, 6.0, 256, endpoint=True)
    y = np.array([f.evaluateAt(p) for p in x])
    plt.plot(x, y, color="black", linewidth=3.0, linestyle="-")

    f = interpolate(points + [(0., 2000.)])
    y = np.array([f.evaluateAt(p) for p in x])
    plt.plot(x, y, color="black", linewidth=3.0, linestyle="-.")

    f = interpolate(points + [(0., 5000.)])
    y = np.array([f.evaluateAt(p) for p in x])
    plt.plot(x, y, color="black", linewidth=3.0, linestyle=":")

    f = interpolate(points + [(0., 7500.)])
    y = np.array([f.evaluateAt(p) for p in x])
    plt.plot(x, y, color="black", linewidth=3.0, linestyle="--")

    plt.scatter(*zip(*points), zorder=10)

    p0 = points[0]
    plt.annotate(
        "({}, {})".format(*p0),
        xy=(p0[0], p0[1]),
        xytext=(p0[0], p0[1] - 1000),
        arrowprops=dict(facecolor='black', shrink=0.01))

    p1 = points[1]
    plt.annotate(
        "({}, {})".format(*p1),
        xy=(p1[0], p1[1]),
        xytext=(p1[0] - 1.5, p1[1] + 500),
        arrowprops=dict(facecolor='black', shrink=0.01))

    # Set labels
    plt.xlim(0, 6)
    plt.ylim(-200, 8000)
    ax = plt.gca()
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # Save the figure to the output SVG file
    plt.savefig("polynomials-perfect-secrecy.svg")
