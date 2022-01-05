import datetime

from jinja2 import FileSystemLoader, Environment

from src.bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph


class ReportGenerator:

    def __init__(self, bpmn_diagram: BpmnDiagramGraph):
        self.diagram = bpmn_diagram
        self.file_loader = FileSystemLoader("templates")
        self.env = Environment(loader=self.file_loader)
        self.template_name = "bpmn_report.html"
        self.template = self.env.get_template(self.template_name)
        self.context_generator = ContextGenerator(self.diagram)
        self.report_path = "reports"

    def generate(self):
        context = self.get_context()
        rendered_template = self.template.render(**context)

        with open(self.get_report_path(), "w") as fh:
            fh.write(rendered_template)

    def get_report_path(self) -> str:
        date = datetime.date.today().strftime("%d_%m_%Y")
        return f"{self.report_path}/report_{date}.html"

    def get_image_name(self) -> str:
        date = datetime.date.today().strftime("%d_%m_%Y")
        return f"{self.report_path}/report_{date}_image.jpg"

    def get_context(self):
        context = self.context_generator.get_context()
        context["model_image"] = self.get_image_name()
        return context


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
    report_generator.generate()
