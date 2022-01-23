from src.bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph
import bpmn_python.bpmn_python_consts as consts


class BpmnPrinter:

    def __init__(self, bpmn_diagram: BpmnDiagramGraph):
        self.diagram = bpmn_diagram
        self.id_mappings = self.get_id_mappings()

    def print(self) -> str:
        lines = [f"Components of the BPMN diagram:"]
        nodes = (
            "startEvent", "endEvent", "intermediateCatchEvent", "intermediateThrowEvent", "task",
            "subProcess", "complexGateway", "eventBasedGateway", "inclusiveGateway",
            "exclusiveGateway", "parallelGateway"
        )
        lines.append(self.get_nodes_representation(nodes))
        lines.append(self.get_edges_representation())
        lines.append(self.get_nodes_details())
        return "\n".join(lines)

    def get_nodes_representation(self, nodes: list | tuple) -> str:
        lines = []
        for node_type in nodes:
            line = self.print_node_type(node_type)
            if line:
                lines.append(line)
        return "\n".join(lines)

    def get_edges_representation(self) -> str:
        lines = ["\nEdges:"]
        for idx, edge in enumerate(self.diagram.diagram_graph.edges(data=True)):
            lines.append(self.get_edge_representation(idx, edge))
        return "\n".join(lines)

    def get_edge_representation(self, idx: int, edge: tuple[str, str, dict]) -> str:
        edge_name = edge[2].get("name", "") or "Unnamed"
        start_name = self.id_mappings[edge[1]] or "Unnamed"
        end_name = self.id_mappings[edge[0]] or "Unnamed"
        index = f"{idx:2}. {edge_name}: "
        line = f"{index:20}{start_name} -> {end_name}"
        return line

    def print_node_type(self, node_type: str) -> str:
        key, values = self.get_node_names_of_type(node_type)
        if not values:
            return ""
        lines = [f"{key}:"]
        for idx, value in enumerate(values):
            lines.append(f"  {idx:2}. {value}")
        return "\n".join(lines)

    def get_node_names_of_type(self, node_type: str) -> tuple[str, tuple]:
        node_ids = self.diagram.get_nodes_id_list_by_type(node_type)
        return node_type, tuple(self.id_mappings[node_id] for node_id in node_ids)

    def get_id_mappings(self) -> dict:
        labels = {}
        graph = self.diagram.diagram_graph
        for edge in graph.edges(data=True):
            labels[(edge[0], edge[1])] = edge[2].get("name", "").replace("\n", " ")
        for node in graph.nodes(data=True):
            labels[node[0]] = node[1].get("node_name", "").replace("\n", " ")
        return labels

    def get_nodes_details(self):
        nodes_data = self.get_nodes_data()
        nodes = []
        for node_data in nodes_data:
            lines = [f"Node name: {node_data.pop('node_name')}"]
            for key, value in node_data.items():
                value = str(value)
                line = f"\t{key:>20} {value:>60}"
                lines.append(line)
            nodes.append("\n".join(lines))
        return "\n\n".join(nodes)

    def get_nodes_data(self):
        nodes = self.diagram.get_nodes()
        nodes_data = []
        for node_id, node_dict in nodes:
            keys_to_remove = (consts.Consts.width, consts.Consts.height, consts.Consts.x,
                              consts.Consts.y)
            for key in keys_to_remove:
                try:
                    del node_dict[key]
                except KeyError:
                    pass
            for key, value in node_dict.items():
                node_dict[key] = value or "No data provided."
            nodes_data.append(node_dict)
        return nodes_data

if __name__ == '__main__':
    bpnm_diagram = BpmnDiagramGraph()
    bpnm_diagram.load_diagram_from_xml_file("../examples/01_Obsluga_zgloszen.bpmn")
    printer = BpmnPrinter(bpnm_diagram)
    print(printer.print())
    # printer.get_nodes_details()
