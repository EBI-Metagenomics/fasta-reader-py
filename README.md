# fasta-reader-py

FASTA file reader.

## Examples

Loop over its contents.

```ipython
>>> from fasta_reader import open_fasta
>>>
>>> for item in open_fasta("fasta_reader/test/correct1.faa"):
...     print(item)
FASTAItem(defline='ID1', sequence='GAGUUA')
FASTAItem(defline='ID2', sequence='CAUAACAAATT')
FASTAItem(defline='ID3', sequence='AAGAA')
FASTAItem(defline='ID4', sequence='AAGAA')

```

Open a compressed file and show the first item.

```ipython
>>> from fasta_reader import open_fasta
>>>
>>> with open_fasta("fasta_reader/test/protein.faa.gz") as file:
...     item = file.read_item()
...     print(item.defline, item.sequence[:10] + "...")
P01013 GENE X PROTEIN (OVALBUMIN-RELATED) QIKDLLVSSS...

```

## Install

```bash
pip install fasta-reader
```

## Author

* [Danilo Horta](https://github.com/horta)

## License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/EBI-Metagenomics/fasta-reader-py/master/LICENSE.md).
