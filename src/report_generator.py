from datetime import date
from jinja2 import FileSystemLoader, Environment

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
template = env.get_template("bpmn_report.html")
# file_system.load("bpmn_report.html")
# print(file_system)

new_template = template.render()

file_name = "dupa"
date = date.today().strftime("%d_%m_%Y")
with open(f"reports/report_{file_name}_{date}.html", "w") as fh:
    fh.write(new_template)
