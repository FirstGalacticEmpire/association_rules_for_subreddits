import json
import numpy as np
import pandas as pd
import plotly.express as px
import mlxtend as mlx
from tqdm.notebook import tqdm, trange
from itertools import chain
import time
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import yaml
import sys
from pathlib import Path

params = yaml.safe_load(open('params.yaml'))['generate_association_rules_final']
min_support = params['min_support']
input_path = sys.argv[1]
#Path(output_dir).mkdir(exist_ok=True)

df_bool = pd.read_csv(input_path, sep=',')
frequent_itemsets = apriori(df_bool, min_support=min_support,
                            use_colnames=True, low_memory=True,
                            verbose=2, max_len=7)
rules = association_rules(frequent_itemsets,
                  metric='lift',
                  min_threshold=1.01)
del frequent_itemsets
rules.to_json("target/arules-10000-00035.json")
del rules



#frequent_itemsets = apriori(df_bool, min_support=min_support, use_colnames=True)
#rules = association_rules(frequent_itemsets,
#                  metric='confidence',
#                  min_threshold=0.7)
#
#rules.to_json(output_dir + "arules.json")