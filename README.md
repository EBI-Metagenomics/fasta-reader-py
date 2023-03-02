# Welcome to fasta-reader 👋

> Read and write FASTA file

### 🏠 [Homepage](https://github.com/EBI-Metagenomics/fasta-reader-py)

## ⚡️ Requirements

- Python >= 3.9

## Install

```sh
pip install fasta-reader
```

## Examples

The following example show that it can read a compressed file remotely seamlessly:

```python
from fasta_reader import read_fasta

ROOT = "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/858/895"
REF = "GCF_009858895.2_ASM985889v3"
FILE = f"{ROOT}/{REF}/{REF}_genomic.fna.gz"

for item in read_fasta(FILE):
    print(item)
```

We can also write a FASTA file in a compressed format directly:

```python
from fasta_reader import write_fasta

with write_fasta("protein.faa.gz") as file:
    file.write_item("P01013 GENE X PROTEIN", "QIKDLLVSSSTDLDT...")
```

## 👤 Author

- [Danilo Horta](https://github.com/horta)

## Show your support

Give a ⭐️ if this project helped you!
