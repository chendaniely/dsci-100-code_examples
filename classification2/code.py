from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn import set_config
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

import pandas as pd


##### Preparing data do not need to know about what's happenign here
set_config(transform_output="pandas")

data = load_wine(as_frame=True)

x = data["data"]
y = data["target"]

wine = pd.concat([x, y], axis="columns")
#####

print(data.DESCR)
print(wine.columns)
wine.head()


x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

preprocessor = make_column_transformer(
    (StandardScaler(), make_column_selector(dtype_include="number")),
    verbose_feature_names_out=False,
)

knn_pipeline = make_pipeline(
    preprocessor,
    KNeighborsClassifier(),
)


param_grid = {"kneighborsclassifier__n_neighbors": range(1, 21, 3)}

gridsearch = GridSearchCV(
    estimator=knn_pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="accuracy",
)

# fit the GridSearchCV object
gridsearch.fit(x_train, y_train)

print("Best CV accuracy:", gridsearch.best_score_)
print("Best parameters:", gridsearch.best_params_)

y_pred = gridsearch.predict(x_test)

test_accuracy = gridsearch.score(x_test, y_test)
print("Test accuracy:", test_accuracy)
