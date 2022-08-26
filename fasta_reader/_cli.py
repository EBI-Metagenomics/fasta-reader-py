import sys
from statistics import mean

import click
import plotille

from ._reader import read_fasta
from ._writer import write_fasta


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option()
@click.argument("fasta", type=click.Path(exists=True))
@click.option("--stats/--no-stats", default=True, help="Show sequence statistics.")
@click.option(
    "--hist/--no-hist", default=False, help="Show histogram of sequence lengths."
)
@click.option("--ncols", default=0, help="Show formatted sequences.")
@click.option(
    "--upper/--no-upper",
    default=False,
    help="Convert sequence symbols to uppercase.",
)
def cli(fasta, stats: bool, hist: bool, ncols: int, upper: bool):
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
        if upper:
            seq = item.sequence.upper()
        else:
            seq = item.sequence
        abc |= set(seq)
        nitems += 1

    if stats:
        usymbols = "".join(sorted(list(abc)))
        click.echo(f"Number of sequences: {nitems}")
        click.echo(f"Unique sequence symbols: {usymbols}")
        msg = f"Sequence length: min {min(seq_lens)}, mean {mean(seq_lens)}, max {max(seq_lens)}"
        click.echo(msg)

    if hist:
        show_hist(seq_lens)

    if ncols > 0:
        with write_fasta(sys.stdout, ncols) as writer:
            for item in read_fasta(fasta):
                if upper:
                    seq = item.sequence.upper()
                else:
                    seq = item.sequence
                writer.write_item(item.defline, seq)


def show_hist(seq_lengths):

    click.echo(plotille.hist(seq_lengths))
