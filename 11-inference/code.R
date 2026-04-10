library(tidyverse)
library(infer)
library(palmerpenguins)

# -----------------------------------------------------------------------------
# Goal: Show how a sampling distribution is built by taking many samples from
# a known population. In practice we never have the full population, but this
# exercise lets us see what "repeated sampling" looks like and why sample means
# cluster around the true population mean.
# -----------------------------------------------------------------------------

# Treat the full Adelie penguin flipper length data as our "population"
population <- penguins |>
  filter(species == "Adelie", !is.na(flipper_length_mm)) |>
  select(flipper_length_mm)

population_mean <- mean(population$flipper_length_mm)
population_size <- nrow(population)

cat("Population mean:", round(population_mean, 2), "mm\n")
cat("Population size:", population_size, "\n")

# -----------------------------------------------------------------------------
# Take 1000 random samples (without replacement) from the population.
# Each sample has 30 penguins — the same size used throughout the textbook.
# rep_sample_n() adds a "replicate" column so we can group by each sample.
# -----------------------------------------------------------------------------
set.seed(42)
samples <- population |>
  rep_sample_n(size = 30, replace = FALSE, reps = 1000)

# Calculate the sample mean flipper length for each of the 1000 samples
sample_means <- samples |>
  group_by(replicate) |>
  summarize(mean_flipper_length = mean(flipper_length_mm))

# The standard error tells us how much sample means vary around the population mean
se_sampling <- sd(sample_means$mean_flipper_length)
cat("Standard error of sampling distribution:", round(se_sampling, 2), "mm\n")

# -----------------------------------------------------------------------------
# Visualize the sampling distribution.
# Each bar represents how often samples produced a mean in that range.
# The red line marks the true population mean — notice the distribution is
# centred on it. This illustrates that sample means are unbiased estimators.
# -----------------------------------------------------------------------------
sampling_plot <- ggplot(sample_means, aes(x = mean_flipper_length)) +
  geom_histogram(binwidth = 0.5, colour = "white", fill = "steelblue") +
  geom_vline(xintercept = population_mean, colour = "red", linewidth = 1) +
  labs(
    title = "Sampling Distribution of Mean Flipper Length (n = 30, 1000 samples)",
    x = "Sample Mean Flipper Length (mm)",
    y = "Count"
  ) +
  theme_minimal()

sampling_plot
