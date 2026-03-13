library(tidyverse)

# Load iris dataset
df <- iris


ggplot(df, mapping = aes(x = Sepal.Length)) +
  geom_histogram()

ggplot(df, mapping = aes(x = Sepal.Length)) +
  geom_boxplot()

ggplot(df, aes(x=Species)) + geom_bar()

ggplot(df, mapping = aes(x = Sepal.Length)) +
  geom_bar()

# 1st plot: Iris sepal dimensions colored by petal length
ggplot(df, aes(x = Sepal.Length, y = Sepal.Width, color = Petal.Length)) +
  geom_point() +
  labs(
    x = "sepal length (cm)",
    y = "sepal width (cm)",
    color = "petal length (cm)"
  )

ggplot(df, aes(x = Sepal.Length, y = Sepal.Width, color = Species)) +
  geom_point() +
  labs(
    x = "sepal length (cm)",
    y = "sepal width (cm)",
    color = "species"
  )

data(mtcars)
# 2nd plot: hp vs mpg colored by cyl (continuous color scale)
ggplot(mtcars, aes(x = hp, y = mpg, color = cyl)) +
  geom_point()

# 3rd plot: hp vs mpg with cyl as categorical
ggplot(mtcars, aes(x = hp, y = mpg, color = factor(cyl))) +
  geom_point() +
  labs(title = "hello", color = "cyl") +
  theme_minimal()



ggplot(mtcars, aes(x = hp, y = mpg, color = factor(cyl))) +
  geom_point() +
  labs(title = "hello", color = "cyl") +
  theme_minimal() +
  theme(
    panel.grid.major = element_blank(),  # remove major grid lines
    panel.grid.minor = element_blank()   # remove minor grid lines
  )
