import torch

from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained('i-timur/microdata-classifier')
tokenizer = AutoTokenizer.from_pretrained('i-timur/microdata-classifier')

def classify(text):
    with torch.no_grad():
        proba = torch.softmax(model(**tokenizer(text, return_tensors='pt', truncation=True, max_length=512).to(model.device)).logits, -1)
    return proba.cpu().numpy()[0]
