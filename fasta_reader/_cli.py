from statistics import mean

import click

from ._parser import open_fasta


def get_version():
    import re
    import fasta_reader
    import importlib_resources as pkg_resources

    content = pkg_resources.read_text(fasta_reader, "__init__.py")
    c = re.compile(r"__version__ *= *('[^']+'|\"[^\"]+\")")
    m = c.search(content)
    return m.groups()[0][1:-1]


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(get_version())
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
