from __future__ import annotations

import base64
import datetime
import os.path
from pathlib import Path

from jinja2 import FileSystemLoader, Environment
import pdfkit

import src.bpmn_python.bpmn_python_consts as consts
from src.bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph
from src.visualizer import DiagramVisualizer


class ReportGenerator:
    """ Class handling task related to generation of the reports. """

    def __init__(self, bpmn_diagram: BpmnDiagramGraph):
        self.diagram = bpmn_diagram
        self.file_loader = FileSystemLoader("templates")
        self.env = Environment(loader=self.file_loader)
        self.template_name = "bpmn_report.html"
        self.template = self.env.get_template(self.template_name)
        self.report_path = "reports"
        self.context_generator = ContextGenerator(self.diagram)
        self.visualizer = DiagramVisualizer(self.diagram)
        self.file_name = None
        if not os.path.exists(self.report_path):
            os.mkdir(self.report_path)

    @classmethod
    def from_file(cls, file_path: str) -> ReportGenerator:
        """ Loads BPMN model form .xml/.bpmn file and returns new instance of ReportGenerator. """
        diagram = BpmnDiagramGraph()
        diagram.load_diagram_from_xml_file(file_path)
        instance = cls(diagram)
        instance.file_name = Path(file_path).stem
        return instance

    def generate_html_report(self, save=True) -> str:
        """
        Renders html report using context data, may save report to html_report_path.
        Returns rendered report as a string.
        """
        self.visualizer.generate_image(self.image_path)
        context = self.get_context()
        rendered_template = self.template.render(**context)

        if save:
            with open(self.html_report_path, "w") as html_file:
                html_file.write(rendered_template)
        return rendered_template

    def generate_pdf_report(self, wkhtmltopdf_path=None) -> None:
        """
        Generates pdf report using string representation of html_report and saves it to
        pdf_report_path.
        """
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

        config = {"configuration": pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)} if wkhtmltopdf_path else {}
        html_file = self.generate_html_report(save=False)
        pdfkit.from_string(html_file, self.pdf_report_path, options=options, **config)

    @property
    def base_path(self) -> str:
        """
        Base path used for saving all reports.
        Every report name contains date of report generation.
        """
        date = datetime.date.today().strftime("%d_%m_%Y")
        file_name = f"_{self.file_name}" if self.file_name else ""
        return f"{self.report_path}/report_{date}{file_name}"

    @property
    def html_report_path(self) -> str:
        """ Path used for saving html reports. """
        return f"{self.base_path}.html"

    @property
    def pdf_report_path(self) -> str:
        """ Path used for saving pdf reports. """
        return f"{self.base_path}.pdf"

    @property
    def image_path(self) -> str:
        """ Path used for saving graphical model representation. """
        return f"{self.base_path}_image.png"

    def encode_image(self) -> str:
        """ Encodes image to base64, to allow for embedding into html or pdf report. """
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("UTF-8")

    def get_context(self):
        """ Generates context used during image generation. """
        context = self.context_generator.get_context()
        context["encoded_image"] = self.encode_image()
        return context


class ContextGenerator:
    """ Class handling generation of context data from BpmnDiagramGraph. """

    def __init__(self, bpmn_diagram: BpmnDiagramGraph):
        self.diagram = bpmn_diagram
        self.id_mappings = self.get_id_mappings()

    def get_context(self) -> dict:
        """
        Generates context content by calling methods inside context_names with 'get_' suffix.
        """
        context_names = ["start_events", "end_events", "processes", "gates", "edges",
                         "model_title", "nodes"]
        return {context_name: getattr(self, f"get_{context_name}")()
                for context_name in context_names}

    def get_id_mappings(self) -> dict:
        """ Generates dictionary, mapping ids to node names. """
        labels = {}
        graph = self.diagram.diagram_graph
        for edge in graph.edges(data=True):
            labels[(edge[0], edge[1])] = edge[2].get("name", "").replace("\n", " ")
        for node in graph.nodes(data=True):
            labels[node[0]] = node[1].get("node_name", "").replace("\n", " ")
        return labels

    def get_model_title(self) -> str:
        """ Returns the name of the model. """
        return next(iter(self.diagram.process_elements))

    def get_start_events(self) -> tuple:
        """ Returns tuple of start events names. """
        return self.get_node_names_of_type("startEvent")

    def get_end_events(self) -> tuple:
        """ Returns tuple of end events names. """
        return self.get_node_names_of_type("endEvent")

    def get_processes(self) -> tuple:
        """ Returns tuple of all process names. """
        labels = ["task", "process", "subProcess", "intermediateCatchEvent",
                  "intermediateThrowEvent", "boundaryEvent"]
        results = []
        for label in labels:
            results.extend(self.get_node_names_of_type(label))
        return tuple(results)

    def get_gates(self) -> tuple:
        """ Returns tuple of all gate names. """
        labels = ["complexGateway", "eventBasedGateway", "inclusiveGateway", "exclusiveGateway",
                  "parallelGateway"]
        results = []
        for label in labels:
            results.extend(self.get_node_names_of_type(label))
        return tuple(results)

    def get_edges(self) -> tuple[dict[str, str]]:
        """ Returns the tuple of dictionaries containing edge start, end and its name. """
        results = []
        for edge in self.diagram.diagram_graph.edges(data=True):
            edge_name = edge[2].get("name", "") or "Unnamed"
            start_name = self.id_mappings[edge[0]] or "Unnamed"
            end_name = self.id_mappings[edge[1]] or "Unnamed"
            elements = {"start": start_name, "end": end_name, "edge": edge_name}
            results.append(elements)
        return tuple(results)

    def get_node_names_of_type(self, node_type: str) -> tuple:
        """ Returns tuple of nodes of given type. """
        node_ids = self.diagram.get_nodes_id_list_by_type(node_type)
        return tuple(self.id_mappings[node_id] for node_id in node_ids)

    def get_nodes(self) -> tuple[tuple[str, dict]]:
        """
        Returns tuple of pairs [node_name, node_dict].
        Removes unnecessary data according to key_to_remove.
        """
        nodes = self.diagram.get_nodes()
        nodes_data = []
        for _, node_dict in nodes:
            name = node_dict.get(consts.Consts.node_name, "")
            keys_to_remove = (consts.Consts.width, consts.Consts.height, consts.Consts.x,
                              consts.Consts.y, consts.Consts.node_name)
            for key in keys_to_remove:
                try:
                    del node_dict[key]
                except KeyError:
                    pass
            for key, value in node_dict.items():
                if isinstance(value, (list, tuple, set)):
                    value = ", ".join(value)
                node_dict[key] = value or "No data provided."
            nodes_data.append((name, node_dict))
        return tuple(nodes_data)


def generate_pdf_report(bpmn_file: str, wkhtmltopdf_path=None) -> None:
    """ Helper function used to generate pdf report using ReportGenerator class. """
    report_generator = ReportGenerator.from_file(bpmn_file)
    report_generator.generate_pdf_report(wkhtmltopdf_path)


def generate_html_report(bpmn_file: str) -> None:
    """ Helper function used to generate html report using ReportGenerator class. """
    report_generator = ReportGenerator.from_file(bpmn_file)
    report_generator.generate_html_report()
