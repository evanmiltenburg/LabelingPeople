def load_lexical_items(filename):
    "Load lexical items from a file."
    lexical_items = []
    with open(filename) as f:
        for line in f:
            tokens = line.strip().split()
            quoted_tokens = ["'{}'".format(token) for token in tokens]
            spaced_tokens = ' '.join(quoted_tokens)
            lexical_items.append(spaced_tokens)
    return lexical_items


def create_lexical_rule(category_name, lexical_items):
    "Generate rule."
    rule = category_name + ' -> ' + ' | '.join(lexical_items)
    return rule


def extend_grammar(grammar, category_name, filename, additional_rules=None):
    "Extend a grammar."
    # Initialize grammar as list of rules.
    new_grammar = []
    new_grammar.extend(grammar)
    
    # Add category-specific rules.
    if additional_rules:
        new_grammar.extend(additional_rules)
    
    # Add lexical items.
    lexical_items = load_lexical_items(filename)
    lexical_rule = create_lexical_rule(category_name, lexical_items)
    new_grammar.append(lexical_rule)
    
    return new_grammar


def write_grammar(grammar):
    "Write the grammar to a file."
    with open('labelgrammar.cfg','w') as f:
        lines = [line + '\n' for line in grammar]
        f.writelines(lines)

numbers = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety one-hundred".split()
numbers.extend(map(str,range(100)))
numbers += ['mainly', 'mostly', 'several', 'roughly', "at' 'least", 'around','all']
number_rule = "Number -> " + ' | '.join("'{}'".format(n) for n in numbers)

my_grammar = ["S -> Gendered",
                "S -> Gendered Conj Gendered",
                "S -> Gendered Gendered",
                "Gendered -> Number Gendered",
                "Gendered -> Mod Gendered",
                "Gendered -> Mod Mod Gendered",
                "Gendered -> Mod Mod Mod Gendered",
                "Gendered -> Det Gendered",
                "Gendered -> Contrast Gendered",
                "Contrast -> 'other'",
                "Det -> 'a' | 'an' | 'the'",
                "Mod -> Mod Conj Mod",
                "Conj -> 'or' | 'and'",
                "Gendered -> 'man' | 'men' | 'woman' | 'women' | 'boy' | 'boys' | 'girl' | 'girls' | 'male' | 'males' | 'female' | 'females'",
                number_rule,
                "Consist -> 'of'"]

external_data = [('Ability', './resources/Categories/ability.txt', ["Mod -> Ability"]),
                 
                 ('Activity', './resources/Categories/activity.txt', ["Mod -> Activity"]),
                 
                 ('Age', './resources/Categories/age.txt', ["Mod -> Age"]),
                 
                 ('AmountOfClothing', './resources/Categories/amount-of-clothing.txt', ["Mod -> AmountOfClothing"]),
                 
                 ('Attractiveness', './resources/Categories/attractiveness.txt', ["Mod -> Attractiveness"]),
                 
                 ('Build', './resources/Categories/build.txt', ["Mod -> Build"]),
                 
                 ('Cleanliness', './resources/Categories/cleanliness.txt', ["Mod -> Cleanliness"]),
                 
                 ('ColorOfClothing', './resources/Categories/color-of-clothing.txt', ["Mod -> ColorOfClothing"]),
                 
                 ('Ethnicity', './resources/Categories/ethnicity.txt', ["Mod -> Ethnicity"]),
                 
                 ('Eyes', './resources/Categories/eyes.txt', ["Mod -> Eyes"]),
                 
                 ('Group', './resources/Categories/group.txt', ["S -> Group S", "S -> Group Consist S"]),
                 
                 ('FamilyRelation', './resources/Categories/familyrelation.txt', ["Mod -> FamilyRelation"]),
                 
                 ('FacialHair', './resources/Categories/facial-hair.txt', ["Mod -> FacialHair"]),
                 
                 ('Fitness', './resources/Categories/fitness.txt', ["Mod -> Fitness"]),
                 
                 ('HairColor', './resources/Categories/hair-color.txt', ["Mod -> HairColor"]),
                 
                 ('HairLength', './resources/Categories/hair-length.txt', ["Mod -> HairLength"]),
                 
                 ('HairStyle', './resources/Categories/hair-style.txt', ["Mod -> HairStyle"]),
                 
                 ('Height', './resources/Categories/height.txt', ["Mod -> Height"]),
                 
                 ('Identity', './resources/Categories/identity.txt', ["Mod -> Identity"]),
                 
                 ('Judgment', './resources/Categories/judgment.txt', ["Mod -> Judgment"]),
                 
                 ('KindOfClothing', './resources/Categories/kind-of-clothing.txt', ["Mod -> KindOfClothing"]),
                 
                 ('Mood', './resources/Categories/mood.txt', ["Mod -> Mood"]),
                 
                 ('Number', './resources/Categories/number.txt', ["Mod -> Number"]),
                 
                 ('OccupationSocGroup', './resources/Categories/occupation-or-social-group.txt', ["Mod -> OccupationSocGroup"]),
                 
                 ('Religion', './resources/Categories/religion.txt', ["Mod -> Religion"]),
                 
                 ('SkinColor', './resources/Categories/skin-color.txt', ["Mod -> SkinColor"]),
                 
                 ('SkinOther', './resources/Categories/skin-other.txt', ["Mod -> SkinOther"]),
                 
                 ('State', './resources/Categories/state.txt', ["Mod -> State"]),
                 
                 ('Weight', './resources/Categories/weight.txt', ["Mod -> Weight"]),
                 ]

for category, filename, rules in external_data:
    my_grammar = extend_grammar(my_grammar, category, filename, rules)




write_grammar(my_grammar)
