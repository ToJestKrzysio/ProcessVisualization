from src.report_generator import generate_html_report, generate_pdf_report

generate_html_report("../examples/03_Rozpocznij_zatrudnienie.bpmn")
generate_pdf_report("../examples/03_Rozpocznij_zatrudnienie.bpmn", "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
