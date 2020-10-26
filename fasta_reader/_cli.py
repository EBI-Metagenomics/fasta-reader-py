from statistics import mean

import click

from ._parser import open_fasta
from ._version import __version__


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__)
@click.argument("fasta", type=click.File("r"))
def cli(fasta):
    """
    Show information about FASTA files.
    """
    with open_fasta(fasta) as parser:
        items = parser.read_items()

    nitems = len(items)
    abc = set([])
    seq_lens = []
    for item in items:
        seq_lens.append(len(item.sequence))
        abc |= set(item.sequence)

    usymbols = "".join(sorted(list(abc)))
    click.echo(f"Number of sequences: {nitems}")
    click.echo(f"Unique sequence symbols: {usymbols}")
    click.echo(f"Average sequence length: {mean(seq_lens)}")
