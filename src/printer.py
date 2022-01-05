from src.bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph


class BpmnPrinter:

    def __init__(self, bpmn_diagram: BpmnDiagramGraph):
        self.diagram = bpmn_diagram
        self.id_mappings = self.get_id_mappings()

    def print(self):
        lines = [f"Components of the BPMN diagram:"]
        for node_type in ("startEvent", "endEvent"):
            lines.append(self.print_node_type(node_type))
        return "\n".join(lines)

    def print_node_type(self, node_type: str):
        key, values = self.get_node_names_of_type(node_type)
        lines = [f"{key}:"]
        for idx, value in enumerate(values):
            lines.append(f"  {idx}. {value}")
        return "\n".join(lines)

    def get_node_names_of_type(self, node_type: str):
        node_ids = self.diagram.get_nodes_id_list_by_type(node_type)
        return node_type, (self.id_mappings[node_id] for node_id in node_ids)

    def get_id_mappings(self):
        labels = {}
        graph = self.diagram.diagram_graph
        for edge in graph.edges(data=True):
            labels[(edge[0], edge[1])] = edge[2].get("name", "").replace("\n", " ")
        for node in graph.nodes(data=True):
            labels[node[0]] = node[1].get("node_name", "").replace("\n", " ")
        return labels


bpnm_diagram = BpmnDiagramGraph()
bpnm_diagram.load_diagram_from_xml_file("../examples/01_Obsluga_zgloszen.bpmn")
printer = BpmnPrinter(bpnm_diagram)
print(printer.print())
