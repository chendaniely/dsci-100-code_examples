library(tidyverse)
library(tidymodels)

# ---- Load data -------------------------------------------------------------
wine <- read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data",
  col_names = c(
    "target", "alcohol", "malic_acid", "ash", "alcalinity_of_ash",
    "magnesium", "total_phenols", "flavanoids", "nonflavanoid_phenols",
    "proanthocyanins", "color_intensity", "hue",
    "od280_od315_of_diluted_wines", "proline"
  )
) |>
  mutate(target = factor(target))

# ---- Train/test split ------------------------------------------------------
set.seed(42)
wine_split <- initial_split(wine, prop = 0.8)
wine_train <- training(wine_split)
wine_test  <- testing(wine_split)

# ---- Preprocessing recipe --------------------------------------------------
wine_recipe <- recipe(target ~ ., data = wine_train) |>
  step_center(all_numeric_predictors()) |>
  step_scale(all_numeric_predictors())
  #step_normalize(all_numeric_predictors())
  

# ---- Model specification ---------------------------------------------------
knn_spec <- nearest_neighbor(neighbors = tune()) |>
  set_engine("kknn") |>
  set_mode("classification")

# ---- Workflow --------------------------------------------------------------
knn_workflow <- workflow() |>
  add_recipe(wine_recipe) |>
  add_model(knn_spec)

# ---- Grid search (k = 1, 4, 7, 10, 13, 16, 19) -----------------------------
param_grid <- tibble(neighbors = seq(1, 21, by = 3))

wine_folds <- vfold_cv(wine_train, v = 5)

grid_results <- tune_grid(
  knn_workflow,
  resamples = wine_folds,
  grid      = param_grid,
  metrics   = metric_set(accuracy)
)

# ---- Best CV result --------------------------------------------------------
best_k <- grid_results |>
  collect_metrics() |>
  filter(.metric == "accuracy") |>
  arrange(desc(mean)) |>
  head(1) |>
  pull(neighbors)

best_k

# ---- Refit with best K and evaluate on test set ----------------------------
knn_spec_final <- nearest_neighbor(neighbors = best_k) |>
  set_engine("kknn") |>
  set_mode("classification")

final_fit <- workflow() |>
  add_recipe(wine_recipe) |>
  add_model(knn_spec_final) |>
  fit(data = wine_train)

predict(final_fit, wine_test) |>
  bind_cols(wine_test) |>
  metrics(truth = target, estimate = .pred_class) |>
  filter(.metric == "accuracy")
