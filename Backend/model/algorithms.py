from typing import Dict, List, Tuple, Optional
from backend.model.graph import Graph
import math


def dijkstra(
    graph: Graph,
    source: str,
    target: Optional[str] = None,
    contrainte: Optional[Dict[str, Dict[str, float]]] = None,
) -> Tuple[Dict[str, float], List[str]]:


    # 1) Initialisation
    dist: Dict[str, float] = {node: float("inf") for node in graph.nodes}
    prev: Dict[str, Optional[str]] = {node: None for node in graph.nodes}
    print("Initial previous  :", prev)
    dist[source] = 0.0
    print("Initial distances :", dist)

    unvisited = set(graph.nodes.keys())
    print("Noeuds non visités :", unvisited)

    # 2) Boucle principale
    while unvisited:
        current = None
        for node in unvisited:
            if current is None or dist[node] < dist[current]:
                current = node

        if current is None:
            break

        if dist[current] == float("inf"):
            break

        if target is not None and current == target:
            break

        unvisited.remove(current)

        # Parcours des voisins
        for neighbor, weight in graph.neighbors(current):
            # print("Les voisins de", current, ":", list(graph.neighbors(current)))
            # Pénalité éventuelle
            extra = 0.0
            if contrainte is not None:
                extra = contrainte.get(current, {}).get(neighbor, 0.0)

            new_dist = dist[current] + weight + extra

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current

    # 3) Reconstruction du chemin si target est donné
    path: List[str] = []
    if target is not None and dist[target] < math.inf:
        cur = target
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()

    return dist, path


def greedy_coloring(graph: Graph) -> Dict[str, str]:

    # 1) Calcul des degrés
    degres = {node: len(graph.adj.get(node, [])) for node in graph.nodes}
    deg_max = max(degres.values()) if degres else 0
    print("Degrés :", degres)
    print("Degré max :", deg_max)

    # 2) Palette de couleurs (tu peux adapter)
    couleurs = ["rouge", "bleu", "vert", "jaune", "violet", "orange", "rose", "cyan"]

    color_assignment: Dict[str, str] = {}

    # 3) Parcours des sommets (tu peux trier par degré décroissant si tu veux améliorer)
    for node in graph.nodes:
        # Récupérer la liste des voisins
        voisins = [edge["to"] for edge in graph.adj.get(node, [])]

        # Couleurs déjà prises par les voisins
        couleurs_voisins = set()
        for voisin in voisins:
            if voisin in color_assignment:
                couleurs_voisins.add(color_assignment[voisin])

        # Choisir la première couleur disponible
        for couleur in couleurs:
            if couleur not in couleurs_voisins:
                color_assignment[node] = couleur
                break

    return color_assignment

