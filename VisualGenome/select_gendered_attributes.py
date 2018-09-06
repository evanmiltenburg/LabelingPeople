from collections import Counter, defaultdict
import json
import zipfile

def load_json(filename):
    "Wrapper to load JSON files in one line."
    with open(filename) as f:
        return json.load(f)

def load_zipped_json(zipname, filename):
    file = zipfile.ZipFile(zipname)
    opened = file.open(filename)
    data = json.load(opened)
    opened.close()
    file.close()
    return data

GENDERED = set(load_json('./resources/gendered.json'))

def get_attribute_dict():
    "Get a dictionary with attribute counts for all objects."
    attributes_file = load_zipped_json('./resources/attributes.json.zip', 'attributes.json')
    name_attr_dict = defaultdict(Counter)
    for cluster in attributes_file:
        for attribute_set in cluster['attributes']:
            for name in attribute_set['object_names']:
                name = name.lower().strip()
                attributes = [a.lower().strip() for a in attribute_set['attributes']]
                name_attr_dict[name].update(attributes)
    return name_attr_dict

def select_attributes(attribute_dict, object_names):
    "Select attributes for all objects in object_names."
    selected_attributes = {a for noun in object_names
                             for a in attribute_dict[noun]}
    return selected_attributes

attribute_dict = get_attribute_dict()
selected_attributes = select_attributes(attribute_dict, GENDERED)

with open('./resources/selected_attributes.txt','w') as f:
    f.write('\n'.join(sorted(selected_attributes)))
