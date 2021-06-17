import pandas as pd
import sys
import json
import pickle
import yaml
import numpy as np
from pathlib import Path
from sklearn.neighbors import BallTree

params = yaml.safe_load(open('params.yaml'))['scrape_user']
username = params['username']



rules = pd.read_json(sys.argv[1])
f = open(sys.argv[2])
user = json.load(f)
f.close()
#tsna = pd.read_csv(sys.argv[3], sep=',')
#infile = open(sys.argv[4],'rb')
#tsna_model = pickle.load(infile)
#infile.close()
pca_df = pd.read_csv(sys.argv[3], sep=',')
df = pd.read_csv(sys.argv[4], sep=',')
infile = open(sys.argv[5],'rb')
pca = pickle.load(infile)
infile.close()
infile = open(sys.argv[6],'rb')
clustering = pickle.load(infile)
infile.close()


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



user = {username : user}
def reshape_new_user(new_user,df):
    base_dict = dict(zip(df.columns,[0]*df.columns.shape[0]))
    for key,value in list(new_user.values())[0].items():
        if key in base_dict:
            base_dict[key] = value
    base_dict ={list(new_user.keys())[0]:base_dict}
    new_user_df = pd.DataFrame(base_dict).T
    new_user_df = new_user_df[df.columns.to_list()]
    return new_user_df

def get_cluster_index(pca_new_user,pca_df,NN=10):
    tree = BallTree(pca_df.iloc[:,:-1])
    dist, ind = tree.query(pca_new_user,k=NN)
    new_user_cluster = pca_df.iloc[ind[0],pca_df.columns.get_loc("clustering")]\
    .value_counts().sort_values(ascending=False).index[0]
    return int(new_user_cluster)

def get_clustered_subreddits(df,labels):
    clustered_useres_dicts = {}
    df.loc[:,'clustering'] = clustering.labels_
    clustered_users = df.groupby(by=df['clustering']).sum()
    clustered_users_matrix = clustered_users.to_numpy().astype(int)
    for i in range(clustered_users.to_numpy().shape[0]):
        mask = np.where(clustered_users_matrix[i,:] >0,True,False)
        clustered_useres_dicts[clustered_users.iloc[i].name] = \
        dict(zip(clustered_users.columns[mask],clustered_users_matrix[i,:][mask]))
    df.drop(columns=['clustering'],inplace=True)
    return clustered_useres_dicts

new_user_df = reshape_new_user(user,df)
pca_new_user = pca.transform(new_user_df)
new_user_cluster_index = get_cluster_index(pca_new_user,pca_df)
clustered_useres_dicts = get_clustered_subreddits(df,clustering.labels_)
user_cluster = clustered_useres_dicts[new_user_cluster_index]
user_cluster = {i[0]:i[1] for i in user_cluster.items() if i[0] not in list(user.values())[0].keys()}
print(new_user_cluster_index,user,pd.Series(user_cluster).sort_values(ascending=False).head(20))

