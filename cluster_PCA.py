from sklearn.decomposition import PCA
from sklearn.neighbors import BallTree
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import pickle
import sys
import yaml
from pathlib import Path

params = yaml.safe_load(open('params.yaml'))['cluster_PCA']
n_components = params['n_components']
n_clusters = params['n_clusters']
input_file = sys.argv[1]
Path('target').mkdir(exist_ok=True)
df = pd.read_csv(input_file, sep=',')

pca = PCA(n_components=n_components).fit(df)
pca_df = pd.DataFrame(pca.transform(df))

pca_df['clustering'] = None
clustering = KMeans(n_clusters=n_clusters).fit(pca_df.iloc[:,:-1])
pca_df['clustering'] = clustering.labels_
pca_df['clustering'] = pca_df['clustering'].astype(str)

pca_df.to_csv('target/pca.csv', index=False)

outfile = open('target/pca.pkl','wb')
pickle.dump(pca,outfile)
outfile.close()
outfile = open('target/clustering.pkl','wb')
pickle.dump(clustering,outfile)
outfile.close()