import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def displayId_to_userId(displayId):
    return displayId+1

def userId_to_cluster(userId):
    return np.random.randint(20)

def addId_to_cluster(adId):
    return np.random.randint(10)

def userCluster_addCluster_matrix(userCluster,adCluster):
    return np.random.randint(10,size=len(adCluster))

def get_rank_array(array,keys):
    array2 = array[:]
    array2.sort(reverse=True)
    result = {}
    for i in range(len(array)):
        result[str(array2[i])] = i+1
    return result

def rank_simple(vector):
    return sorted(range(len(vector)), key=vector.__getitem__)

test_df = pd.read_csv('../click_test.csv')
test_df['adIdCluster'] = test_df['adId'].map(addId_to_cluster)
num_of_slots = test_df.groupby(['displayId']).apply(lambda f: len(f['displayId']))
ads_df = test_df.groupby(['displayId'])['adIdCluster'].apply(lambda group_series: group_series.tolist()).reset_index(name="adsCluster")
ads_df2 = test_df.groupby(['displayId'])['adId'].apply(lambda group_series: group_series.tolist()).reset_index(name="ads")
ads_df = ads_df.merge(ads_df2)
ads_df['userCluster'] = ads_df['displayId'].map(displayId_to_userId).map(userId_to_cluster)
ads_df['adsPoints'] = ads_df.apply(lambda x: userCluster_addCluster_matrix(userCluster = x['userCluster'], adCluster = x['adsCluster']), axis=1)
print(ads_df.head())

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
result_df.to_csv('results2.csv',header=None, index=False)