import typer

from rich import print
from classifier import classify
from segmenter import Segmenter

app = typer.Typer()

# TODO:
@app.command()
def annotate(inline: str = "", filename: str = "") -> None:
    html = ""

    if inline:
        html = inline
    elif filename:
        try:
            with open(filename, "r") as file:
                html = file.read()
        except FileNotFoundError:
            print(f"[red]File not found: {filename}[/red]")
            typer.Exit(code=1)
    else:
        print("[red]Please, provide HTML either [italic]inline[/italic] or via [italic]filename[/italic][/red]")
        raise typer.Exit(code=1)

    # TODO: Validate HTML.
    # TODO: Split HTML into segments.
    segmenter = Segmenter(html)
    # TODO: Classify each segment.

if __name__ == "__main__":
    app()
