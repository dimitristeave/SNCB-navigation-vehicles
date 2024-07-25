import timeit

from functions import distance_cout, distance_vol_oiseau, print_path, get_neighbors_from_json_cout, memory
from queue import PriorityQueue

def astar(graph, start, goal, heuristic):
    # Initialisation des variables
    i = 0  # Compteur d'itérations
    temps = 0  # Coût total du chemin trouvé
    open_set = PriorityQueue()  # File de priorité pour les nœuds à explorer
    open_set.put((0, start))  # Ajouter le nœud de départ avec un coût initial de 0
    came_from = {}  # Dictionnaire pour reconstruire le chemin
    g_score = {node: float('inf') for node in graph}  # Coût pour atteindre chaque nœud depuis le départ
    g_score[start] = 0  # Le coût pour atteindre le départ est 0
    f_score = {node: float('inf') for node in graph}  # Estimation du coût total du départ à l'objectif passant par chaque nœud
    f_score[start] = heuristic(start, goal)  # Estimation initiale pour le nœud de départ
    closed_set = set()  # Ensemble des nœuds déjà évalués

    # Boucle principale de l'algorithme A*
    while not open_set.empty():
        # Récupérer le nœud avec le coût f le plus bas
        _, current = open_set.get()
        i += 1  # Incrémenter le compteur d'itérations

        # Si l'objectif est atteint, reconstruire le chemin
        if current == goal:
            path = []  # Liste pour stocker le chemin
            while current in came_from:
                path.append(current)
                current = came_from[current]
                temps += g_score[current]  # Ajouter le coût du chemin
            path.append(start)  # Ajouter le nœud de départ
            path.reverse()  # Inverser le chemin pour obtenir l'ordre correct
            return path, temps, i  # Retourner le chemin, le coût total et le nombre d'itérations

        closed_set.add(current)  # Ajouter le nœud courant aux nœuds évalués

        # Examiner les voisins du nœud courant
        for neighbor, cost in graph[current]:
            if neighbor in closed_set:
                continue  # Ignorer les voisins déjà évalués

            # Calculer le coût g provisoire pour atteindre le voisin
            tentative_g_score = g_score[current] + cost

            # Si le nouveau coût g est inférieur au coût g enregistré pour le voisin
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                # Mettre à jour le chemin et les scores pour le voisin
                came_from[neighbor] = current  # Enregistrer le nœud courant comme prédécesseur
                g_score[neighbor] = tentative_g_score  # Mettre à jour le coût g pour le voisin
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)  # Calculer le nouveau coût f
                open_set.put((f_score[neighbor], neighbor))  # Ajouter le voisin à la file de priorité

    return None  # Si aucun chemin n'est trouvé, retourner None

depart = (4.055451, 50.91962)
arrivee = (4.266485, 50.7519)
graph = get_neighbors_from_json_cout(distance_cout)
path, temps, i = astar(graph, depart, arrivee, distance_vol_oiseau)
print(f"Nombre d'itérations {i}")
execution_time = round((timeit.timeit(lambda: astar(graph, depart, arrivee, distance_vol_oiseau), number=1)) * 1000000, 2)
print(f"Execution time : {execution_time} µs")
h = int(temps//60)
m = int(temps%60)
print(f"le chemin trouvé dure {h} h {m} min")
memory(path)
print_path(path, depart, arrivee)