from bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph
from bpmn_python.bpmn_python_consts import Consts

import matplotlib
matplotlib.use('Qt5Agg')

import networkx as nx
import matplotlib.pyplot as plt

bpnm_diagram = BpmnDiagramGraph()
bpnm_diagram.load_diagram_from_xml_file("../examples/01_Obsluga_zgloszen.bpmn")


def visualize_diagram(bpmn_diagram):
    """
    Shows a simple visualization of diagram

    :param bpmn_diagram: an instance of BPMNDiagramGraph class.
    """
    g = bpmn_diagram.diagram_graph
    pos = bpmn_diagram.get_nodes_positions()

    options = {"edgecolors": "black", "node_size": 1500, "node_color": "white"}
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.task), **options, node_shape="s")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.subprocess), **options, node_shape="s")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.complex_gateway), **options, node_shape="d")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.event_based_gateway), **options, node_shape="d")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.inclusive_gateway), **options, node_shape="d")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.exclusive_gateway), **options, node_shape="d")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.parallel_gateway), **options, node_shape="d")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.start_event), **options, node_shape="o")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.intermediate_catch_event), **options, node_shape="s")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.end_event), **options, node_shape="o")
    nx.draw_networkx_nodes(g, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.intermediate_throw_event), **options, node_shape="s")

    # nx.draw_networkx_nodes(g, pos, node_shape='s', node_color='white', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.subprocess))
    # nx.draw_networkx_nodes(g, pos, node_shape='d', node_color='white', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.complex_gateway))
    # nx.draw_networkx_nodes(g, pos, node_shape='o', node_color='black', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.event_based_gateway))
    # nx.draw_networkx_nodes(g, pos, node_shape='s', node_color='white', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.inclusive_gateway))
    # nx.draw_networkx_nodes(g, pos, node_shape='d', node_color='white', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.exclusive_gateway))
    # nx.draw_networkx_nodes(g, pos, node_shape='d', node_color='white', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.parallel_gateway))
    # nx.draw_networkx_nodes(g, pos, node_shape='o', node_color='white', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.start_event))
    # nx.draw_networkx_nodes(g, pos, node_shape='o', node_color='white', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.intermediate_catch_event))
    # nx.draw_networkx_nodes(g, pos, node_shape='o', node_color='white', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.end_event))
    # nx.draw_networkx_nodes(g, pos, node_shape='o', node_color='white', node_size=600,
    #                        nodelist=bpmn_diagram.get_nodes_id_list_by_type(Consts.intermediate_throw_event))



    node_labels = {}
    for node in g.nodes(data=True):
        node_labels[node[0]] = node[1].get(Consts.node_name)
    nx.draw_networkx_labels(g, pos, node_labels, font_size=8)

    nx.draw_networkx_edges(g, pos)

    edge_labels = {}
    for edge in g.edges(data=True):
        edge_labels[(edge[0], edge[1])] = edge[2].get(Consts.name)
    nx.draw_networkx_edge_labels(g, pos, edge_labels, font_size=8)

    plt.show()


visualize_diagram(bpnm_diagram)
