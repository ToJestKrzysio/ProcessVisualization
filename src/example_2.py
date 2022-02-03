from src.report_generator import generate_html_report, generate_pdf_report

generate_html_report("../examples/02_Realizuj_zlecenie.bpmn")
generate_pdf_report("../examples/02_Realizuj_zlecenie.bpmn", "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
