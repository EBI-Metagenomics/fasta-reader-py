# Welcome to fasta-reader 👋

> Read and write FASTA file

### 🏠 [Homepage](https://github.com/EBI-Metagenomics/fasta-reader-py)

## ⚡️ Requirements

- Python >= 3.9
- Pip

## Install

```sh
pip install fasta-reader
```

## Usage

```

```

## Example

Open a file and loop over its contents.

```python
from fasta_reader import read_fasta

for item in read_fasta("fasta_reader/test/correct1.faa"):
  print(item)
# FASTAItem(defline='ID1', sequence='GAGUUA')
# FASTAItem(defline='ID2', sequence='CAUAACAAATT')
# FASTAItem(defline='ID3', sequence='AAGAA')
# FASTAItem(defline='ID4', sequence='AAGAA')
```

Open a compressed file and show the first item.

```python
from fasta_reader import read_fasta

with read_fasta("fasta_reader/test/protein.faa.gz") as file:
    item = file.read_item()
    print(item.defline, item.sequence[:10] + "...")
# P01013 GENE X PROTEIN (OVALBUMIN-RELATED) QIKDLLVSSS...
```

Write to `output.faa.gz`.

```python
from fasta_reader import write_fasta

with write_fasta("output.faa.gz") as file:
    file.write_item("id1 gene x protein", "AGUTAGA")
    file.write_item("id2 gene x protein", "TUUA")
```

## 👤 Author

- [Danilo Horta](https://github.com/horta)

## Show your support

Give a ⭐️ if this project helped you!
