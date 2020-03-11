import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

click_train_data = pd.read_csv('../click_train.csv')
event_data = pd.read_csv('../event.csv',skipinitialspace=True, usecols=["displayId","userId"])
# user-add
df = click_train_data.merge(event_data,left_on="displayId",right_on="displayId")
df = df[df['clicked'] == 1]
df = df[['userId','adId']]
df.to_csv("../user_ad_clicks.csv",index=False)
