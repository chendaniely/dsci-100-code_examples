from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn import set_config
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.pipeline import make_pipeline

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

# fit a model without pre-processing

knn = KNeighborsClassifier(n_neighbors=5)
knn

knn.fit(X=x, y=y)  # this line of code is wrong

y_pred = knn.predict(x_test)
y_test


knn.score(x_test, y_test)
accuracy_score(y_test, y_pred)

# fit model with pre processing

preprocessor = make_column_transformer(
    (StandardScaler(), make_column_selector(dtype_include="number")),
    verbose_feature_names_out=False,
)

# this line is also wrong
preprocessor.fit(x)  # using x instead of wine because the y is a number

scaled_wine = preprocessor.transform(x)
scaled_wine

knn_pipeline = make_pipeline(preprocessor, knn)
knn_pipeline.fit(X=x, y=y)  # this line is wrong
knn_pipeline

knn_pipeline.predict(x_train)
y_train

knn_pipeline.predict(x_test)
y_test

knn_pipeline.score(x_test, y_test)
