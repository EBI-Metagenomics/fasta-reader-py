from statistics import mean

import click

from ._reader import read_fasta
from ._version import __version__


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__)
@click.argument("fasta", type=click.Path(exists=True))
@click.option(
    "--hist/--no-hist", default=False, help="Show histogram of sequence lengths."
)
def cli(fasta, hist: bool):
    """
    Show information about FASTA files.

    \b
    Warning
    -------
    The commad line interface is in EXPERIMENTAL stage. It might change in
    future releases.
    """

    nitems = 0
    abc = set([])
    seq_lens = []
    for item in read_fasta(fasta):
        seq_lens.append(len(item.sequence))
        abc |= set(item.sequence)
        nitems += 1

    usymbols = "".join(sorted(list(abc)))
    click.echo(f"Number of sequences: {nitems}")
    click.echo(f"Unique sequence symbols: {usymbols}")
    msg = f"Sequence length: min {min(seq_lens)}, mean {mean(seq_lens)}, max {max(seq_lens)}"
    click.echo(msg)

    if hist:
        show_hist(seq_lens)


def show_hist(seq_lengths):
    import plotille

    click.echo(plotille.hist(seq_lengths))
