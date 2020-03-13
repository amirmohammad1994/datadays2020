import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer

users = {-1}

def displayId_to_userId(displayId):
    return display_to_user[displayId]

def userId_to_cluster(userId):
    if (userId in user_to_cluster):
        return user_to_cluster[userId]
    else:
        users.add(userId)
        return 28
def addId_to_cluster(adId):
    if (adId in ad_to_cluster):
        return ad_to_cluster[adId]
    else:
        return 120

events_df = pd.read_csv('../event.csv',skipinitialspace=True, usecols=["displayId","userId"])
display_to_user = dict(zip(events_df.displayId, events_df.userId))

user_clusters_df = pd.read_csv('../user_cluster.csv')
user_to_cluster = dict(zip(user_clusters_df.userId, user_clusters_df.Cluster))

ad_clusters_df = pd.read_csv('../ad_cluster.csv')
ad_to_cluster = dict(zip(ad_clusters_df.adId, ad_clusters_df.Cluster))

click_train_df = pd.read_csv('../click_train.csv')
click_train_df = click_train_df[click_train_df['clicked']==1]
#print(click_train_df.head())
click_train_df['adCluster'] = click_train_df['adId'].map(addId_to_cluster)
click_train_df['userCluster'] = click_train_df['displayId'].map(displayId_to_userId).map(userId_to_cluster)
#print(click_train_df.head())
matrix = pd.crosstab(click_train_df['userCluster'],click_train_df['adCluster'])
print(matrix.head())
print(matrix.info())
#print(users)
matrix.to_csv('../view_cluster.csv')