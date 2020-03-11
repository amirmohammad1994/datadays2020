import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer

user_ad_clicks = pd.read_csv("../user_ad_clicks.csv")
ads = user_ad_clicks.adId.unique()
users =  user_ad_clicks.userId.unique()
user_ad_matrix = pd.crosstab(user_ad_clicks['userId'],user_ad_clicks['adId'])
df = pd.read_csv('../click_train.csv')
