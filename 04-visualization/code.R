library(tidyverse)

# Load iris dataset
df <- iris

# 1st plot: Iris sepal dimensions colored by petal length
ggplot(df, aes(x = Sepal.Length, y = Sepal.Width, color = Petal.Length)) +
  geom_point() +
  labs(
    x = "sepal length (cm)",
    y = "sepal width (cm)",
    color = "petal length (cm)"
  )

# 2nd plot: hp vs mpg colored by cyl (continuous color scale)
ggplot(mtcars, aes(x = hp, y = mpg, color = cyl)) +
  geom_point()

# 3rd plot: hp vs mpg with cyl as categorical
ggplot(mtcars, aes(x = hp, y = mpg, color = factor(cyl))) +
  geom_point() +
  labs(color = "cyl")
