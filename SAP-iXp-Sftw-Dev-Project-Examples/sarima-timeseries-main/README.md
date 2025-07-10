# Urban Air Quality Forecasting & Improvement Using SARIMA

Forecasting and improving air quality across Shanghai, Delhi, Indore, Los Angeles, and Imphal using time-series modeling.

---

## Overview

This project utilizes SARIMA (Seasonal AutoRegressive Integrated Moving Average) models to analyze and forecast air quality metrics for five major cities: Shanghai, Delhi, Indore, Los Angeles, and Imphal. The objective is to deliver accurate forecasts and actionable insights to aid environmental planning and policy implementation.

---

## Objectives

* Analyze historical air quality data across multiple cities
* Visualize pollutant trends and temporal patterns
* Generate short-term forecasts for key pollutants
* Deliver detailed reports to inform environmental improvement strategies
* Collaborate with local authorities (e.g., the Indian Municipal Corporation for Indore) to recommend and implement changes

---

## Forecasted Air Quality Components

* AQI – Air Quality Index
* CO – Carbon Monoxide
* NO – Nitric Oxide
* NO₂ – Nitrogen Dioxide
* O₃ – Ozone
* SO₂ – Sulfur Dioxide
* PM₂.₅ – Fine Particulate Matter
* PM₁₀ – Respirable Particulate Matter
* NH₃ – Ammonia

---

## Features

### Data Preprocessing

* Loads city-level data from CSV files (e.g., `Shanghai.csv`)
* Filters data to the last 5 years
* Resamples data to hourly intervals
* Cleans and prepares data for modeling

### Visualization

* Plots historical trends for each pollutant
* Performs time series decomposition to identify seasonality and trend
* Generates pollutant-wise visualizations and comparisons

### SARIMA Modeling

* Fits SARIMA models for each pollutant in every city
* Performs parameter tuning using AIC/BIC for model selection
* Generates 90-day forecasts with confidence intervals
* Produces forecast plots for intuitive understanding

### Real-World Impact

* Submitted a comprehensive air quality report for **Indore** to the **Indian Municipal Corporation**
* Identified high-risk zones with critical pollution levels
* Recommended targeted interventions and policy measures
* Contributed to local environmental improvement efforts based on data-driven evidence

---

## Tech Stack

* Python 3.x
* pandas – Data manipulation
* numpy – Numerical computing
* matplotlib – Data visualization
* statsmodels – SARIMA modeling

---

## How to Use

1. Clone the repository:

   ```bash
   git clone https://github.com/krrishghindanii/sarima-timeseries.git
   cd sarima-timeseries
   ```

2. Place your city dataset(s) (e.g., `Shanghai.csv`) in the project directory.

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:

   ```bash
   python air_quality_forecast.py
   ```

The script will output pollutant-wise forecasts, trend visualizations, and summaries.

---

## Data Format

Each city dataset (CSV) should contain:

* A `dt` column with timestamps
* Separate columns for each air quality component (e.g., `PM2.5`, `NO2`, `CO`, etc.)

---

## Contributions & Collaboration

We welcome contributions that enhance the forecasting models, add more cities, or integrate new data sources. This project also demonstrated a successful collaboration with government agencies to drive real-world environmental improvements.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
