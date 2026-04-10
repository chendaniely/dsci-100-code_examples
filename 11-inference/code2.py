import pandas as pd
import numpy as np
import altair as alt

# load and clean data
URL = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
penguins = pd.read_csv(URL).dropna()

# treat adelie as our "sample" (what we actually observed in reality)
adelie = penguins[penguins["species"] == "Adelie"]
sample = adelie["flipper_length_mm"].copy()
sample_mean = sample.mean()
sample_size = len(sample)

print(f"Sample mean: {sample_mean:.2f} mm")
print(f"Sample size: {sample_size}")

# bootstrap resampling (with replacement)
np.random.seed(42)
n_bootstrap = 1000
bootstrap_means = []

for i in range(n_bootstrap):
    bootstrap_sample = sample.sample(n=sample_size, replace=True)
    bootstrap_means.append(bootstrap_sample.mean())

bootstrap_df = pd.DataFrame({"mean_flipper_length": bootstrap_means})

# calculate 95% confidence interval
ci_lower = np.percentile(bootstrap_means, 2.5)
ci_upper = np.percentile(bootstrap_means, 97.5)

print(f"95% Confidence Interval: [{ci_lower:.2f}, {ci_upper:.2f}] mm")

# calculate standard error
se_bootstrap = np.std(bootstrap_means)
print(f"Standard error of bootstrap distribution: {se_bootstrap:.2f} mm")

# visualize bootstrap distribution
bootstrap_chart = (
    alt.Chart(bootstrap_df)
    .mark_bar()
    .encode(
        alt.X(
            "mean_flipper_length:Q",
            bin=alt.Bin(maxbins=30),
            title="Mean Flipper Length (mm)",
        ),
        alt.Y("count()", title="Count"),
    )
    .properties(
        title=f"Bootstrap Distribution of Mean Flipper Length ({sample_size} observations)",
        width=600,
        height=400,
    )
)

# add sample mean line
sample_line = (
    alt.Chart(pd.DataFrame({"sample": [sample_mean]}))
    .mark_rule(color="red", size=2)
    .encode(x="sample:Q")
)

# add confidence interval lines
ci_lines = pd.DataFrame({"value": [ci_lower, ci_upper], "label": ["2.5%", "97.5%"]})

ci_chart = (
    alt.Chart(ci_lines).mark_rule(color="orange", strokeDash=[5, 5]).encode(x="value:Q")
)

bootstrap_chart + sample_line + ci_chart
