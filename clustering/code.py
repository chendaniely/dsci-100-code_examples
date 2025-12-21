import altair as alt
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn import set_config
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline


### Do not worry about this code, it's to create the example dataset
# Output dataframes instead of arrays
set_config(transform_output="pandas")

iris_data = load_iris(as_frame=True)
iris = pd.concat([iris_data.data, iris_data.target.rename("species")], axis=1)
iris["species"] = iris["species"].map({0: "setosa", 1: "versicolor", 2: "virginica"})
iris
###

# example 1 -----
# run k-means on 2 variables with standarization

preprocessor1 = make_column_transformer(
    (StandardScaler(), ["sepal length (cm)", "sepal width (cm)"]),
    verbose_feature_names_out=False,  # do not worry about this argument
)
preprocessor1


kmeans = KMeans(n_clusters=3)
kmeans


clust = make_pipeline(preprocessor1, kmeans)
clust.fit(iris)
clust

iris["kmeans1"] = clust[1].labels_
iris

iris.groupby(["species", "kmeans1"])["kmeans1"].count()

## not needed, but this is code to create an elbow plot
inertias = []
k_range = range(1, 11)

for k in k_range:
    kmeans_temp = KMeans(n_clusters=k, random_state=42)
    clust_temp = make_pipeline(preprocessor1, kmeans_temp)
    clust_temp.fit(iris)
    inertias.append(clust_temp[1].inertia_)

# Create dataframe for plotting
elbow_df = pd.DataFrame({"k": list(k_range), "inertia": inertias})

# Create elbow plot
alt.Chart(elbow_df).mark_line(point=True).encode(
    x=alt.X("k:Q", title="Number of Clusters (k)", scale=alt.Scale(domain=[1, 10])),
    y=alt.Y("inertia:Q", title="Inertia (Within-Cluster Sum of Squares)"),
).properties(title="Elbow Plot for K-Means Clustering", width=500, height=300)

#

# example 2 -----
# run k means on all variables (including species and other categorical)
# standarize on 2 variables (missing others)
# code here is to show a comparison on what happens if you use categorical variables
# you are not responsible on one-hot/dummy variable encoding

### Do not worry about this code, it's to create the example dataset
iris_data = load_iris(as_frame=True)
iris = pd.concat([iris_data.data, iris_data.target.rename("species")], axis=1)
iris["species"] = iris["species"].map({0: "setosa", 1: "versicolor", 2: "virginica"})
iris
###

preprocessor2 = make_column_transformer(
    (StandardScaler(), ["sepal length (cm)", "sepal width (cm)"]),
    (OneHotEncoder(sparse_output=False), ["species"]),
    verbose_feature_names_out=False,
    remainder="passthrough",  # this parameter puts all the other variables into the model as-is
)

clust = make_pipeline(preprocessor2, kmeans)
clust.fit(iris)
clust

iris["kmeans2"] = clust[1].labels_
iris

iris.groupby(["species", "kmeans2"])["kmeans2"].count()

# example 3 -----
# run k means on all variables (including species and other categorical)
# standarize all numeric

### Do not worry about this code, it's to create the example dataset
iris_data = load_iris(as_frame=True)
iris = pd.concat([iris_data.data, iris_data.target.rename("species")], axis=1)
iris["species"] = iris["species"].map({0: "setosa", 1: "versicolor", 2: "virginica"})
iris
###

preprocessor3 = make_column_transformer(
    (
        StandardScaler(),
        [
            "sepal length (cm)",
            "sepal width (cm)",
            "petal length (cm)",
            "petal width (cm)",
        ],
    ),
    (OneHotEncoder(sparse_output=False), ["species"]),
    verbose_feature_names_out=False,
    remainder="passthrough",
)

clust = make_pipeline(preprocessor3, kmeans)
clust.fit(iris)
clust

iris["kmeans3"] = clust[1].labels_
iris

iris.groupby(["species", "kmeans3"])["kmeans3"].count()
