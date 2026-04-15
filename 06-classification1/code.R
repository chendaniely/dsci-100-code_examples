library(tidyverse)
library(tidymodels)

# Load wine dataset
wine <- read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data",
  col_names = c(
    "target", "alcohol", "malic_acid", "ash", "alcalinity_of_ash",
    "magnesium", "total_phenols", "flavanoids", "nonflavanoid_phenols",
    "proanthocyanins", "color_intensity", "hue",
    "od280_od315_of_diluted_wines", "proline"
  )
) |>
  mutate(target = as_factor(target))

wine

# --- Train/test split ---
set.seed(42)
wine_split <- initial_split(wine, prop = 0.8, strata = target)
wine_train <- training(wine_split)
wine_test  <- testing(wine_split)

knn_spec <- nearest_neighbor(neighbors = 5) |>
  set_engine("kknn") |>
  set_mode("classification")

# --- KNN without preprocessing (wrong: fitting on all data, no scaling) ---
wine_recipe_no_scaling <- recipe(target ~ ., data = wine_train)

# This is wrong: we fit on ALL data instead of only training data
knn_fit_wrong <- workflow() |>
  add_recipe(wine_recipe_no_scaling) |>
  add_model(knn_spec) |>
  fit(data = wine)  # should be wine_train, not wine
knn_fit_wrong

predict(knn_fit_wrong, wine_test) |>
  bind_cols(wine_test) |>
  metrics(truth = target, estimate = .pred_class) |>
  filter(.metric == "accuracy")

# --- KNN with preprocessing (correct: scaling + fit on training data only) ---
wine_recipe <- recipe(target ~ ., data = wine_train) |>
  step_center(all_numeric_predictors()) |>
  step_scale(all_numeric_predictors())

knn_pipeline <- workflow() |>
  add_recipe(wine_recipe) |>
  add_model(knn_spec)

knn_pipeline_fit <- knn_pipeline |>
  fit(data = wine_train)

knn_pipeline_fit

# Predictions on train and test
predict(knn_pipeline_fit, wine_train)
predict(knn_pipeline_fit, wine_test)

# Accuracy on test set
knn_pipeline_fit |>
  predict(wine_test) |>
  bind_cols(wine_test) |>
  metrics(truth = target, estimate = .pred_class) |>
  filter(.metric == "accuracy")