import os
import pathlib
import pickle

from learnhtml.extractor import HTMLExtractor
class Preprocessor:
    def __init__(self):
        with open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'models/model.pkl'), 'rb') as file:
            model = pickle.load(file)
        self.extractor = HTMLExtractor(model)

    def preprocess(self, html: str) -> str:
        return self.extractor.extract_from_html(html)
