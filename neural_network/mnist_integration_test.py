import os
import random
import shutil
import tarfile
import tempfile

from mnist_network import train_mnist


def test_train_mnist():
    random.seed(1)
    tmpdir = tempfile.mkdtemp()
    test_dir = os.path.dirname(__file__)
    mnist_archive = os.path.join(test_dir, 'mnist', 'mnist.tar.gz')

    with tarfile.open(mnist_archive) as tar:
        tar.extractall(tmpdir)

    try:
        train_mnist(tmpdir, num_epochs=1)
    finally:
        shutil.rmtree(tmpdir)
