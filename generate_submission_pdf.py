import os
from xhtml2pdf import pisa

def generate_pdf():
    # Define the content in HTML format with inline CSS for styling
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @page {
                size: A4;
                margin: 2cm;
                @frame footer_frame {
                    -pdf-frame-content: footerContent;
                    bottom: 1cm;
                    margin-left: 2cm;
                    margin-right: 2cm;
                    height: 1cm;
                }
            }
            body {
                font-family: Helvetica, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                color: #333;
            }
            h1 {
                color: #0047AB;
                font-size: 24pt;
                text-align: center;
                margin-bottom: 20px;
                border-bottom: 2px solid #0047AB;
                padding-bottom: 10px;
            }
            h2 {
                color: #2c3e50;
                font-size: 16pt;
                margin-top: 30px;
                margin-bottom: 15px;
                border-left: 5px solid #0047AB;
                padding-left: 10px;
            }
            h3 {
                color: #555;
                font-size: 13pt;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            p {
                margin-bottom: 10px;
                text-align: justify;
            }
            ul {
                margin-bottom: 10px;
            }
            li {
                margin-bottom: 5px;
            }
            .header-section {
                text-align: center;
                margin-bottom: 50px;
            }
            .team-name {
                font-size: 14pt;
                color: #666;
                font-weight: bold;
            }
            .alert-box {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
                color: #333;
            }
        </style>
    </head>
    <body>

        <div class="header-section">
            <h1>Universal Child Identity:<br>Bridging the Early Enrollment Gap</h1>
            <p class="team-name">Team: Birth-Chain | UIDAI Hackathon 2026</p>
        </div>

        <h2>1. Problem Statement and Approach</h2>
        
        <h3>Problem Statement</h3>
        <p>The Aadhaar ecosystem has achieved near-universal penetration in India, yet a critical gap persists in the <strong>0-5 age cohort</strong>, where approximately <strong>30-40% of children remain unenrolled</strong>. This "identity gap" leads to three major systemic failures:</p>
        <ul>
            <li><strong>Data Blind Spots:</strong> Inaccurate demographic data prevents effective planning for infrastructure, schools, and immunization programs.</li>
            <li><strong>Benefit Delivery Denial:</strong> Vulnerable children are excluded from welfare schemes like POSHAN Abhiyaan and Ayushman Bharat due to lack of diverse identity proof.</li>
            <li><strong>Child Safety Risks:</strong> Unidentified children are at higher risk of trafficking, illegal adoption, and identity fraud.</li>
        </ul>
        <p>Our analysis indicates that high aggregate enrollment numbers often mask deep district-level disparities. For instance, while states like Uttar Pradesh show high total numbers, specific districts (e.g., Bagpat) report zero enrollments for the 0-5 age group, highlighting critical execution gaps.</p>

        <h3>Analytical & Technical Approach</h3>
        <p>We propose a two-pronged <strong>"Birth-Chain"</strong> policy and technology framework to achieve 100% saturation:</p>
        <ol>
            <li><strong>Birth-Aadhaar Integration (Systemic Reform):</strong> 
                <p>Mandating Aadhaar enrollment at the point of birth by integrating hospital Hospital Management Information Systems (HMIS) and municipal birth registration portals directly with UIDAI's enrollment client. This ensures "One Birth, One Identity" instantly.</p>
            </li>
            <li><strong>Rapid Kiosk Deployment (Emergency Intervention):</strong>
                <p>A data-driven "Strategic Action Center" dashboard identifies "dark zones" (districts with &lt;50 enrollments). We propose deploying mobile mobile enrollment units to these specific geotagged locations to clear the backlog within 6 months.</p>
            </li>
        </ol>

        <h2>2. Datasets Used</h2>
        <p>Our analysis relies on a robust combination of official UIDAI datasets and government birth statistics to triangulate the enrollment gap.</p>
        
        <h3>Primary Datasets (UIDAI)</h3>
        <ul>
            <li><strong>Aadhaar Enrolment Data (2018-2024):</strong> Granular CSV data containing state and district-level enrollment figures, segmented by age groups (0-5, 5-17, 18+).</li>
            <li><strong>Aadhaar Biometric Update Data:</strong> Tracks biometric updates for children crossing age thresholds (5 and 15 years), used as a proxy for ecosystem engagement.</li>
            <li><strong>Aadhaar Demographic Update Data:</strong> Insights into correction trends which help identify data quality issues.</li>
        </ul>

        <h3>Secondary Datasets (Government of India)</h3>
        <ul>
            <li><strong>Registered Births Statistics (2014-2024):</strong> State-wise annual birth registration data sourced from the Civil Registration System (CRS) reports. Used to calculate the projected 2025 "Target Cohort" for the 0-5 age group.</li>
            <li><strong>GeoJSON Shapefiles:</strong> Vector data for Indian States and Districts to enable geospatial mapping and "dark zone" visualization.</li>
        </ul>

        <h2>3. Methodology</h2>
        <p>We adopted a rigorous data pipeline to ensure accuracy and actionable insights.</p>

        <h3>Data Cleaning & Preprocessing</h3>
        <ul>
            <li><strong>Standardization:</strong> Inconsistent state and district names (e.g., "Orissa" vs "Odisha", "Allahabad" vs "Prayagraj") were normalized using a custom mapping dictionary to ensure 100% match rate with GeoJSON maps.</li>
            <li><strong>Deduplication & Validation:</strong> Rows with invalid metadata (e.g., placeholder state names like "100000") were filtered out using pincode-based reverse lookup logic.</li>
            <li><strong>Temporal Alignment:</strong> Enrollment data was aggregated annually and closely matched with birth registration years to calculate the "Coverage Ratio".</li>
        </ul>

        <h3>Transformation Logic</h3>
        <ul>
            <li><strong>Cohort Projection:</strong> We calculated the expected "0-5 Population" for 2025 by summing birth registrations from 2020-2024, adjusting for standard mortality rates.</li>
            <li><strong>Saturation Calculation:</strong> <code>Coverage Ratio = (Actual 0-5 Enrollments / Projected 0-5 Population) * 100</code></li>
            <li><strong>Gap Identification:</strong> Calculated the absolute <code>Enrollment Gap = Projected Population - Actual Enrollments</code> to quantify the number of missing children per district.</li>
        </ul>

        <h2>4. Data Analysis and Visualisation</h2>
        <p>Our <strong>"UIDAI Insights Dashboard"</strong> serves as the central intelligence unit for this policy framework. It transforms raw data into actionable implementation triggers.</p>

        <h3>Dashboard Architecture</h3>
        <ul>
            <li><strong>Tech Stack:</strong> Built on <strong>Streamlit</strong> (Python) for rapid interactivity, integrated with <strong>Plotly</strong> for dynamic visualizations and <strong>Pandas/NumPy</strong> for high-performance data processing.</li>
            <li><strong>Deployment:</strong> Cloud-native architecture (Streamlit Cloud) ensuring accessibility for district magistrates and state nodal officers.</li>
        </ul>

        <h3>Key Modules & Features</h3>
        
        <h4>1. Strategic Action Center & Age Cohort Analysis</h4>
        <p>This module provides a granular view of enrollment distribution:</p>
        <ul>
            <li><strong>Demographic Heatmaps:</strong> Visualizes the density of enrollments across Age Groups (0-5, 5-17, 18+). This instantly highlights "inverted pyramids" where adult enrollment is high but child enrollment is near zero.</li>
            <li><strong>Interactive Filtering:</strong> Users can drill down from "All India" to specific States and Districts to isolate local anomalies.</li>
        </ul>

        <h4>2. Temporal Trends Engine</h4>
        <p>A time-series analysis tool that tracks month-on-month enrollment velocity:</p>
        <ul>
            <li><strong>Growth (QoQ) Metrics:</strong> Automatically calculates Quarter-over-Quarter growth. If a district shows negative growth, it is flagged for review.</li>
            <li><strong>Peak Detection:</strong> Identifies historical enrollment spikes (e.g., during past drives) to benchmark future capacity planning.</li>
        </ul>

        <h4>3. Risk & Anomalies Dashboard</h4>
        <p>The core compliance engine that categorizes districts based on ecosystem health:</p>
        <ul>
            <li><strong>Critical Risk (⚫):</strong> Districts with <strong>ZERO (0) enrollments</strong> in the 5-17 age group (indicating no base population for updates) or 0-5 group.</li>
            <li><strong>High Risk (🔴):</strong> Districts with Bio-Update Ratios &lt;20%, indicating a failure to update child biometrics at age 5.</li>
            <li><strong>Medium (🟡) & Low (🟢) Risk:</strong> Districts meeting standard operational benchmarks.</li>
        </ul>

        <h4>4. Birth vs Enrollment Predictive Model</h4>
        <p>To quantify the exact "Enrollment Gap", we developed a predictive model:</p>
        <ul>
            <li><strong>Model Type:</strong> Linear Regression (Ordinary Least Squares).</li>
            <li><strong>Training Data:</strong> Civil Registration System (CRS) birth data (2014-2023).</li>
            <li><strong>Projection:</strong> Forecasts <strong>2025 Birth Cohorts</strong> for every state.</li>
            <li><strong>Gap Analysis:</strong> Compares <em>Projected 2025 Births</em> vs <em>Actual Child Enrollments</em>. A gap >10% triggers a "Critical Coverage Alert".</li>
        </ul>

        <div class="alert-box">
            <strong>Key Insight:</strong> The integration of the Linear Regression model allows us to move from "reactive" analysis (looking at past data) to "proactive" planning (estimating the 2025 target cohort).
        </div>

        <div id="footerContent" style="text-align: center; color: #888; font-size: 9pt;">
            Generated by Team Birth-Chain for UIDAI Hackathon 2026
        </div>

    </body>
    </html>
    """

    # Generate PDF
    output_filename = "Hackathon_Submission_Consolidated.pdf"
    
    # Open output file for binary write
    with open(output_filename, "wb") as output_file:
        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(
            html_content,         # the HTML to convert
            dest=output_file      # file handle to recieve result
        )

    # Check for errors
    if pisa_status.err:
        print(f"Error generating PDF: {pisa_status.err}")
    else:
        print(f"PDF successfully generated: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    generate_pdf()
