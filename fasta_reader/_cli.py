from statistics import mean

import click

from ._parser import open_fasta


def get_version():
    import pkg_resources
    import re
    from os.path import realpath, dirname, join

    if __name__ == "__main__":
        filepath = join(dirname(realpath(__file__)), "..", "__init__.py")
        with open(filepath, "r", encoding="utf8") as f:
            content = f.read()
    else:
        content = pkg_resources.resource_string(__name__.split(".")[0], "__init__.py")
        content = content.decode()

    c = re.compile(r"__version__ *= *('[^']+'|\"[^\"]+\")")
    m = c.search(content)
    if m is None:
        return "unknown"
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
