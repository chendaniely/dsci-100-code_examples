import pandas as pd

URL = "https://raw.githubusercontent.com/cmrivers/ebola/refs/heads/master/country_timeseries.csv"
ebola = pd.read_csv(URL)
ebola

ebola_long = ebola.melt(
    id_vars=["Date", "Day"],
    var_name="cd_country",
    value_name="count",
)
ebola_long


# don't need to know
ebola_long[["case_death", "country"]] = ebola_long.cd_country.str.split(
    "_",
    expand=True,
)
ebola_long


ebola_long.groupby(["case_death", "country"])["count"].max().reset_index()


ebola_tidy = (
    ebola_long.drop(columns="cd_country")  # dropping a column
    .pivot(index=["Date", "Day", "country"], columns="case_death", values="count")
    .reset_index()
    .dropna()
)
ebola_tidy

# final clean up of names
# don't need to know
ebola_tidy.columns.name = None
ebola_tidy
