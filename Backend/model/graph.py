from config import GRAPH_JSON_PATH
import json
from typing import Dict, List, Tuple

class Graph:
    def __init__(self) -> None:
        self.nodes: Dict[str, Dict] = {}
        self.adj: Dict[str, List[Dict]] = {}

    def load_from_json_file(self, path=GRAPH_JSON_PATH) -> None:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.nodes = data.get("nodes", {})
        self.adj = data.get("edges", {})

    def to_json_dict(self) -> Dict:
        return {
            "nodes": self.nodes,
            "edges": self.adj
        }
    
    def neighbors(self, node_id: str) -> List[Tuple[str, float]]:
        result: List[Tuple[str, float]] = []
        for edge in self.adj.get(node_id, []):
            result.append((edge["to"], edge["weight"]))
        return result
    

    def add_node(self, node_id: str, x: int, y: int) -> None:
        if node_id not in self.nodes:
            self.nodes[node_id] = {"x": x, "y": y}
            self.adj.setdefault(node_id, [])

    def add_edge(
        self,
        u: str,
        v: str,
        weight: float,
        bidirectional: bool = True
    ) -> None:
        self.adj.setdefault(u, [])
        self.adj[u].append({"to": v, "weight": weight})
        if bidirectional:
            self.adj.setdefault(v, [])
            self.adj[v].append({"to": u, "weight": weight})
    


 
