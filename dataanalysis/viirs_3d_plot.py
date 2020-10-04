# -*- coding: utf-8 -*-
"""VIIRS_3D_plot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UlSHDGwzRXxhNHWyDf2aMgv5cwwOxwtG
"""

import pandas as pd

df = pd.read_csv("~/Downloads/NASA_spaceapps_challenge/active_fire_data/fire_archive_V1_157508.csv")

df.head(5)

data_cols = ['latitude','longitude','bright_ti4','acq_time']
df[data_cols[1]].head(10000).shape

from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d')

zdata = df[data_cols[3]].head(10000)
xdata = (np.array(df[data_cols[0]].head(10000).max() * np.ones(10000)) - np.array(df[data_cols[0]].head(10000)))/(df[data_cols[0]].head(10000).max() - df[data_cols[0]].head(10000).min())
ydata = (np.array(df[data_cols[1]].head(10000).max() * np.ones(10000)) - np.array(df[data_cols[1]].head(10000)))/(df[data_cols[1]].head(10000).max() - df[data_cols[1]].head(10000).min())
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');

