import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

# import the K-NN regression model
from sklearn.model_selection import GridSearchCV
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import set_config

# import the K-NN regression model
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

# scikit learn data comes in 2 parts
# it separates the predictor data from response data
skhouse = fetch_california_housing(as_frame=True)

print(skhouse.DESCR)

housing_x = skhouse["data"]
housing_y = skhouse["target"]

# split data!
housing_x_train, housing_x_test, housing_y_train, housing_y_test = train_test_split(
    housing_x, housing_y, test_size=0.2, random_state=42
)

# combine data to make it a single dataframe (for reference)
housing = pd.concat([housing_x, housing_y], axis="columns")
housing.columns
housing.head()


# --- model

# Output dataframes instead of arrays
set_config(transform_output="pandas")

# preprocess the data, make the pipeline
preprocessor = make_column_transformer(
    (
        StandardScaler(),
        [
            "MedInc",
            "HouseAge",
            "AveRooms",
            "AveBedrms",
            "Population",
            "AveOccup",
            "Latitude",
            "Longitude",
        ],
    )
)
pipeline = make_pipeline(preprocessor, KNeighborsRegressor())

# create the 5-fold GridSearchCV object
param_grid = {
    "kneighborsregressor__n_neighbors": range(1, 201, 3),
}
gridsearch = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="neg_root_mean_squared_error",
)

# fit the GridSearchCV object
gridsearch.fit(housing_x_train, housing_y_train)


# Retrieve the CV scores
results = pd.DataFrame(gridsearch.cv_results_)
results

# get the best parameter values
gridsearch.best_params_

predicted = gridsearch.predict(housing_x_test)

rmspe_knn = mean_squared_error(
    y_true=housing_y_test,
    y_pred=predicted,
) ** (1 / 2)

rmspe_knn
