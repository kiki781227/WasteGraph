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

    def save_to_json_file(self, path=GRAPH_JSON_PATH) -> None:
        data = self.to_json_dict()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def neighbors(self, node_id: str) -> List[Tuple[str, float]]:
        result: List[Tuple[str, float]] = []
        for edge in self.adj.get(node_id, []):
            if edge.get("status", "open") == "open":
                result.append((edge["to"], edge["weight"]))
        return result
    

        
