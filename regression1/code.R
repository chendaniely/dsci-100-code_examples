library(tidyverse)
library(tidymodels)

housing <- read_csv("https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv")

set.seed(42)
housing_split <- initial_split(housing, prop = 0.8)
housing_train <- training(housing_split)
housing_test  <- testing(housing_split)

knn_spec <- nearest_neighbor(weight_func = "rectangular", neighbors = tune()) |>
  set_engine("kknn") |>
  set_mode("regression")

# ocean_proximity is categorical — dummy-encode before scaling
housing_recipe <- recipe(median_house_value ~ ., data = housing_train) |>
  step_impute_median(all_numeric_predictors()) |> #  total_bedrooms column has ~200 NAs. Without imputation, kknn silently drops those rows from each fold's data
  step_dummy(all_nominal_predictors()) |>
  step_scale(all_predictors()) |>
  step_center(all_predictors())

housing_wf <- workflow() |>
  add_recipe(housing_recipe) |>
  add_model(knn_spec)

gridvals <- tibble(neighbors = seq(from = 1, to = 19, by = 3))

housing_folds <- vfold_cv(housing_train, v = 5)

gridsearch_results <- housing_wf |>
  tune_grid(resamples = housing_folds, grid = gridvals) |>
  collect_metrics() |>
  filter(.metric == "rmse")

gridsearch_results

# Best K
best_k <- gridsearch_results |>
  filter(mean == min(mean))

best_k

kmin <- best_k |> pull(neighbors)

# Refit with best K and evaluate on test set
knn_spec_final <- nearest_neighbor(weight_func = "rectangular", neighbors = kmin) |>
  set_engine("kknn") |>
  set_mode("regression")

housing_fit <- workflow() |>
  add_recipe(housing_recipe) |>
  add_model(knn_spec_final) |>
  fit(data = housing_train)

rmspe_knn <- housing_fit |>
  predict(housing_test) |>
  bind_cols(housing_test) |>
  metrics(truth = median_house_value, estimate = .pred) |>
  filter(.metric == "rmse") |>
  pull(.estimate)

rmspe_knn
