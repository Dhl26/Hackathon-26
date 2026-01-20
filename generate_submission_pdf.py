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
        <p>Our "UIDAI Insights Dashboard" provides real-time visibility into the ecosystem's health.</p>

        <h3>Key Findings</h3>
        <ul>
            <li><strong>Geographic Disparities:</strong> While national coverage is improving, we identified <strong>3 Tier-1 Critical Districts</strong> (e.g., Bagpat, UP) with near-zero enrollments, requiring immediate intervention.</li>
            <li><strong>Enrollment vs. Births:</strong> A significant delta exists between registered births and Aadhaar enrollments in 2024, suggesting that process friction (separate visits for birth certificate and Aadhaar) is the primary drop-off point.</li>
            <li><strong>Updates as Risk Indicator:</strong> Districts with low biometric update ratios for the 5-17 age group correlate strongly with low initial enrollment, indicating systemic infrastructure issues in those regions.</li>
        </ul>

        <h3>Visualisations Developed</h3>
        <ul>
            <li><strong>Choropleth Saturation Maps:</strong> Interactive colour-coded maps of India showing state and district-wise saturation levels. "Red Zones" clearly highlight areas needing Rapid Kiosk Deployment.</li>
            <li><strong>Age-Cohort Heatmaps:</strong> Visual grids displaying the demographic make-up of enrollments. Helps spot anomalies (e.g., a district with 90% adult enrollment but 0% child enrollment).</li>
            <li><strong>Trend Analysis Charts:</strong> Line graphs comparing "Projected Births" vs "Actual Enrollments" over the last decade, visually demonstrating the widening or narrowing of the identity gap.</li>
            <li><strong>Risk Profile Donut Charts:</strong> Segments districts into High, Medium, and Low risk based on their bio-metric update compliance, aiding resource allocation.</li>
        </ul>

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
