from src.report_generator import generate_html_report, generate_pdf_report

generate_html_report("../examples/01_Obsluga_zgloszen.bpmn")
generate_pdf_report("../examples/01_Obsluga_zgloszen.bpmn", "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
