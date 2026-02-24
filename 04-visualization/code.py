import altair as alt
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)

df = iris.frame


alt.Chart(df).mark_point().encode(
    x="sepal length (cm):Q",
    y="sepal width (cm):Q",
    color="petal length (cm)",
)

URL = "https://gist.githubusercontent.com/seankross/a412dfbd88b3db70b74b/raw/5f23f993cd87c283ce766e7ac6b329ee7cc2e1d1/mtcars.csv"

cars = pd.read_csv(URL)

alt.Chart(cars).mark_point().encode(x="hp:Q", y="mpg:Q", color="cyl")

alt.Chart(cars).mark_point().encode(x="hp:Q", y="mpg:Q", color="cyl:Q")
alt.Chart(cars).mark_point().encode(x="hp:Q", y="mpg:Q", color="cyl:N")
