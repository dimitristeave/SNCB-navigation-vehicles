import timeit
from collections import deque
from functions import print_path, get_neighbors_from_json_heur, memory


# Fonction de recherche avec beam search adaptée
def beam_search(graph, source, goal, beta):
    i=0
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
        # Beam Search : Utiliser seulement les meilleurs nœuds selon la largeur donnée
        # Copier les beta meilleurs noeuds dans une nouvelle liste
        best_nodes = []
        for _ in range(min(beta, len(queue))):  # Assurez-vous que nous n'essayons pas de retirer plus d'éléments qu'il n'y en a dans la file d'attente
            best_nodes.append(queue.popleft())

        # Sélectionner les voisins de tous les meilleurs nœuds
        neighbors = []
        for node in best_nodes:
            neighbors.extend(graph[node])

        # Sélectionner les meilleurs voisins parmi tous les voisins
        sorted_neighbors = sorted(neighbors, key=lambda x: x[1])[:beta]

        # Parcourir les meilleurs voisins
        for neighbor, temps in sorted_neighbors:
            # Si le voisin n'a pas été visité
            if neighbor not in visited:
                # Ajouter le voisin à la file d'attente
                queue.append(neighbor)
                # Marquer le voisin comme visité
                visited.add(neighbor)
                # Mettre à jour le chemin vers le voisin
                paths[neighbor] = paths[node] + [neighbor]
                if neighbor == goal:
                    return paths[neighbor], i
    # Si aucun chemin n'est trouvé, retourner None
    return None

def main():
    # Coordonnées des points de départ et d'arrivée
    depart = (4.5433, 50.89307)
    arrivee = (4.222719, 50.95495)
    # Largeur de la recherche
    largeur = 2
    # Calcul des voisins pour le point d'arrivée
    voisins = get_neighbors_from_json_heur(arrivee)
    chemin, i = beam_search(voisins, depart, arrivee, largeur)
    print(f"Nombre d'itérations {i}")
    execution_time = round((timeit.timeit(lambda: beam_search(voisins, depart, arrivee, largeur), number=1)) * 1000000, 2)
    print(f"Execution time : {execution_time} µs")
    memory(chemin)
    print_path(chemin, depart, arrivee)

# Exécuter le programme
if __name__ == "__main__":
    main()