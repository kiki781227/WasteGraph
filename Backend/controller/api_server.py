from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from backend.model.db import GraphRepository
from backend.model.algorithms import dijkstra, greedy_coloring
from config import DEFAULT_START_NODE


class GraphRequestHandler(BaseHTTPRequestHandler):
    # Pour éviter les logs trop verbeux (optionnel)
    def log_message(self, format, *args):
        return

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/graph":
            self.handle_get_graph()
        elif path == "/shortest-path":
            self.handle_shortest_path(query)
        elif path == "/coloring":
            self.handle_coloring()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_get_graph(self):
        repo = GraphRepository()
        try:
            graph = repo.load_graph()
            # On renvoie les structures internes telles quelles
            data = {
                "nodes": graph.nodes,
                "edges": graph.adj,
            }
            self._send_json(data)
        finally:
            repo.close()

    def handle_shortest_path(self, query):
        # src et dst dans l’URL, ex: /shortest-path?src=Strt&dst=K
        src = query.get("src", [DEFAULT_START_NODE])[0]
        dst_list = query.get("dst")

        if not dst_list:
            self._send_json({"error": "paramètre 'dst' manquant"}, status=400)
            return

        dst = dst_list[0]

        repo = GraphRepository()
        try:
            graph = repo.load_graph()
            dist, path = dijkstra(graph, source=src, target=dst)
            result = {
                "source": src,
                "target": dst,
                "distance": dist.get(dst, float("inf")),
                "path": path,
            }
            self._send_json(result)
        finally:
            repo.close()

    def handle_coloring(self):
        repo = GraphRepository()
        try:
            graph = repo.load_graph()
            colors = greedy_coloring(graph)
            result = {
                "colors": colors
            }
            self._send_json(result)
        finally:
            repo.close()


def run_server(host="127.0.0.1", port=8000):
    httpd = HTTPServer((host, port), GraphRequestHandler)
    print(f"Serveur API sur http://{host}:{port}")
    httpd.serve_forever()
