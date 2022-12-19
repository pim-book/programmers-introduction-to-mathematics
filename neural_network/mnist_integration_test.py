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
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, tmpdir)

    try:
        train_mnist(tmpdir, num_epochs=1)
    finally:
        shutil.rmtree(tmpdir)
