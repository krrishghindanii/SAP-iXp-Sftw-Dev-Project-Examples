# Case Study: Ramen Data Analysis

**Author:** Krrish Ghindani
**Date:** September 16, 2024

---

## Project Overview

This project examines a rich ramen dataset to uncover trends and insights across various attributes, including **brand**, **country**, **star ratings**, **packaging style**, and **salt content** (expressed as a percentage). The primary objectives include:

* Identifying top-performing ramen brands
* Exploring the relationship between **salt content** and **ratings**
* Analyzing the distribution of **ramen packaging styles** by country
* Understanding regional preferences and trends in ramen consumption
* Highlighting brands that made it to the **Top 10 Ramen List** by year

---

## Dataset Description

The dataset includes detailed information on hundreds of ramen varieties worldwide. Key columns include:

* `Brand`: Name of the ramen brand
* `Country`: Country of origin
* `Stars`: User rating (on a 0–5 scale)
* `Style`: Packaging type (e.g., Pack, Cup, Bowl)
* `SaltPct`: Salt content as a percentage
* `TopTen`: Indicator for whether the ramen was ranked in the top 10 for a given year

---

## Libraries Used

This analysis is built using **R** and relies on the following libraries:

* `ggplot2`: Data visualization
* `dplyr`: Data manipulation and grouping
* `tidyr`: Handling missing values and data tidying
* `stringr`: Text processing and string matching

---

## How to Run the Project

1. Clone the repository to your local machine.
2. Ensure the `ramen.Rdata` file is in your R working directory.
3. Open the R script or R Markdown file containing the analysis.
4. Load the dataset using:

   ```r
   load("ramen.Rdata")
   ```
5. Install required packages if not already installed:

   ```r
   install.packages(c("ggplot2", "dplyr", "tidyr", "stringr"))
   ```
6. Run each code chunk sequentially to perform data cleaning, analysis, and visualization.

---

## Insights & Findings

* **Top Brands**: Certain brands consistently received high ratings across years and countries.
* **Salt vs. Rating**: Analysis showed varying patterns in how salt content influences star ratings.
* **Country Trends**: Some countries favored cup-style ramen while others preferred traditional pack-style.
* **Top 10 Appearance**: Ramen products in the top 10 list often had unique combinations of flavor, packaging, and regional appeal.

---

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for more information.

---
