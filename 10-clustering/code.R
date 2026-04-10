library(tidyverse)
library(tidymodels)
library(tidyclust)

# Use built-in iris dataset with cleaned column names
iris_data <- iris |>
  rename(
    sepal_length = Sepal.Length,
    sepal_width = Sepal.Width,
    petal_length = Petal.Length,
    petal_width = Petal.Width,
    species = Species
  )
iris_data

# example 1 -----
# run k-means on 2 variables with standardization

recipe1 <- recipe(~ sepal_length + sepal_width, data = iris_data) |>
  step_scale(all_predictors()) |>
  step_center(all_predictors())

kmeans_spec <- k_means(num_clusters = 3) |>
  set_engine("stats", nstart = 10)

clust1 <- workflow() |>
  add_recipe(recipe1) |>
  add_model(kmeans_spec) |>
  fit(data = iris_data)

iris_clustered1 <- clust1 |>
  augment(iris_data)
iris_clustered1

iris_clustered1 |>
  count(species, .pred_cluster)

## elbow plot (not required, shown for completeness)
elbow_results <- map_dfr(1:10, \(k) {
  wf <- workflow() |>
    add_recipe(recipe1) |>
    add_model(k_means(num_clusters = k) |> set_engine("stats", nstart = 10)) |>
    fit(data = iris_data)
  tibble(num_clusters = k, mean = extract_fit_engine(wf)$tot.withinss)
})

ggplot(elbow_results, aes(x = num_clusters, y = mean)) +
  geom_line() +
  geom_point() +
  labs(
    x = "Number of Clusters (k)",
    y = "Total Within-Cluster Sum of Squares",
    title = "Elbow Plot for K-Means Clustering"
  )

#

# example 2 -----
# run k-means including species (categorical variable)
# you are not responsible for dummy variable encoding

recipe2 <- recipe(~ sepal_length + sepal_width + species, data = iris_data) |>
  step_dummy(species) |>
  step_scale(all_predictors()) |>
  step_center(all_predictors())

clust2 <- workflow() |>
  add_recipe(recipe2) |>
  add_model(kmeans_spec) |>
  fit(data = iris_data)

iris_clustered2 <- clust2 |>
  augment(iris_data)
iris_clustered2

iris_clustered2 |>
  count(species, .pred_cluster)

# example 3 -----
# run k-means on all numeric variables with standardization

recipe3 <- recipe(
  ~ sepal_length + sepal_width + petal_length + petal_width,
  data = iris_data
) |>
  step_scale(all_predictors()) |>
  step_center(all_predictors())

clust3 <- workflow() |>
  add_recipe(recipe3) |>
  add_model(kmeans_spec) |>
  fit(data = iris_data)

iris_clustered3 <- clust3 |>
  augment(iris_data)
iris_clustered3

iris_clustered3 |>
  count(species, .pred_cluster)
