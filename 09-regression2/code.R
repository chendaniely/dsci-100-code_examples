library(tidyverse)
library(tidymodels)

housing <- read_csv("https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv")

set.seed(42)
housing_split <- initial_split(housing, prop = 0.8)
housing_train <- training(housing_split)
housing_test  <- testing(housing_split)

lm_spec <- linear_reg() |>
  set_engine("lm") |>
  set_mode("regression")

# ocean_proximity is categorical, so we dummy-encode it
housing_recipe <- recipe(median_house_value ~ ., data = housing_train) |>
  step_dummy(all_nominal_predictors())

housing_wf <- workflow() |>
  add_recipe(housing_recipe) |>
  add_model(lm_spec)

housing_fit <- housing_wf |>
  fit(data = housing_train)

coefs <- housing_fit |>
  extract_fit_parsnip() |>
  tidy()

coefs

housing_test_results <- housing_fit |>
  predict(housing_test) |>
  bind_cols(housing_test)

rmspe_lr <- housing_test_results |>
  metrics(truth = median_house_value, estimate = .pred) |>
  filter(.metric == "rmse") |>
  pull(.estimate)

rmspe_lr
