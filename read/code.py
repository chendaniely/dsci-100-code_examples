## DO NOT RUN
import os

os.chdir("read/")
##


import pandas as pd

pd.read_csv("data/data1.csv")

pd.read_csv("data-meta/data2.csv")
pd.read_csv("data-meta/data2.csv", skiprows=5)


pd.read_csv("data-meta-delim/data3.csv", skiprows=5)
pd.read_csv("data-meta-delim/data3.csv", skiprows=5, delimiter="$")
