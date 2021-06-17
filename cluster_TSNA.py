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
import pickle

params = yaml.safe_load(open('params.yaml'))['cluster_TSNA']
n_components = params['n_components']
n_jobs = params['n_jobs']
random_state = params['random_state']

input_file = sys.argv[1]
#Path(output_dir).mkdir(exist_ok=True)
df = pd.read_csv(input_file, sep=',')
df = df.iloc[:-3,:]
tsne =  TSNE(n_components=n_components,n_jobs=n_jobs,random_state=random_state)
#X_tsne = tsne.fit_transform(df)
X_tsne = pd.read_csv('X_tsneL=3U=2000.csv')
X_tsne.drop(columns=['Unnamed: 0'],inplace=True)

clustering = DBSCAN(eps=2, min_samples=8,n_jobs=-1).fit(X_tsne)
X_tsne = pd.DataFrame(X_tsne,columns=['component1','component2','component3'])
X_tsne['clustering'] = clustering.labels_
X_tsne['clustering'] = X_tsne['clustering'].astype(str)
X_tsne = X_tsne[X_tsne['clustering'] !='-1']

clustered_useres_dicts = {}
print(df.shape, X_tsne.shape)
df.loc[:,'clustering'] = clustering.labels_
clustered_users = df.groupby(by=df['clustering']).sum()
clustered_users_matrix = clustered_users.to_numpy().astype(int)
for i in range(clustered_users.to_numpy().shape[0]):
    mask = np.where(clustered_users_matrix[i,:] >0,True,False)
    clustered_useres_dicts[clustered_users.iloc[i].name] = \
    dict(zip(clustered_users.columns[mask],clustered_users_matrix[i,:][mask]))

#for i in clustered_useres_dicts:
#    x = clustered_useres_dicts[i]
#    print(sorted(x.items(),key=lambda item: item[1],reverse=True)[:5])

clustered_useres_dicts[df.loc[5,"clustering"]]
outfile = open('target/tsna.pkl','wb')
pickle.dump(X_tsne,outfile)
outfile.close()

clustered_users.to_csv('target/clustered_users.csv')
