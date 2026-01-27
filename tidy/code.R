library(tidyverse)

URL <- "https://raw.githubusercontent.com/cmrivers/ebola/refs/heads/master/country_timeseries.csv"
ebola <- read_csv(URL)

ebola_long <- ebola |>
  pivot_longer(
    cols = -c(Date, Day),
    names_to = "cd_country",
    values_to = "count"
  )

ebola_long <- ebola_long |>
  separate(
    cd_country,
    into = c("case_death", "country"),
    sep = "_"
  )

ebola_long |>
  summarize(max_count = max(count, na.rm = TRUE), .by = c(case_death, country))

ebola_tidy <- ebola_long |>
  pivot_wider(
    id_cols = c(Date, Day, country),
    names_from = case_death,
    values_from = count
  ) |>
  drop_na()

ebola_tidy
