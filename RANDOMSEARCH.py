import random
import timeit
from collections import deque
from functions import get_neighbors_from_json, print_path, memory


def random_search(graph, source, goal):
    i = 0
    # File d'attente pour les nœuds à explorer
    queue = deque()
    # Ensemble pour garder une trace des nœuds visités
    visited = set()
    # Ajouter le nœud source à la file d'attente
    queue.append(source)
    # Marquer le nœud source comme visité
    visited.add(source)
    # Dictionnaire pour garder une trace des chemins
    path = {source: [source]}

    while queue:
        i += 1
        # choix du prochain noeud dans la file
        current_station = queue.popleft()
        # Si le nœud actuel est le nœud cible, retourner le chemin jusqu'à ce nœud
        if current_station == goal:
            return path[current_station], i
        # recuperation des voisins du noeud en cours
        neighbors = graph[current_station]
        if not neighbors:
            break
        # parcours des voisins du noeud en cours
        for neighbor in neighbors:
            if neighbor not in visited:
                # Ajouter le voisin à une position aléatoire dans la file d'attente
                position = random.randint(0, len(queue))
                queue.insert(position, neighbor)
                visited.add(neighbor)
                path[neighbor] = path[current_station] + [neighbor]

    return None

# Exécution du programme
def main():
    #Récupérer les voisins de chaque station
    voisins_par_station = get_neighbors_from_json()
    # Spécifier les points de départ et d'arrivée
    depart = (4.011095, 51.00315)
    arrivee = (4.266485, 50.7519)
    chemin, i = random_search(voisins_par_station, depart, arrivee)
    memory(chemin)
    execution_time = round((timeit.timeit(lambda: random_search(voisins_par_station, depart, arrivee), number=1)) * 1000000,2)
    print(f"Execution time : {execution_time} µs")
    print(f"Nombre d'itérations {i}")
    print_path(chemin, depart, arrivee)

# Exécuter le programme
if __name__ == "__main__":
    main()