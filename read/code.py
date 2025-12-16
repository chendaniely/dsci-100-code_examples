## DO NOT RUN
import os

# os.chdir("read/")
##


import pandas as pd

pd.read_csv("data/data1.csv")

pd.read_csv("data-meta/data2.csv")
pd.read_csv("data-meta/data2.csv", skiprows=5)
pd.read_csv("data-meta/data2.csv", skiprows=6)
pd.read_csv("data-meta/data2.csv", skiprows=7)

pd.read_csv("data-meta-delim/data3.csv", skiprows=5)
pd.read_csv("data-meta-delim/data3.csv", skiprows=5, delimiter="$")
pd.read_csv("data-meta-delim/data3.csv", skiprows=5, sep="$")

pd.read_csv("data/data1.csv", skiprows=0, sep=",")
pd.read_csv("data3-same.csv", skiprows=5, sep="$")
