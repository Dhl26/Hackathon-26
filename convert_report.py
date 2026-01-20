
import markdown
from xhtml2pdf import pisa
import os

def convert_md_to_pdf(source_md, output_pdf):
    # 1. Read Markdown
    with open(source_md, 'r', encoding='utf-8') as f:
        text = f.read()

    # 2. Convert to HTML
    # Extras: tables for table support, fencing for code blocks
    html_text = markdown.markdown(text, extensions=['tables', 'fenced_code'])

    # 3. Add some basic styling
    styled_html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: sans-serif; font-size: 11pt; line-height: 1.5; }}
        h1 {{ color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px; }}
        h2 {{ color: #2874A6; margin-top: 20px; }}
        h3 {{ color: #1B4F72; }}
        code {{ background-color: #f4f4f4; padding: 2px 5px; font-family: monospace; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 10px; margin-bottom: 10px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .metric-box {{ background-color: #e8f6f3; padding: 10px; border-left: 5px solid #1abc9c; margin: 10px 0; }}
    </style>
    </head>
    <body>
    {html_text}
    </body>
    </html>
    """

    # 4. Write PDF
    with open(output_pdf, "wb") as result_file:
        pisa_status = pisa.CreatePDF(
            styled_html,                # the HTML to convert
            dest=result_file            # file handle to recieve result
        )

    if pisa_status.err:
        print(f"Error converting {source_md}: {pisa_status.err}")
    else:
        print(f"Successfully created {output_pdf}")

if __name__ == "__main__":
    if os.path.exists("PROJECT_REPORT.md"):
        convert_md_to_pdf("PROJECT_REPORT.md", "UIDAI_Hackathon_Project_Report.pdf")
    else:
        print("PROJECT_REPORT.md not found!")
