import base64
import datetime

from jinja2 import FileSystemLoader, Environment
import pdfkit

from src.bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph
from src.visualizer import DiagramVisualizer


class ReportGenerator:

    def __init__(self, bpmn_diagram: BpmnDiagramGraph):
        self.diagram = bpmn_diagram
        self.file_loader = FileSystemLoader("templates")
        self.env = Environment(loader=self.file_loader)
        self.template_name = "bpmn_report.html"
        self.template = self.env.get_template(self.template_name)
        self.context_generator = ContextGenerator(self.diagram)
        self.report_path = "reports"
        self.visualizer = DiagramVisualizer(self.diagram)

    def generate_html_report(self, save=True):
        self.visualizer.generate_image(self.image_path)
        context = self.get_context()
        rendered_template = self.template.render(**context)

        if save:
            with open(self.html_report_path, "w") as html_file:
                html_file.write(rendered_template)
        return rendered_template

    @property
    def base_path(self) -> str:
        date = datetime.date.today().strftime("%d_%m_%Y")
        return f"{self.report_path}/report_{date}"

    @property
    def html_report_path(self) -> str:
        return f"{self.base_path}.html"

    @property
    def pdf_report_path(self) -> str:
        return f"{self.base_path}.pdf"

    @property
    def image_path(self) -> str:
        return f"{self.base_path}_image.png"

    def encode_image(self) -> str:
        image_path = self.image_path
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("UTF-8")

    def get_context(self):
        context = self.context_generator.get_context()
        context["encoded_image"] = self.encode_image()
        return context

    def generate_pdf_report(self):
        options = {
            'page-size': 'A4',
            'margin-top': '0.35in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        html_file = self.generate_html_report(save=False)
        pdfkit.from_string(html_file, self.pdf_report_path, options=options)


class ContextGenerator:

    def __init__(self, bpmn_diagram: BpmnDiagramGraph):
        self.diagram = bpmn_diagram
        self.id_mappings = self.get_id_mappings()

    def get_id_mappings(self) -> dict:
        labels = {}
        graph = self.diagram.diagram_graph
        for edge in graph.edges(data=True):
            labels[(edge[0], edge[1])] = edge[2].get("name", "").replace("\n", " ")
        for node in graph.nodes(data=True):
            labels[node[0]] = node[1].get("node_name", "").replace("\n", " ")
        return labels

    def get_context(self):
        context_names = ["start_events", "end_events", "processes", "gates", "edges",
                         "model_title"]
        context = {}
        for context_name in context_names:
            context[context_name] = getattr(self, f"get_{context_name}")()
        return context

    def get_model_title(self) -> str:
        return next(iter(self.diagram.process_elements))

    def get_start_events(self) -> tuple:
        return self.get_node_names_of_type("startEvent")

    def get_end_events(self) -> tuple:
        return self.get_node_names_of_type("endEvent")

    def get_processes(self) -> tuple:
        labels = ["task", "process", "subProcess", "intermediateCatchEvent",
                  "intermediateThrowEvent", "boundaryEvent"]
        results = []
        for label in labels:
            results.extend(self.get_node_names_of_type(label))
        return tuple(results)

    def get_gates(self) -> tuple:
        labels = ["complexGateway", "eventBasedGateway", "inclusiveGateway", "exclusiveGateway",
                  "parallelGateway"]
        results = []
        for label in labels:
            results.extend(self.get_node_names_of_type(label))
        return tuple(results)

    def get_edges(self) -> tuple:
        results = []
        for edge in self.diagram.diagram_graph.edges(data=True):
            edge_name = edge[2].get("name", "") or "Unnamed"
            start_name = self.id_mappings[edge[0]] or "Unnamed"
            end_name = self.id_mappings[edge[1]] or "Unnamed"
            elements = {"start": start_name, "end": end_name, "edge": edge_name}
            results.append(elements)
        return tuple(results)

    def get_node_names_of_type(self, node_type: str) -> tuple:
        node_ids = self.diagram.get_nodes_id_list_by_type(node_type)
        return tuple(self.id_mappings[node_id] for node_id in node_ids)


if __name__ == '__main__':
    bpnm_diagram = BpmnDiagramGraph()
    bpnm_diagram.load_diagram_from_xml_file("../examples/01_Obsluga_zgloszen.bpmn")
    report_generator = ReportGenerator(bpnm_diagram)
    # report_generator.generate_html_report()
    report_generator.generate_pdf_report()
