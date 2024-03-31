import os

import click

from src.classification.classifier import Classifier
from src.common.constants import CONFIDENCE_THRESHOLD, CLASS_MAP
from src.cli.params import HTMLInput
from src.classification.segmenter import Segmenter
from src.common.utils import clear_string

@click.group()
def cli():
    pass

@cli.command(short_help='Annotate HTML content with microdata')
@click.argument('html', type=HTMLInput(), required=True)
@click.option('-o', '--output', 'output', type=str, help='Path to the output file', required=False)
def annotate(html, output):
    splitter = Segmenter()
    segments = splitter.segment_html(html)
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
                pass
                # classes_list_question = [
                #     {
                #         "type": "list",
                #         "name": "category",
                #         "message": f"The following text has low confidence. Please, select the correct category or skip it: {text}",
                #         "choices": [v for k, v in CLASS_MAP.items()] + [EMPTY_CATEGORY]
                #     }
                # ]
                #
                # category = prompt(classes_list_question)["category"]
                #
                # if category == EMPTY_CATEGORY:
                #     continue
                #
                # category_idx = list(CLASS_MAP.values()).index(category)
                #
                # for selector in record["css_selector"]:
                #     soup = splitter.soup
                #     element = soup.select(selector)[0]
                #     element["itemscope"] = None
                #     element["itemtype"] = CLASS_MAP[category_idx]
            else:
                for selector in record['css_selector']:
                    soup = splitter.soup
                    element = soup.select(selector)[0]
                    element['itemscope'] = None
                    element['itemtype'] = CLASS_MAP[max_idx]

    result = splitter.soup.prettify()

    if output:
        try:
            with open(os.path.expanduser(output), 'wt') as file:
                file.write(result)
        except Exception as error:
            click.echo(f'Error writing to file: {error}')
    else:
        click.echo(result)
