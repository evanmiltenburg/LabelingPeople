import json
import glob
import re

import spacy
from numpy import median, std, mean

def load_json(filename):
    "Load a JSON file."
    with open(filename) as f:
        return json.load(f)


def get_lengths(descriptions):
    "Get lengths for an iterable of text."
    lengths = [len(nlp.tokenizer(text)) for text in descriptions]
    return lengths


def load_face2text(filename):
    "Load the Face2Text descriptions."
    data = load_json(filename)
    descriptions = [description['text'] for img in data for description in img['descriptions']]
    return descriptions


def gendered_labels(files):
    "Take a list of files, and generate all labels ending with gendered nouns."
    pattern = re.compile('\[/EN#\d+/people (.*?)\]', re.IGNORECASE)
    for filename in files:
        with open(filename) as f:
            text = f.read()
            results = pattern.findall(text)
            for label in results:
                if label in GENDERED or label.split()[-1] in GENDERED:
                    label = label
                    yield label



nlp = spacy.load('en',disable=['parser','ner'])
face2text = load_face2text('/Users/Emiel/PhD/Datasets/face2text_v0.1/clean.json')
f2t_lengths = get_lengths(face2text)


GENDERED    = set(load_json('../Flickr30k/resources/gendered.json'))
files = glob.glob('../Flickr30k/resources/Sentences/*.txt')
label_generator = gendered_labels(files)
f30k_lengths = get_lengths(label_generator)

print('Name, mean, median, std')
print('Face2text', mean(f2t_lengths), median(f2t_lengths), std(f2t_lengths))
print('Flickr30K', mean(f30k_lengths), median(f30k_lengths), std(f30k_lengths))
