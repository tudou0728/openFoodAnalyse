import algoDis
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import math


# classe pour integrer
class DataCenter:
    algoDis = algoDis.AlgoDis()

    def cleanData(self, dataFrame, cols):
        df = dataFrame[cols]
        return df

    def selectData(self, dataFrame):
        pass

    def selectPOIs(self, df, n):
        data = self.convertDataSet(df)
        estimator = KMeans(n_clusters=n, n_jobs=n)
        estimator.fit(data)  # 聚类
        label_pred = estimator.labels_  # 获取聚类标签
        centroids = estimator.cluster_centers_  # 获取聚类中心
        inertia = estimator.inertia_  # 获取聚类准则的总和
        closest, _ = pairwise_distances_argmin_min(centroids, data)
        pois_df = pd.DataFrame()
        for i in closest:
            df_temp = pd.DataFrame([df.iloc[i]])
            pois_df = pd.concat([pois_df, df_temp], axis=0)
        return closest, pois_df

    def convertDataSet(self, df):
        num_df = pd.DataFrame()
        for index, row in df.iterrows():
            data_num = self.algoDis.selectNumeric(row.values)
            two_gram = self.algoDis.selectStr(row)
            data = np.append(data_num, two_gram)
            # data = np.nan_to_num(data)
            df_temp = pd.DataFrame([data])
            num_df = pd.concat([num_df, df_temp], axis=0)
            num_df = num_df.fillna(0)
        return num_df

    def selectPOIsRandom(self, num_POIs, df):
        pois_df = pd.DataFrame()
        POIs = np.random.randint(0, len(df) - 1, size=num_POIs)
        for i in POIs:
            df_temp = pd.DataFrame([df.iloc[i]])
            pois_df = pd.concat([pois_df, df_temp], axis=0)
        return POIs, pois_df

    def dividedf(self, df, n):
        num = math.ceil(len(df) / n)
        for i in range(num):
            start = i * n
            end = (i + 1) * n if ((i + 1) * n) < len(df) else len(df) - 1
            yield df.iloc[start:end]

