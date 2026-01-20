# 🇮🇳 UIDAI Analyitcs & Insights Dashboard

> **Hackathon 2026 Submission**  
> *A Next-Gen Analytical Tool for Aadhaar Saturation & Strategic Decision Making.*

## 🌟 Project Overview
This dashboard is a specialized analytics platform designed for UIDAI decision-makers. It integrates disparate datasets—Aadhaar Enrollments, Demographic Updates, Biometric Logs, and Civil Registration System (Births) data—to provide a unified view of the ecosystem's health. 

The tool moves beyond basic reporting to provide **Strategic Intelligence**, helping identify:
-   **"Ghost Children":** Gaps between actual births and child enrollments.
-   **Compliance Risks:** Populations missing Mandatory Biometric Updates (MBU).
-   **Service Gaps:** Districts with dwindling operator activity.

## 🚀 Key Features

### 1. 🗺️ Interactive Saturation Maps
-   Full India State & District level drill-down capabilities.
-   Visualizes enrollment density and activity hotspots.
-   Interactive click-events to explore specific regions.

### 2. 🎯 Strategic Action Center
-   **Age Cohort Analysis:** Heatmaps showing demographic shifts (0-5 vs 5-17 vs 18+).
-   **Risk Dashboard:** Identifies districts where biometric updates lag behind demographic changes (Critical for Age 5/15 MBU).
-   **Scheme Linkages:** Maps age cohorts to active government schemes (POSHAN, Scholarships) to drive enrollment value.

### 3. 👶 Birth vs. Enrollment Gap Analysis
-   **Data Fusion:** Merges CRS (Civil Registration System) birth data with UIDAI enrollment databases.
-   **Gap Viz:** Quantifies the exact number of missing children (Births - Enrollments) per state.
-   **Impact:** Pinpoints exactly where hospital-based enrollment integration is failing.

## 🛠️ Technology Stack
-   **Language:** Python 3.12+
-   **Framework:** Streamlit (Web App)
-   **Data Engine:** Pandas, NumPy
-   **Visualization:** Plotly Express, Plotly Graph Objects
-   **Geospatial:** GeoJSON

## 📂 Project Structure
```
├── app.py                     # Main Application Entry Point
├── ANALYSIS_CONCEPTS.md       # Detailed guide on the analytical logic & visualizations
├── PROJECT_REPORT.md          # Formal project methodology and findings report
├── Dataset_Cleaned/           # Processed CSV Data (Enrolment, Bio, Demo)
├── india_states.geojson       # Geospatial boundaries for States
├── india_districts.geojson    # Geospatial boundaries for Districts
└── births_statewise_and_ut.xlsx # Birth registration statistics
```

## ⚙️ How to Run

1.  **Prerequisites:** Ensure Python is installed.
2.  **Install Dependencies:**
    ```bash
    pip install streamlit pandas plotly openpyxl
    ```
3.  **Launch the App:**
    ```bash
    python -m streamlit run app.py
    ```

## 🧠 Decision Framework
This tool is designed to support the **"Saturation -> Compliance -> Utilization"** lifecycle:
1.  **Saturation:** Use the Map & Birth Analysis to find who is *not* enrolled.
2.  **Compliance:** Use the Risk Dashboard to find who needs *updates*.
3.  **Utilization:** Use the Age/Scheme mapper to ensure Aadhaar is *used* for welfare delivery.

---
*Developed for UIDAI Hackathon 2026*
