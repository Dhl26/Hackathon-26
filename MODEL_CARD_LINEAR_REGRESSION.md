# Model Card: Birth Registration Projection Model (Linear Regression)

## Model Details
- **Model Name:** Birth Registration Linear Projection Model
- **Version:** 1.0
- **Type:** Simple Linear Regression (Least Squares)
- **Library:** `numpy` (`polyfit`)
- **Date:** January 2025
- **Developer:** Project Team (UIDAI Hackathon Submission)

## Intended Use
- **Primary Intended Uses:** 
    - To estimate future birth registration numbers (for years 2024 and 2025) for Indian States and Union Territories.
    - To provide a baseline for calculating Aadhaar enrollment coverage ratios for children aged 0-5.
- **Primary Intended Users:** 
    - Policy makers, UIDAI analysts, and district administrators planning enrollment camps.
- **Out-of-Scope Uses:** 
    - This model should **not** be used for precise demographic census planning without corroborating data.
    - It captures linear trends only and does not account for sudden demographic shifts, pandemics (post-COVID anomalies), or policy changes affecting registration rates.

## Training Data
- **Source:** Historical Birth Registration Data (2014-2023) from Civil Registration System (CRS) reports.
- **Features:** 
    - **Independent Variable (X):** Time (Year Index, e.g., 0 for 2014, 1 for 2015).
    - **Target Variable (Y):** Number of Registered Births.
- **Data Preprocessing:**
    - "N.A." and missing values are filtered out.
    - A minimum of 2 valid data points is required to generate a projection.

## Model Logic & Parameters
- **Algorithm:** Ordinary Least Squares (OLS) Linear Regression.
    - $y = mx + c$
    - Where $m$ is the slope (growth/decline rate) and $c$ is the intercept.
- **Training Procedure:**
    - The model fits a line to the valid historical data points for each state individually.
- **Forecasting:**
    - **2024 Prediction:** Extrapolated using the trend line derived from 2014-2023.
    - **2025 Prediction:** Extrapolated using the trend line derived from 2014-2024 (including the projected 2024 value).
- **Post-Processing:**
    - Predictions are rounded to the nearest integer.
    - Negative predictions are floored to 0.

## Evaluation
- **Method:** The model simply extrapolates the line of best fit. No formal train-test split was performed due to the small sample size (data is annual).
- **Metric:** The primary metric is the trend consistency with historical data.

## Caveats and Limitations
1.  **Linear Assumption:** The model assumes birth registrations follow a linear trend. This may not be true for all states (e.g., states with fluctuating birth rates).
2.  **Dataset Size:** 10 data points (2014-2023) is a small dataset for robust time-series forecasting.
3.  **External Factors:** Does not account for external factors like the COVID-19 pandemic (2020-2021), which may have temporarily suppressed or inflated registration numbers, potentially skewing the long-term trend.
4.  **Error Propagation:** The 2025 prediction uses the *projected* 2024 value, meaning errors in 2024 will propagate to 2025.

## Ethical Considerations
- **Bias:** The model is purely statistical based on reported numbers. However, if historical registration data was biased (e.g., underreporting in certain regions), the projections will reflect that bias.
- **Impact:** Use of these projections for resource allocation should always include a buffer, as underestimating births could lead to insufficient enrollment kits/centers.

## Recommendations
- Use these projections as a **directional guide** rather than absolute truth.
- Update the model annually as verified 2024 data becomes available.
- Consider more advanced smoothing techniques (e.g., Exponential Smoothing) for future versions if non-linear trends are observed.
