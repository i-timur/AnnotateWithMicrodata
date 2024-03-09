from typing import Any

import torch

from transformers import AutoModelForSequenceClassification, AutoTokenizer

class Classifier:
    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained('i-timur/microdata-classifier')
        self.tokenizer = AutoTokenizer.from_pretrained('i-timur/microdata-classifier')

    def classify(self, text: str) -> Any:
        with torch.no_grad():
            proba = torch.softmax(self.model(**self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512).to(self.model.device)).logits, -1)
        return proba.cpu().numpy()[0]
