import timeit
from functions import print_path, get_neighbors_from_json_heur, memory

def greedy_search(graph, source, goal):
    i=0
    current_station = source
    visited_stations = [current_station]

    while current_station != goal:
        i+=1
        # Obtenir les voisins de la station actuelle et des stations déjà visitées
        all_neighbors = [graph[station] for station in visited_stations]
        # Concaténer tous les voisins dans une seule liste
        all_neighbors = [neighbor for neighbors_list in all_neighbors for neighbor in neighbors_list]
        #print(f"all neighbors : {all_neighbors}")

        # Ajouter également les voisins de la station actuelle
        #all_neighbors += graph[current_station]

        # Ressortir les voisins et parmi eux filtrer les voisins qui n'ont pas déjà été visités
        unvisited_neighbors = [(neighbor, distance) for neighbor, distance in all_neighbors if
                               neighbor not in visited_stations]
        #print(f"all unvisited neighbors : {all_neighbors}")
        if not unvisited_neighbors:
            break  # Si aucun voisin non visité n'est disponible, arrêter la recherche

        # Choisir la station voisine la plus proche
        next_station, min_temps = min(unvisited_neighbors, key=lambda x: x[1])

        # Mettre à jour la station actuelle
        current_station = next_station
        #print(f"current station : {current_station}")
        visited_stations.append(current_station)
        #print(f"visited stations: {visited_stations}")
    # la liste des statons visitées constituent le chemin resultant car l'algorithme ne vidite que les chemin sélectionnés
    return visited_stations, i

def main():
    # Spécifier les points de départ et d'arrivée
    depart = (4.011095, 51.00315)
    arrivee = (4.266485, 50.7519)
    voisins_par_station = get_neighbors_from_json_heur(arrivee)
    execution_time = round((timeit.timeit(lambda: greedy_search(voisins_par_station, depart, arrivee), number=1)) * 1000000, 2)
    print(f"Execution time : {execution_time} µs")
    chemin, i = greedy_search(voisins_par_station, depart, arrivee)
    print(f"Nombre d'itérations {i}")
    memory(chemin)
    print_path(chemin, depart, arrivee)


# Exécuter le programme
if __name__ == "__main__":
    main()
