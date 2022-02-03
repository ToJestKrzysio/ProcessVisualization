# BPNM Report Generator

## Prerequisites
* Python 3.10+

## Usage
* Clone or download the repository
* Enter repository folder ```cd ReportGeneratorBPNM```
* Install dependencies ```pip install -r requirements.txt```
* Open python terminal inside repository, for example via bash by calling ```python3.10```
* Import report necessary functions, and generate reports
```python 
from src.reportgenerator import generate_pdf_report, generate_html_report

generate_html_report("../examples/01_Obsluga_zgloszen.bpmn")
generate_pdf_report("../examples/01_Obsluga_zgloszen.bpmn")
```


In case of problems with generating pdf report installation of [wkhtmltopdf] may be necessary.
Additionally, if that will not suffice manual definition of wkhtmltopdf_path should be specified in generate_pdf_report.


[wkhtmltopdf]:(https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf)
