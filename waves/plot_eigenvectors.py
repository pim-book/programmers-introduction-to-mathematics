import numpy


markers = ["o", "v", "s", "+", "x", "d", "p", "*"]


def plot_eigenvectors(eigensystem, markersize=6):
    eigenvalues, eigenvectors = eigensystem
    x = numpy.arange(0, len(eigenvectors[0]), 1)
    fig = plt.figure()
    for val, vec, marker in zip(eigenvalues, eigenvectors, markers):
        plt.plot(x, vec, marker=marker, markersize=markersize,
                 label="λ = %G" % val)

    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    return fig


def create_and_save_plots():
    A = bead_matrix(5)
    eigensystem = sorted_eigensystem(A)
    eigenvalues, eigenvectors = eigensystem

    print("%s | %s" % ("eigenvalue", "eigenvector"))
    for val, vec in zip(eigenvalues, eigenvectors):
        vec_str = ", ".join(["%5.2f" % entry for entry in vec])
        print("%10.2f | %s" % (val, vec_str))

    fig1 = plot_eigenvectors(eigensystem)
    fig1.savefig("eigenvalues_5_beads.pdf", bbox_inches="tight")

    fig2 = plot_eigenvectors(
        sorted_eigensystem(bead_matrix(100), top_k=5), markersize=4)
    fig2.savefig("eigenvalues_100_beads.pdf", bbox_inches="tight")


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    A = bead_matrix(5)
    eigensystem = sorted_eigensystem(A)
    eigenvalues, eigenvectors = eigensystem
    w = [0, 0.5, 0, 0, 0]
    coeffs = decompose(eigenvectors, w)
    reconstructed = numpy.sum(
        [coeffs[i] * eigenvectors[i] for i in range(5)], axis=0)
    print("w={}\nreconstructed={}".format(w, reconstructed))
