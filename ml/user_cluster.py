import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def extract_user_features(df):
    # Remove system messages
    temp = df[df['user'] != 'group_notification'].copy()

    # Basic message stats
    user_stats = temp.groupby('user').agg(
        total_messages=('message', 'count'),
        avg_msg_length=('message', lambda x: x.dropna().apply(lambda m: len(m.split())).mean()),
        emoji_usage=('message', lambda x: x.dropna().apply(lambda m: sum(1 for c in m if c in '😀😃😄😁😆😅😂🤣😊😍😘😜👍❤️🔥💯')).sum())
    ).fillna(0)

    # Sentiment distribution
    sentiment_dummies = pd.get_dummies(temp[['user', 'sentiment']], columns=['sentiment'])
    sentiment_dist = sentiment_dummies.groupby('user').sum()
    sentiment_dist.columns = sentiment_dist.columns.str.replace("sentiment_", "")

    # Message types
    if 'message_type' in temp.columns:
        msgtype_dummies = pd.get_dummies(temp[['user', 'message_type']], columns=['message_type'])
        msgtype_dist = msgtype_dummies.groupby('user').sum()
        msgtype_dist.columns = msgtype_dist.columns.str.replace("message_type_", "")
    else:
        msgtype_dist = pd.DataFrame(index=user_stats.index)

    # Merge all features
    user_features = user_stats.join([sentiment_dist, msgtype_dist], how='outer').fillna(0)

    return user_features

def cluster_users(user_features, n_clusters=3):
    # Scale features
    scaler = StandardScaler()
    scaled = scaler.fit_transform(user_features)

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    user_features['cluster'] = kmeans.fit_predict(scaled)

    # For visualization: use PCA to reduce to 2D
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(scaled)
    user_features['pca1'] = reduced[:, 0]
    user_features['pca2'] = reduced[:, 1]

    return user_features
