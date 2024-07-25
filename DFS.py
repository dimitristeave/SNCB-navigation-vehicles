import json
from collections import deque
import folium

# Fonction pour calculer la distance entre deux points géographiques
def distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5

# Fonction pour trouver le chemin entre deux points en utilisant BFS
def dfs(graph, start, end, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    visited.add(start)
    path = path + [start]
    if start == end:
        return path
    for neighbor in graph[start]:
        if neighbor not in visited:
            new_path = dfs(graph, neighbor, end, visited, path)
            if new_path:
                return new_path
    return None

# Fonction pour créer une carte et afficher le chemin avec des marqueurs
def create_map_with_path(chemin):
    # Convertir le chemin en format compatible avec folium
    chemin_folium = [(coord[1], coord[0]) for coord in chemin]

    # Créer une carte centrée sur le premier point du chemin
    mymap = folium.Map(location=chemin_folium[0], zoom_start=10)

    # Ajouter le chemin à la carte en tant que ligne
    folium.PolyLine(chemin_folium, color="blue", weight=2.5, opacity=1).add_to(mymap)

    # Ajouter des marqueurs pour le point de départ et d'arrivée
    folium.Marker(chemin_folium[0], popup=f"Départ: {chemin_folium[0]}", icon=folium.Icon(color="green")).add_to(mymap)
    folium.Marker(chemin_folium[-1], popup=f"Arrivée: {chemin_folium[-1]}", icon=folium.Icon(color="red")).add_to(mymap)

    # Ajouter des marqueurs pour les stations intermédiaires
    for coord in chemin_folium[1:-1]:
        folium.Marker(coord, popup=f"{coord}", icon=folium.Icon(color="gray")).add_to(mymap)

    # Afficher la carte
    mymap.save("chemin_sur_carte_avec_stations.html")

def round_coordinates(coord, decimals=5):
    """Fonction pour arrondir les coordonnées à un nombre fixe de décimales."""
    return round(coord[0], decimals), round(coord[1], decimals)

def get_neighbors_from_json():
    # Charger les données du fichier JSON
    with open('tc-trajet-train-statique-sncb.json', 'r') as f:
        data = json.load(f)
    # Initialiser le dictionnaire pour stocker les voisins de chaque station
    voisins_par_station = {}

    # Parcourir chaque trajet
    for trajet in data:
        stations = trajet['shape']['geometry']['coordinates'][0]  # Coordonnées des stations du trajet
        for i in range(len(stations)):
            station = tuple(stations[i])  # Convertir en tuple
            # Si la station n'est pas déjà dans le dictionnaire, l'ajouter avec une liste vide de voisins
            if station not in voisins_par_station:
                voisins_par_station[station] = []
            # Identifier les stations adjacentes dans le trajet actuel
            if i > 0:
                precedent = tuple(stations[i - 1])  # Station précédente
                if precedent not in voisins_par_station[station]:
                    voisins_par_station[station].append(precedent)
            if i < len(stations) - 1:
                suivante = tuple(stations[i + 1])  # Station suivante
                if suivante not in voisins_par_station[station]:
                    voisins_par_station[station].append(suivante)
    return voisins_par_station

# Exécution du programme
def main():
    i=0
    # Récupérer les voisins de chaque station
    voisins_par_station = get_neighbors_from_json()

    # Spécifier les points de départ et d'arrivée
    depart = (4.17589, 50.65101)
    arrivee = (4.542787, 50.42383)

    # Trouver le chemin entre le point de départ et d'arrivée en utilisant BFS
    chemin = dfs(voisins_par_station, depart, arrivee)

    # Vérifier si un chemin a été trouvé
    if chemin:
        print("Chemin trouvé :")
        for station in chemin:
            if station == depart:
                print(f"Depart : {station}")
            elif station == arrivee:
                print(f"Destination : {station}")
            else:
                print(f"noeud {i}: {station}")
            i += 1
        # Créer une carte et afficher le chemin avec des marqueurs
        create_map_with_path(chemin)
    else:
        print("Aucun chemin trouvé entre les points de départ et d'arrivée.")



# Exécuter le programme
if __name__ == "__main__":
    main()
