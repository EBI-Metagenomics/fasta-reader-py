import pytest


@pytest.fixture
def correct1(tmp_path):
    return _write_file(tmp_path, "correct1.seq")


@pytest.fixture
def correct2(tmp_path):
    return _write_file(tmp_path, "correct2.seq")


@pytest.fixture
def damaged1(tmp_path):
    return _write_file(tmp_path, "damaged1.seq")


@pytest.fixture
def damaged2(tmp_path):
    return _write_file(tmp_path, "damaged2.seq")


@pytest.fixture
def damaged3(tmp_path):
    return _write_file(tmp_path, "damaged3.seq")


def _write_file(path, filename):
    import importlib_resources as pkg_resources
    import fasta_reader

    text = pkg_resources.read_text(fasta_reader.test, filename)

    with open(path / filename, "w") as f:
        f.write(text)

    return path / filename
