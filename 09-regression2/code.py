import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn import set_config

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

set_config(transform_output="pandas")

skhouse = fetch_california_housing(as_frame=True)

housing_x = skhouse["data"]
housing_y = skhouse["target"]
housing_x_train, housing_x_test, housing_y_train, housing_y_test = train_test_split(
    housing_x,
    housing_y,
    test_size=0.2,
    random_state=42,
)

regressor = LinearRegression().fit(housing_x_train, housing_y_train)

regressor.coef_

regressor.intercept_

# coefficient table of results
coefs = pd.DataFrame(
    {
        "feature": housing_x_train.columns,
        "coef": regressor.coef_,
    }
).assign(intercept=regressor.intercept_)

coefs

# predict on the test set
predicted = regressor.predict(housing_x_test)

rmspe_lr = mean_squared_error(
    y_true=housing_y_test,
    y_pred=predicted,
) ** (1 / 2)

rmspe_lr
