from palmerpenguins import load_penguins
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn import set_config
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline

# Output dataframes instead of arrays
set_config(transform_output="pandas")

penguins = load_penguins().dropna()
penguins

# %% example 1 -----
# run k-means on 2 variables with standarization

preprocessor1 = make_column_transformer(
    (StandardScaler(), ["bill_length_mm", "flipper_length_mm"]),
    verbose_feature_names_out=False,
)
preprocessor1


kmeans = KMeans(n_clusters=3)
kmeans


penguin_clust = make_pipeline(preprocessor1, kmeans)
penguin_clust.fit(penguins)
penguin_clust

penguins["kmeans1"] = penguin_clust[1].labels_
penguins

penguins.groupby(["species", "kmeans1"])["kmeans1"].count()

# %% example 2 -----
# run k means on all variables (including species and other categorical)
# standarize on 2 variables (missing others)

penguins = load_penguins().dropna()
penguins

preprocessor2 = make_column_transformer(
    (StandardScaler(), ["bill_length_mm", "flipper_length_mm"]),
    (OneHotEncoder(sparse_output=False), ["species", "island", "sex"]),
    verbose_feature_names_out=False,
    remainder="passthrough",
)

penguin_clust = make_pipeline(preprocessor2, kmeans)
penguin_clust.fit(
    penguins,
)
penguin_clust

penguins["kmeans2"] = penguin_clust[1].labels_
penguins

penguins.groupby(["species", "kmeans2"])["kmeans2"].count()

# %% example 3 -----
# run k means on all variables (including species and other categorical)
# standarize all numeric

penguins = load_penguins().dropna()
penguins

preprocessor3 = make_column_transformer(
    (
        StandardScaler(),
        [
            "bill_length_mm",
            "flipper_length_mm",
            "bill_depth_mm",
            "body_mass_g",
            "year",
        ],
    ),
    (OneHotEncoder(sparse_output=False), ["species", "island", "sex"]),
    verbose_feature_names_out=False,
    remainder="passthrough",
)

penguin_clust = make_pipeline(preprocessor2, kmeans)
penguin_clust.fit(
    penguins,
)
penguin_clust

penguins["kmeans3"] = penguin_clust[1].labels_
penguins

penguins.groupby(["species", "kmeans3"])["kmeans3"].count()
