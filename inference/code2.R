library(tidyverse)
library(infer)
library(palmerpenguins)

# -----------------------------------------------------------------------------
# Goal: Show how bootstrapping lets us estimate uncertainty using only a single
# observed sample. Instead of drawing new samples from a population (which we
# rarely have access to), we resample *with replacement* from our data to
# approximate the sampling distribution and build a confidence interval.
# -----------------------------------------------------------------------------

# Treat the observed Adelie penguin data as our one real-world sample
sample_data <- penguins |>
  filter(species == "Adelie", !is.na(flipper_length_mm)) |>
  select(flipper_length_mm)

sample_mean <- mean(sample_data$flipper_length_mm)
sample_size <- nrow(sample_data)

cat("Sample mean:", round(sample_mean, 2), "mm\n")
cat("Sample size:", sample_size, "\n")

# -----------------------------------------------------------------------------
# Bootstrap resampling: draw 1000 new samples from our data WITH replacement.
# Each bootstrap sample is the same size as the original. Because sampling is
# done with replacement, some observations appear more than once and some not
# at all — this mimics the variability we'd see across different real samples.
# -----------------------------------------------------------------------------
set.seed(42)
boot_samples <- sample_data |>
  rep_sample_n(size = sample_size, replace = TRUE, reps = 1000)

# Calculate the mean flipper length for each bootstrap replicate
boot_means <- boot_samples |>
  group_by(replicate) |>
  summarize(mean_flipper_length = mean(flipper_length_mm))

# -----------------------------------------------------------------------------
# Build a 95% confidence interval using the percentile method.
# The interval captures the middle 95% of bootstrap means. We are 95% confident
# the true population mean flipper length falls within this range.
# -----------------------------------------------------------------------------
ci_bounds <- quantile(boot_means$mean_flipper_length, c(0.025, 0.975))
ci_lower <- ci_bounds[[1]]
ci_upper <- ci_bounds[[2]]

cat("95% Confidence Interval: [", round(ci_lower, 2), ",", round(ci_upper, 2), "] mm\n")

se_bootstrap <- sd(boot_means$mean_flipper_length)
cat("Standard error of bootstrap distribution:", round(se_bootstrap, 2), "mm\n")

# -----------------------------------------------------------------------------
# Visualize the bootstrap distribution.
# The red line marks our observed sample mean (the centre of the distribution).
# The dashed orange lines mark the 2.5th and 97.5th percentiles — the edges of
# the 95% CI. Values outside those lines represent unlikely estimates.
# -----------------------------------------------------------------------------
ci_df <- tibble(value = c(ci_lower, ci_upper), label = c("2.5%", "97.5%"))

bootstrap_plot <- ggplot(boot_means, aes(x = mean_flipper_length)) +
  geom_histogram(binwidth = 0.3, colour = "white", fill = "steelblue") +
  geom_vline(xintercept = sample_mean, colour = "red", linewidth = 1) +
  geom_vline(
    data = ci_df,
    aes(xintercept = value),
    colour = "orange", linetype = "dashed", linewidth = 1
  ) +
  labs(
    title = paste0(
      "Bootstrap Distribution of Mean Flipper Length (", sample_size, " observations)"
    ),
    x = "Mean Flipper Length (mm)",
    y = "Count"
  ) +
  theme_minimal()

bootstrap_plot
