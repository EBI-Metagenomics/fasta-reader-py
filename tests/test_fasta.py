import os
from pathlib import Path

import pytest

from fasta_reader import read_fasta, write_fasta
from fasta_reader.errors import ParsingError

FIXTURE_DIR = Path(__file__).parent.resolve() / "data"

CORRECT_FILES = pytest.mark.datafiles(
    FIXTURE_DIR / "correct1.fna",
    FIXTURE_DIR / "correct2.fna",
)

EMPTY_SEQUENCES = pytest.mark.datafiles(FIXTURE_DIR / "correct3.fna")
EMPTY_FILE = pytest.mark.datafiles(FIXTURE_DIR / "empty.fna")

DAMAGED_FILES = pytest.mark.datafiles(
    FIXTURE_DIR / "damaged1.fna",
    FIXTURE_DIR / "damaged2.fna",
)

COMPRESSED_FILE = pytest.mark.datafiles(FIXTURE_DIR / "protein.faa.gz")


@CORRECT_FILES
def test_read_trivial_files(datafiles: Path):
    for file in datafiles.iterdir():
        deflines = ["ID1", "ID2", "ID3", "ID4"]
        sequences = ["GAGUUA", "CAUAACAAATT", "AAGAA", "AAGAA"]

        f = read_fasta(file)
        item = f.read_item()
        assert item.defline == deflines[0]
        assert item.id == deflines[0]
        assert not item.has_description
        assert item.sequence == sequences[0]

        item = f.read_item()
        assert item.defline == deflines[1]
        assert item.id == deflines[1]
        assert not item.has_description
        assert item.sequence == sequences[1]

        item = f.read_item()
        assert item.defline == deflines[2]
        assert item.id == deflines[2]
        assert not item.has_description
        assert item.sequence == sequences[2]

        item = f.read_item()
        assert item.defline == deflines[3]
        assert item.id == deflines[3]
        assert not item.has_description
        assert item.sequence == sequences[3]

        with pytest.raises(StopIteration):
            f.read_item()

        f.close()

        f = read_fasta(file)
        for i, item in enumerate(f):
            assert item.defline == deflines[i]
            assert item.sequence == sequences[i]
        f.close()

        f = read_fasta(file)
        items = f.read_items()
        for i, defline in enumerate(deflines):
            assert items[i].defline == defline
            assert items[i].sequence == sequences[i]
        f.close()

        with read_fasta(file) as f:
            for i, item in enumerate(f):
                assert item.defline == deflines[i]
                assert item.sequence == sequences[i]

        with read_fasta(file) as f:
            f.close()


@EMPTY_SEQUENCES
def test_read_empty_sequences(datafiles: Path):
    for file in datafiles.iterdir():
        deflines = ["ID1", "ID2", "ID3", "ID4"]
        sequences = ["", "", "", ""]

        f = read_fasta(file)
        item = f.read_item()
        assert item.defline == deflines[0]
        assert item.id == deflines[0]
        assert not item.has_description
        assert item.sequence == sequences[0]

        item = f.read_item()
        assert item.defline == deflines[1]
        assert item.id == deflines[1]
        assert not item.has_description
        assert item.sequence == sequences[1]

        item = f.read_item()
        assert item.defline == deflines[2]
        assert item.id == deflines[2]
        assert not item.has_description
        assert item.sequence == sequences[2]

        item = f.read_item()
        assert item.defline == deflines[3]
        assert item.id == deflines[3]
        assert not item.has_description
        assert item.sequence == sequences[3]


@EMPTY_FILE
def test_read_empty_file(datafiles: Path):
    for file in datafiles.iterdir():
        f = read_fasta(file)
        with pytest.raises(StopIteration):
            f.read_item()


@DAMAGED_FILES
def test_read_damaged_files(datafiles: Path):
    damaged = list(sorted(datafiles.iterdir()))

    with read_fasta(damaged[0]) as f:
        with pytest.raises(ParsingError) as excinfo:
            f.read_item()
        e: ParsingError = excinfo.value
        assert e.line_number == 0

    with read_fasta(damaged[1]) as f:
        f.read_item()
        with pytest.raises(ParsingError) as excinfo:
            f.read_item()
        e: ParsingError = excinfo.value
        assert e.line_number == 3


@COMPRESSED_FILE
def test_read_compressed_file(datafiles: Path):
    expected = """
QIKDLLVSSSTDLDTTLVLVNAIYFKGMWKTAFNAEDTREMPFHVTKQESKPVQMMCMNNSFNVATLPAE
KMKILELPFASGDLSMLVLLPDEVSDLERIEKTINFEKLTEWTNPNTMEKRRVKVYLPQMKIEEKYNLTS
VLMALGMTDLFIPSANLTGISSAESLKISQAVHGAFMELSEDGIEMAGSTGVIEDIKHSPESEQFRADHP
FLFLIKHNPTNTIVYFGRYWSP
    """.replace(
        "\n", ""
    ).strip()

    file = next(datafiles.iterdir())
    assert len(list(read_fasta(file))) == 1

    with read_fasta(file) as reader:
        item = reader.read_item()
        assert item.defline == "P01013 GENE X PROTEIN (OVALBUMIN-RELATED)"
        assert item.has_description
        assert item.description == "GENE X PROTEIN (OVALBUMIN-RELATED)"
        assert item.id == "P01013"
        assert item.sequence == expected


def test_write_file(tmp_path: Path):
    defline = ["defline1", "defline2 description"]
    sequence = ["ABCD", "ABCD" * 100]

    os.chdir(tmp_path)
    with write_fasta("output.faa") as writer:
        writer.write_item(defline[0], sequence[0])
        writer.write_item(defline[1], sequence[1])

    with read_fasta("output.faa") as reader:
        item = reader.read_item()
        assert item.defline == defline[0]
        assert item.sequence == sequence[0]

        item = reader.read_item()
        assert item.defline == defline[1]
        assert item.sequence == sequence[1]

    with write_fasta("output.faa.xz") as writer:
        writer.write_item(defline[0], sequence[0])
        writer.write_item(defline[1], sequence[1])

    with read_fasta("output.faa.xz") as reader:
        item = reader.read_item()
        assert item.defline == defline[0]
        assert item.sequence == sequence[0]

        item = reader.read_item()
        assert item.defline == defline[1]
        assert item.sequence == sequence[1]
