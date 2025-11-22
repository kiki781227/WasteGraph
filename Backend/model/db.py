import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from backend.model.graph import Graph


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


class GraphRepository:


    def __init__(self, conn=None):
        self.conn = conn or get_connection()

    def close(self):
        self.conn.close()

    def load_graph(self) -> Graph:
        g = Graph()

        with self.conn.cursor() as cur:
            # Charger les noeuds
            cur.execute("SELECT id, x, y FROM nodes;")
            for node_id, x, y in cur.fetchall():
                g.nodes[node_id] = {"x": x, "y": y}
                g.adj.setdefault(node_id, [])

            # Charger les arêtes
            cur.execute(
                "SELECT from_id, to_id, weight FROM edges;"
            )
            for from_id, to_id, weight in cur.fetchall():
                g.adj.setdefault(from_id, []).append(
                    {"to": to_id, "weight": weight}
                )

        return g

    def save_graph(self, graph: Graph):
        with self.conn.cursor() as cur:
            # On vide puis on réinsère (simple pour ton projet)
            cur.execute("DELETE FROM edges;")
            cur.execute("DELETE FROM nodes;")

            # Nodes
            for node_id, data in graph.nodes.items():
                cur.execute(
                    "INSERT INTO nodes (id, x, y) VALUES (%s, %s, %s);",
                    (node_id, data.get("x"), data.get("y")),
                )

            # Edges
            for from_id, edges in graph.adj.items():
                for edge in edges:
                    cur.execute(
                        """
                        INSERT INTO edges (from_id, to_id, weight)
                        VALUES (%s, %s, %s);
                        """,
                        (from_id, edge["to"], edge["weight"]),
                    )

        self.conn.commit()



