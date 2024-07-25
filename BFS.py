import timeit
from collections import deque
from functions import get_neighbors_from_json, print_path, memory


def bfs(graph, source, goal):
    i = 0
    # File d'attente pour les nœuds à explorer
    queue = deque()
    # Ensemble pour garder une trace des nœuds visités
    visited = set()
    # Dictionnaire pour garder une trace des chemins
    paths = {source: [source]}

    # Ajouter le nœud source à la file d'attente
    queue.append(source)
    # Marquer le nœud source comme visité
    visited.add(source)

    # Parcourir les nœuds dans la file d'attente
    while queue:
        i+=1
        # choix du prochain noeud dans la file
        node = queue.popleft()
        # Si le nœud actuel est le nœud cible, retourner le chemin jusqu'à ce nœud
        if node == goal:
            return paths[node], i
        # Parcourir les voisins du nœud actuel
        for neighbor in graph[node]:
            # Si le voisin n'a pas été visité
            if neighbor not in visited:
                # Ajouter le voisin à la file d'attente
                queue.append(neighbor)
                # Marquer le voisin comme visité
                visited.add(neighbor)
                # Mettre à jour le chemin vers le voisin
                paths[neighbor] = paths[node] + [neighbor]
    # Si aucun chemin n'est trouvé, retourner None
    return None

# Exécution du programme
def main():
    # Récupérer les voisins de chaque station
    voisins_par_station = get_neighbors_from_json()
    # Spécifier les points de départ et d'arrivée
    depart = (4.011095, 51.00315)
    arrivee = (4.266485, 50.7519)
    chemin, i = bfs(voisins_par_station, depart, arrivee)
    print(f"Nombre d'itérations {i}")
    memory(chemin)
    execution_time = round((timeit.timeit(lambda: bfs(voisins_par_station, depart, arrivee), number=1))*1000000, 2)
    print(f"Execution time : {execution_time} µs")
    print_path(chemin, depart, arrivee)

if __name__ == "__main__":
    main()