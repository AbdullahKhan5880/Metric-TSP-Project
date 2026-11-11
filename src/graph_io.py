
import json
from pathlib import Path

import networkx as nx


def save_graph(graph, file_path):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.suffix == ".graphml":
        graph_copy = graph.copy()

        for node, attributes in graph_copy.nodes(data=True):
            if "pos" in attributes:
                attributes["pos"] = json.dumps(list(attributes["pos"]))

        nx.write_graphml(graph_copy, file_path)

    elif file_path.suffix == ".json":
        data = {
            "nodes": [
                {
                    "id": node,
                    "pos": list(attributes["pos"]) if "pos" in attributes else None
                }
                for node, attributes in graph.nodes(data=True)
            ],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    "weight": float(attributes["weight"])
                }
                for u, v, attributes in graph.edges(data=True)
            ]
        }

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    else:
        raise ValueError("Supported formats are .graphml and .json.")


def load_graph(file_path):
    file_path = Path(file_path)

    if file_path.suffix == ".graphml":
        graph = nx.read_graphml(file_path)

        for node, attributes in graph.nodes(data=True):
            if "pos" in attributes:
                position = json.loads(attributes["pos"])
                graph.nodes[node]["pos"] = tuple(position)

        for _, _, attributes in graph.edges(data=True):
            if "weight" in attributes:
                attributes["weight"] = float(attributes["weight"])

        return graph

    if file_path.suffix == ".json":
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        graph = nx.Graph()

        for node in data["nodes"]:
            attributes = {}

            if node["pos"] is not None:
                attributes["pos"] = tuple(node["pos"])

            graph.add_node(node["id"], **attributes)

        for edge in data["edges"]:
            graph.add_edge(
                edge["source"],
                edge["target"],
                weight=float(edge["weight"])
            )

        return graph

    raise ValueError("Supported formats are .graphml and .json.")
