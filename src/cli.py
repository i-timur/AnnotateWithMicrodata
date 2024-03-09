#!/usr/bin/env python3

import os

import typer

from rich import print
from src.microdata.classifier import Classifier
from src.microdata.segmenter import Segmenter
from src.microdata.utils import clear_string, CLASS_MAP
from PyInquirer import prompt

CONFIDENCE_THRESHOLD = 0.5
EMPTY_CATEGORY = "Skip"

app = typer.Typer()

@app.command("annotate")
def annotate(inline: str = "", filepath: str= "", output: str = "") -> None:
    html = ""

    if inline:
        html = inline
    elif filepath:
        expanded_filepath = os.path.expanduser(filepath)

        try:
            with open(expanded_filepath, "rt") as file:
                html = file.read()
        except FileNotFoundError:
            print(f"[red]File not found: {filepath}[/red]")
            typer.Exit(code=1)
    else:
        print("[red]Please, provide HTML either [italic]inline[/italic] or via [italic]filepath[/italic][/red]")
        raise typer.Exit(code=1)

    # TODO: Validate HTML before proceeding.
    segmenter = Segmenter()
    segments = segmenter.segment_html(html)
    classifier = Classifier()

    for segment_id, segment in segments.items():
        for record in segment["records"]:
            text = clear_string(" ".join(record["texts"]))
            words = [word for word in text.split(" ")]

            if len(words) < 4:
                continue

            proba = classifier.classify(text)
            max_idx = proba.argmax()

            if proba[max_idx] < CONFIDENCE_THRESHOLD:
                classes_list_question = [
                    {
                        "type": "list",
                        "name": "category",
                        "message": f"The following text has low confidence. Please, select the correct category or skip it: {text}",
                        "choices": [v for k, v in CLASS_MAP.items()] + [EMPTY_CATEGORY]
                    }
                ]

                category = prompt(classes_list_question)["category"]

                if category == EMPTY_CATEGORY:
                    continue

                category_idx = list(CLASS_MAP.values()).index(category)

                for selector in record["css_selector"]:
                    soup = segmenter.soup
                    element = soup.select(selector)[0]
                    # TODO: Add empty itemtype attribute to the element.
                    element["itemscope"] = ""
                    element["itemtype"] = CLASS_MAP[category_idx]
            else:
                for selector in record["css_selector"]:
                    soup = segmenter.soup
                    element = soup.select(selector)[0]
                    # TODO: Add empty itemtype attribute to the element.
                    element["itemscope"] = ""
                    element["itemtype"] = CLASS_MAP[max_idx]


    # TODO: Clear the tree from the tags that were added during the annotation process.

    result = segmenter.soup.prettify()

    if output:
        expanded_output_path = os.path.expanduser(output)
        try:
            with open(expanded_output_path, "wt") as file:
                file.write(result)
        except Exception as error:
            print(f"[red]Error writing to file: {error}[/red]")
            typer.Exit(code=1)
    else:
        print(result)

def main():
    app()
