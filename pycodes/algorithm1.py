import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def displayId_to_userId(displayId):
    return display_to_user[displayId]

def userId_to_cluster(userId):
    if (userId in user_to_cluster):
        return user_to_cluster[userId]
    else:
        return 28
def addId_to_cluster(adId):
    if (adId in ad_to_cluster):
        return ad_to_cluster[adId]
    else:
        return 120


def userCluster_addCluster_matrix(userCluster,adCluster):
    result = np.random.randint(10,size=len(adCluster))
    for i in range(len(adCluster)):
        try:
            result[i] = view_df[str(adCluster[i])][userCluster]
        except KeyError:
            result[i] = np.random.randint(1000)
    return result

def get_rank_array(array,keys):
    array2 = array[:]
    array2.sort(reverse=True)
    result = {}
    for i in range(len(array)):
        result[str(array2[i])] = i+1
    return result

def rank_simple(vector):
    return sorted(range(len(vector)), reverse=True,key=vector.__getitem__)

events_df = pd.read_csv('../event.csv',skipinitialspace=True, usecols=["displayId","userId"])
display_to_user = dict(zip(events_df.displayId, events_df.userId))

user_clusters_df = pd.read_csv('../user_cluster.csv')
user_to_cluster = dict(zip(user_clusters_df.userId, user_clusters_df.Cluster))

ad_clusters_df = pd.read_csv('../ad_cluster.csv')
ad_to_cluster = dict(zip(ad_clusters_df.adId, ad_clusters_df.Cluster))

view_df = pd.read_csv('../view_cluster.csv')

test_df = pd.read_csv('../click_test.csv')
test_df['adIdCluster'] = test_df['adId'].map(addId_to_cluster)
num_of_slots = test_df.groupby(['displayId']).apply(lambda f: len(f['displayId']))
ads_df = test_df.groupby(['displayId'])['adIdCluster'].apply(lambda group_series: group_series.tolist()).reset_index(name="adsCluster")
ads_df2 = test_df.groupby(['displayId'])['adId'].apply(lambda group_series: group_series.tolist()).reset_index(name="ads")
ads_df = ads_df.merge(ads_df2)
ads_df['userCluster'] = ads_df['displayId'].map(displayId_to_userId).map(userId_to_cluster)
ads_df['adsPoints'] = ads_df.apply(lambda x: userCluster_addCluster_matrix(userCluster = x['userCluster'], adCluster = x['adsCluster']), axis=1)
print(ads_df.head())
print(ads_df[2:][:].head())
print(view_df.head())
result_adId = []
result_displayId = []
result_rank = []
for idx,row in ads_df.iterrows():
    ranks = rank_simple(row['adsPoints'].tolist())
    for i in range(len(row['ads'])):
        result_adId.append(row['ads'][i])
        result_displayId.append(row['displayId'])
        result_rank.append(ranks[i]+1)

result_df = pd.DataFrame({"displayId" : result_displayId, "adId" : result_adId , "rank": result_rank})
print(result_df.head())
result_df.to_csv('results2.csv',header=None, index=False)
