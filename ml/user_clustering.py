# ml/user_clustering.py

import pandas as pd
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from collections import defaultdict

model = SentenceTransformer('all-MiniLM-L6-v2')  # fast, 384-dim vectors

def get_user_embeddings(df, min_messages=10, max_users=10):
    user_msgs = df.groupby('user')['message'].apply(lambda x: ' '.join(x.dropna()))
    user_msgs = user_msgs[user_msgs.str.strip().astype(bool)]
    if len(user_msgs) > max_users:
        user_msgs = user_msgs.sample(max_users, random_state=42)

    embeddings = model.encode(user_msgs.tolist())
    return user_msgs.index.tolist(), embeddings

def cluster_users(df, num_clusters=3):
    users, embeddings = get_user_embeddings(df)
    if len(users) < num_clusters:
        return None, None, None

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    cluster_map = defaultdict(list)
    for user, label in zip(users, labels):
        cluster_map[f"Cluster {label+1}"].append(user)

    return users, labels, cluster_map
