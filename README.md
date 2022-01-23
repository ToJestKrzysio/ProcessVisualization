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
