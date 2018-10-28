import os
import shutil
import tempfile

from plot_waves import create_and_save_plots


def test_generate_plots():
    tmpdir = tempfile.mkdtemp()
    five_filename = os.path.join(tmpdir, "five.pdf")
    hundred_filename = os.path.join(tmpdir, "hundred.pdf")
    try:
        create_and_save_plots(five_filename, hundred_filename)
    finally:
        shutil.rmtree(tmpdir)
