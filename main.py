import typer
from rich import print

app = typer.Typer()

# TODO:
@app.command()
def annotate(inline: str = "", filename: str = "") -> None:
    if not inline and not filename:
        print("[red]Please, provide HTML either [italic]inline[/italic] or via [italic]file[/italic][/red]")
        raise typer.Exit(code=1)

    html = """
    """
    pass

if __name__ == "__main__":
    app()
