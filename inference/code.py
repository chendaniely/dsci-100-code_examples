from palmerpenguins import load_penguins
import pandas as pd
import numpy as np
import altair as alt

# load and clean data
penguins = load_penguins().dropna()

# treat the full Adelie penguin flipper length data as our "population"
adelie = penguins[penguins["species"] == "Adelie"]
population = adelie["flipper_length_mm"].copy()
population_mean = population.mean()
population_size = len(population)

print(f"Population mean: {population_mean:.2f} mm")
print(f"Population size: {population_size}")

# take many samples from the population (without replacement)
np.random.seed(42)
n_samples = 1000
sample_size_n = 30  # Each sample has 30 penguins
sample_means = []

for i in range(n_samples):
    sample = population.sample(n=sample_size_n, replace=False)
    sample_means.append(sample.mean())

sampling_dist_df = pd.DataFrame({"mean_flipper_length": sample_means})

# calculate standard error
se_sampling = np.std(sample_means)
print(f"Standard error of sampling distribution: {se_sampling:.2f} mm")

# visualize sampling distribution
sampling_chart = (
    alt.Chart(sampling_dist_df)
    .mark_bar()
    .encode(
        alt.X(
            "mean_flipper_length:Q",
            bin=alt.Bin(maxbins=30),
            title="Sample Mean Flipper Length (mm)",
        ),
        alt.Y("count()", title="Count"),
    )
    .properties(
        title="Sampling Distribution of Mean Flipper Length (n=30, 1000 samples)",
        width=600,
        height=400,
    )
)

# add population mean line
pop_line = (
    alt.Chart(pd.DataFrame({"pop_mean": [population_mean]}))
    .mark_rule(color="red", size=2)
    .encode(x="pop_mean:Q")
)

sampling_chart + pop_line
