from palmerpenguins import load_penguins

penguins = load_penguins().dropna()

penguins

from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer
from sklearn import set_config

# Output dataframes instead of arrays
set_config(transform_output="pandas")

preprocessor = make_column_transformer(
    (StandardScaler(), ["bill_length_mm", "flipper_length_mm"]),
    verbose_feature_names_out=False,
)
preprocessor

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
kmeans

from sklearn.pipeline import make_pipeline

penguin_clust = make_pipeline(preprocessor, kmeans)
penguin_clust.fit(penguins)
penguin_clust

penguins["cluster"] = penguin_clust[1].labels_
penguins

penguins.groupby(["species", "cluster"])["cluster"].count()
