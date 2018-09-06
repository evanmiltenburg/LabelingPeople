import glob

filenames = glob.glob('./resources/Categories/*.txt')

with open('./resources/selected_attributes.txt') as f:
    attributes = {line.strip() for line in f}

print('Initially:', len(attributes))

categorized = set()
for filename in filenames:
    with open(filename) as f:
        categorized = categorized | {line.strip() for line in f}

attributes = sorted(attributes - categorized)

print('Remaining:', len(attributes))

with open('todo.txt','w') as f:
    f.write('\n'.join(attributes))
