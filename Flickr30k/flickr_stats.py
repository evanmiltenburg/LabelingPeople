import glob
import re
from collections import Counter

files = glob.glob('resources/Sentences/*.txt')
pattern = re.compile('\[/EN#\d+/people (.*?)\]', re.IGNORECASE)

GENDERED = { 'male', 'males',
             'female', 'females',
             'girl', 'girls',
             'boy', 'boys',
             'man', 'men',
             'woman', 'women'
             }


def normalize_label(label):
    "Normalize the label."
    label = label.replace('@ ','')
    label = label.lower().replace(' , ',' ').replace(' + ', ' ')
    label = label.replace('(','').replace(')','')
    label = label.replace(' & ', ' ').replace('  ', ' ')
    return label.strip()

def all_labels():
    "Get number of labels."
    c = Counter()
    for filename in files:
        with open(filename) as f:
            text = f.read()
            results = pattern.findall(text)
            results = [normalize_label(s) for s in results]
            c.update(results)
    return dict(unique=len(c),
                total=sum(c.values()))


def gendered_labels():
    "Get number of gendered labels."
    c = Counter()
    for filename in files:
        with open(filename) as f:
            text = f.read()
            results = pattern.findall(text)
            results = [normalize_label(s) for s in results]
            for label in results:
                if label in GENDERED or label.split()[-1] in GENDERED:
                    c[label] += 1
    return dict(unique=len(c),
                total=sum(c.values()))


print('all', all_labels())
print('gendered', gendered_labels())
