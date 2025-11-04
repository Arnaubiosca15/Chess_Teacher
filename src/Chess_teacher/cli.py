"""Console script for Chess_teacher."""

import typer
from rich.console import Console

from Chess_teacher import utils

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for Chess_teacher."""
    console.print("Replace this message by putting your code into "
               "Chess_teacher.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
