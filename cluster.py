from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from itertools import product
import plotly.express as px
from tqdm.notebook import tqdm
import pandas as pd
import numpy as np
import sys
import yaml
from pathlib import Path


params = yaml.safe_load(open('params.yaml'))['featurize']
n_components = params['n_components']
n_jobs = params['n_jobs']
random_state = params['random_state']

input_dir = sys.argv[1]
output_dir = sys.argv[2]

Path(output_dir).mkdir(exist_ok=True)

file = Path(input_dir) / 'matrix.csv'

df = pd.read_csv(file, sep=',')
tsne =  TSNE(n_components=n_components,n_jobs=n_jobs,random_state=random_state)
X_tsne = tsne.fit_transform(df)
clustering = DBSCAN(eps=20, min_samples=3,n_jobs=n_jobs).fit(X_tsne)
X_tsne = pd.DataFrame(X_tsne,columns=['component1','component2','component3'])
X_tsne['clustering'] = clustering.labels_
X_tsne['clustering'] = X_tsne['clustering'].astype(str)

clustered_useres_dicts = {}
df.loc[:,'clustering'] = clustering.labels_
clustered_users = df.groupby(by=df['clustering']).sum()
clustered_users_matrix = clustered_users.to_numpy().astype(int)
for i in range(clustered_users.to_numpy().shape[0]):
    mask = np.where(clustered_users_matrix[i,:] >0,True,False)
    clustered_useres_dicts[clustered_users.iloc[i].name] = \
    dict(zip(clustered_users.columns[mask],clustered_users_matrix[i,:][mask]))

df.drop(columns='clustering',inplace=True)

if n_components == 2:
    X_tsne = pd.DataFrame(X_tsne,columns=['component1','component2'])
    X_tsne['clustering'] = clustering.labels_
    X_tsne['clustering'] = X_tsne['clustering'].astype(str)
    print(f"Number of clusters {pd.unique(X_tsne['clustering']).shape[0]}")
    fig = px.scatter(X_tsne,x="component1", y="component2", color="clustering")
    fig.show()
elif n_components == 3:
    X_tsne = pd.DataFrame(X_tsne,columns=['component1','component2','component3'])
    X_tsne['clustering'] = clustering.labels_
    X_tsne['clustering'] = X_tsne['clustering'].astype(str)
    print(f"Number of clusters {pd.unique(X_tsne['clustering']).shape[0]}")
    fig = px.scatter_3d(X_tsne,x="component1", y="component2",z='component3', color="clustering")
    fig.show()