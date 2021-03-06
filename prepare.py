import mlxtend as mlx
from tqdm.notebook import tqdm, trange
from itertools import chain,product
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import json
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import plotly.express as px
import sys
import yaml

from pathlib import Path

params = yaml.safe_load(open('params.yaml'))['prepare']
upper_limit = params['upper_limit']
lower_limit = params['lower_limit']
upper_limit_arules = params['upper_limit_arules']
lower_limit_arules = params['lower_limit_arules']

input_file = Path(sys.argv[1]) #'reddit_scrapper/data/scrapped_data.json'
input_index = Path(sys.argv[2]) #'reddit_scrapper/data/list_of_unique_subreddits.json'
Path('prepared').mkdir(parents=True, exist_ok=True)
Path('target').mkdir(parents=True, exist_ok=True)
data = json.load(open(input_file,'r+'))
subreddit_names_list = json.load(open(input_index,'r+'))
subreddit_index = dict(zip(subreddit_names_list,range(len(subreddit_names_list))))
index_subreddit =  dict(zip(range(len(subreddit_names_list)),subreddit_names_list))

def create_matrix(data,matrix_width,subreddit_index):
    """ Creates matrix filled with zeros and iterates over it filling the cells based on 
        the subreddit-index dictionary"""
    matrix = np.zeros(shape=(len(data),matrix_width))
    for idx,redditor in enumerate(data.values()):
        for key,value in redditor.items():
            matrix[idx,subreddit_index[key]] = value
    return matrix
def filter_matrix(matrix,threshold,indexsubreddit):
    mask = np.where(matrix>threshold,True,False)
    rows = ~np.all(mask==False,axis=1)
    columns = ~np.all(mask==False,axis=0)
    del mask
    data = matrix[np.ix_(rows,columns)]
    del rows
    df = pd.DataFrame(data,columns=np.squeeze(np.argwhere(columns)))
    del data,columns
    df.rename(columns=index_subreddit,inplace=True)
    return df
def extract_most_popular_subreddits(df,lower_limit,upper_limit,clear_zero_rows=True):
    most_popular_reddits = df.sum(axis=0).sort_values(ascending=False)[lower_limit:upper_limit].index
    column_base_order = dict(zip(df.columns,range(len(df.columns))))
    column_indexes = [column_base_order[i] for i in most_popular_reddits]
    X_np = df.to_numpy()[:, column_indexes]
    del df,column_base_order,column_indexes
    zero_rows = np.where(X_np.sum(axis=1) == 0)[0]
    X_np= np.delete(X_np, zero_rows, axis=0)
    if clear_zero_rows:
        return pd.DataFrame(X_np,columns=most_popular_reddits).drop_duplicates()
    else:
        return pd.DataFrame(df,columns=most_popular_reddits).drop_duplicates()


matrix = create_matrix(data,len(subreddit_names_list),subreddit_index)
df = filter_matrix(matrix,5,index_subreddit)
del matrix
df.rename(columns=index_subreddit,inplace=True)
most_popular_reddits = df.sum(axis=0).sort_values(ascending=False)[lower_limit_arules:upper_limit_arules].index
df_bool = df.loc[:,most_popular_reddits].astype(bool).astype(int)
df = extract_most_popular_subreddits(df,lower_limit,upper_limit)
print(df.shape)
df.to_csv('prepared/matrix.csv', index=False)
print("Almost done...")
print(df_bool.shape)
df_bool.to_csv('prepared/matrix_bool.csv', index=False)