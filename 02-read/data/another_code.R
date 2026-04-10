# run this code assuming you are in the data folder
# as the working directory

library(tidyverse)

read_csv("data1.csv")

# the . is a shortcut for current working directory
read_csv("./data1.csv")

# the .. means previous directory
read_csv('../data-meta/data2.csv', skip = 6)
