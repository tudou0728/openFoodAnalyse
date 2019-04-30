import algoDis
import dataCenter
import dataViz
import pandas as pd
import numpy as np
import multiprocessing
import math
import time
import plotly as py
import plotly.graph_objs as go

class CleanBrand:
    def saveBrands(self):
        # test专用
        file = 'D:\\pycharm_workspace\\projetLibre\\fr.openfoodfacts.org.products.csv'
        df = pd.DataFrame()
        with open(file)as f:
            chunk_iter = pd.read_csv(file, sep='\t', iterator=True, chunksize=100000, low_memory=False,
                                     usecols=['brands'])  # error_bad_lines=False low_memory=False ,nrows=100
            # chunk_iter = pd.read_csv(file, sep=',', iterator=True, chunksize=100000)
            for chunk in chunk_iter:
                df = pd.concat([df, chunk])
        df.to_csv('brands.csv', sep='\t', encoding='utf-8', header='brandsClean', index=False)

    def getBrandsClean(self):
        # test专用
        file='brandsClean1.csv'
        df = pd.DataFrame()
        with open(file)as f:
            chunk_iter = pd.read_csv(file, sep='\t', iterator=True, chunksize=100000, low_memory=False,usecols=['brand1'],encoding='utf-8')# error_bad_lines=False low_memory=False ,nrows=100
            # chunk_iter = pd.read_csv(file, sep=',', iterator=True, chunksize=100000)
            for chunk in chunk_iter:
                df = pd.concat([df, chunk])

        # 正式的程序
        # df['brand'].unique().info()
        df.info()
        return df