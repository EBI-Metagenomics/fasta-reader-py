from statistics import mean

import click

from ._reader import read_fasta
from ._version import __version__


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__)
@click.argument("fasta", type=click.Path(exists=True))
def cli(fasta):
    """
    Show information about FASTA files.

    Warning
    -------
    The commad line interface is in EXPERIMENTAL stage. It might change in
    future releases.
    """
    with read_fasta(fasta) as file:
        items = file.read_items()

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
