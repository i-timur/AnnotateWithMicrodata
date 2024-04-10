import os

import click
import click_log

from bs4 import BeautifulSoup

from src.classification.classifier import Classifier
from src.classification.preprocessor import Preprocessor
from src.common.constants import CONFIDENCE_THRESHOLD, CLASS_MAP, ID_ATTR
from src.cli.params import HTMLInput
from src.classification.segmenter import Segmenter
from src.common.log import logger
from src.common.utils import clear_string, clean_html, set_unique_ids, remove_unique_ids, change_filename


@click.group()
def cli():
    pass

@cli.command(short_help='Annotate HTML content with microdata')
@click_log.simple_verbosity_option(logger, help='Output logging information', required=False)
@click.argument('html', type=HTMLInput(), required=True)
@click.option('-o', '--output', 'output', type=str, help='Path to the output file', required=False)
@click.option('-s', '--skip-products', 'skip_products', is_flag=True, help='Skip items that are related to product entity', required=False)
@click.option('-t', '--threshold', 'confidence_threshold', type=float, help='Confidence threshold for classification', required=False, default=CONFIDENCE_THRESHOLD)
@click.option('--save-preprocessed', 'save_preprocessed', is_flag=True, help='Save preprocessed HTML content to file', required=False)
def annotate(html, output, skip_products, confidence_threshold, save_preprocessed):
    click.echo('Starting annotation process')

    soup = BeautifulSoup(html, 'html.parser')

    logger.info('Adding unique ids to HTML content')
    set_unique_ids(soup)

    logger.info('Preprocessing HTML content')
    preprocessor = Preprocessor()
    x_paths = preprocessor.preprocess(html)
    logger.info(f'Preprocessed XPaths: {x_paths}')
    logger.info(f'Preprocessed {len(x_paths)} elements')

    cleaned_html = clean_html(str(soup), x_paths)
    logger.info('Preprocessing completed')

    if save_preprocessed:
        path = 'preprocessed.html'
        logger.info('Saving preprocessed HTML content to file: preprocessed.html')

        try:
            with open(os.path.expanduser(path), 'wt') as file:
                file.write(cleaned_html)
                logger.info('Preprocessed HTML content saved to file')
        except Exception as error:
            click.echo(f'Error writing to file: {error}')

    logger.info('Segmenting HTML content')
    splitter = Segmenter()
    segments = splitter.segment_html(cleaned_html)
    logger.info(f'Segmented {len(segments)} block(s)')

    logger.info('Classifying segments')
    classifier = Classifier()
    classified_segments = []

    added_items = dict()

    for segment_id, segment in segments.items():
        for record in segment["records"]:
            text = clear_string(" ".join(record["texts"]))
            words = [word for word in text.split(" ")]

            if not words:
                continue

            proba = classifier.classify(text)
            max_idx = proba.argmax()

            if skip_products and max_idx == 0:
                continue

            if proba[max_idx] > confidence_threshold:
                for selector in record['unique_ids']:
                    classified_segments.append((selector, CLASS_MAP[max_idx]))
                    added_items[CLASS_MAP[max_idx]] = added_items.get(CLASS_MAP[max_idx], 0) + 1

    logger.info(f'Classified {len(classified_segments)} record(s)')

    splitter.soup = soup

    for selector, itemtype in classified_segments:
        for element in soup.select(f'[{ID_ATTR}="{selector}"]'):
            logger.info(f'Annoted {splitter.get_css_selector(element)} with {itemtype}')
            element['itemscope'] = None
            element['itemtype'] = itemtype

    logger.info('Removing unique ids from HTML content')
    remove_unique_ids(soup)
    result = soup.prettify()

    if output:
        logger.info(f'Saving annotated HTML content to file: {output}')

        try:
            with open(os.path.expanduser(output), 'wt') as file:
                file.write(result)
                logger.info('Annotated HTML content saved to file')
        except Exception as error:
            click.echo(f'Error writing to file: {error}')
    else:
        click.echo(result)

    for itemtype, count in added_items.items():
        if count:
            logger.info(f'Annotated {count} {itemtype.split("/")[3]}(s)')

    click.echo('Done!')
