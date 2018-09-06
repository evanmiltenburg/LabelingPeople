import nltk
from nltk import ChartParser

# Load grammar.
grammar = nltk.data.load('labelgrammar.cfg')
parser = ChartParser(grammar)

def analyze_label(label):
    "Analyze a label using our CFG."
    tokenized_label = label.split()
    try:
        analysis = parser.parse(tokenized_label)
        trees = list(analysis)
        for tree in trees:
            print(tree)
        if len(trees) > 0:
            return analysis
        else:
            print('No analysis possible')
            return None
    
    except ValueError as e:
        print('No analysis possible:', e.strerror)
        return None
        
