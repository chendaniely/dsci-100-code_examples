library(tidyverse)

read_csv('data/data1.csv')

# read_csv('02-read/data/data1.csv')

# read_csv("/Users/dan/git/hub/dsci-100-code_examples/02-read/data/data1.csv")

read_csv('data-meta/data2.csv')

read_csv('data-meta/data2.csv', skip = 6)

read_delim('data-meta-delim/data3.csv', skip = 6)

read_delim('data-meta-delim/data3.csv', skip = 6, delim = '$')

read_delim('data3-same.csv', skip = 6, delim = '$')

