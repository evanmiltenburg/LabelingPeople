import nltk
from nltk import ChartParser
import glob
import re
import json
from collections import Counter

def load_json(filename):
    "Utility function to load json files in one line."
    with open(filename) as f:
        return json.load(f)

GENDERED    = set(load_json('./resources/gendered.json'))
STOPWORDS   = set(load_json('./resources/stopwords.json')) | set(map(str,range(100)))
TYPOS       = load_json('./resources/typos.json')


def remove_stopwords(label):
    """
    Remove stopwords from a single label.
    """
    tokenized = label.split()
    # Keep removing stopwords until a word doesn't match.
    for i,word in enumerate(tokenized):
        if word not in STOPWORDS:# and len(word) > 1:
            return ' '.join(tokenized[i:])
    # For the empty string.
    return ''


def normalize(label):
    "Normalize the label."
    label = label.replace('@ ','')
    label = label.lower().replace(' , ',' ').replace(' + ', ' ')
    label = label.replace('(','').replace(')','')
    label = label.replace(' & ', ' ').replace('  ', ' ')
    return label

def gendered_labels(files):
    "Take a list of files, and generate all labels ending with gendered nouns."
    pattern = re.compile('\[/EN#\d+/people (.*?)\]', re.IGNORECASE)
    for filename in files:
        with open(filename) as f:
            text = f.read()
            results = pattern.findall(text)
            for label in results:
                if label in GENDERED or label.split()[-1] in GENDERED:
                    label = normalize(label)
                    yield label


def clear_stopwords(labels):
    "Clear stopwords from a set of labels."
    for label in labels:
        label = remove_stopwords(label)
        yield label


def correct_typos(labels):
    "Dictionary-based typo correction"
    for label in labels:
        tokens = [TYPOS[word] if word in TYPOS else word
                    for word in label.split()]
        label = ' '.join(tokens)
        yield label


def grammatical(tokenized_label):
    "Check whether the label is admissible by the grammar."
    try:
        analysis = parser.parse(tokenized_label)
    except ValueError:
        return False
    if list(analysis) == []:
        return False
    else: return True


# Load grammar.
grammar = nltk.data.load('labelgrammar.cfg')
parser = ChartParser(grammar)

# Load labels.
files = glob.glob('resources/Sentences/*.txt')
label_generator = clear_stopwords(correct_typos(gendered_labels(files)))

# Filter grammatical.
all_labels = {label for label in label_generator if ' ' in label}
ungrammatical = {label for label in all_labels if not grammatical(label.split())}

print(len(all_labels), 'labels in total, after filtering stopwords and correcting typos')
print(len(ungrammatical), 'ungrammatical labels remaining')

# Write ungrammatical to file.
with open('ungrammatical.txt','w') as f:
    lines = [label + '\n' for label in sorted(ungrammatical)]
    f.writelines(lines)

with open('grammatical.txt','w') as f:
    lines = [label + '\n' for label in sorted(all_labels - ungrammatical)]
    f.writelines(lines)
