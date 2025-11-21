from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Backend" / "data"
GRAPH_JSON_PATH = DATA_DIR / "graph.json"
DEFAULT_START_NODE = "Strt"
DEFAULT_EDGE_STATUS = "open"
