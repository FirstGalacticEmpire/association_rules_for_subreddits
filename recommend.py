import pandas as pd
import sys
import json
import pickle
import yaml
from pathlib import Path

user = None



rules = pd.read_json(sys.argv[1])
user = json.load(sys.argv[2])
tsna = pd.read_csv(sys.argv[3], sep=',')
infile = open(sys.argv[4],'rb')
tsna_model = pickle.load(infile)
infile.close()
pca = pd.read_csv(sys.argv[5], sep=',')

rules["antecedents"] = rules["antecedents"].apply(lambda x: frozenset(x))
rules["consequents"] = rules["consequents"].apply(lambda x: frozenset(x))

def get_rules(set_of_subreddits, top_n=100):
    antecedents_rule =  rules['antecedents'].apply(lambda x: set_of_subreddits.issuperset(x))
    new_rules =  rules[antecedents_rule].copy()
#     new_rules["Coefficient"] = new_rules["confidence"] + new_rules["support"]
    new_rules["Coefficient"] = new_rules["lift"]
#     new_rules["Coefficient"] = new_rules["confidence"] - new_rules["support"] + new_rules["lift"] + new_rules["leverage"]+ new_rules["conviction"]
#     new_rules["consequents"] = new_rules["consequents"].apply(lambda x: x - set_of_subreddits - OBVIOUS_SUBREDDITS)
    new_rules["consequents"] = new_rules["consequents"].apply(lambda x: x - set_of_subreddits)
    new_rules = new_rules[new_rules["consequents"].apply(lambda x: len(x) > 0)]
    if len(new_rules) == 0:
        return []
    new_rules = new_rules[['consequents', "Coefficient"]]
    new_rules = new_rules.explode("consequents")
    new_rules["consequents"] = new_rules["consequents"].apply(lambda x:list(x)[0])
    new_rules = new_rules.groupby("consequents")["Coefficient"].max().reset_index()
    return list(new_rules.nlargest(top_n, "Coefficient")["consequents"])


sub_red = {k for k,v in user.items()}
print("User likes:", sub_red)
print("User should like:",get_rules(sub_red,10))

user2 = {'user' : user}