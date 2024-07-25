import json
from math import radians, sin, cos, asin, sqrt

import folium
import requests

def create_map_with_path(chemin):
    chemin_folium = [(coord[1], coord[0]) for coord in chemin]
    mymap = folium.Map(location=chemin_folium[0], zoom_start=10)
    folium.PolyLine(chemin_folium, color="blue", weight=2.5, opacity=1).add_to(mymap)
    folium.Marker(chemin_folium[0], popup=f"Départ: {coord_to_station_name(chemin_folium[0])}", icon=folium.Icon(color="green")).add_to(mymap)
    folium.Marker(chemin_folium[-1], popup=f"Arrivée: {coord_to_station_name(chemin_folium[-1])}", icon=folium.Icon(color="red")).add_to(mymap)
    for coord in chemin_folium[1:-1]:
        folium.Marker(coord, popup=f"{coord_to_station_name(coord)}", icon=folium.Icon(color="gray")).add_to(mymap)
    mymap.save("chemin_sur_carte_avec_stations.html")

def get_neighbors_from_json():
    with open('tc-trajet-train-statique-sncb.json', 'r') as f:
        data = json.load(f)
    voisins_par_station = {}

    for trajet in data:
        stations = trajet['shape']['geometry']['coordinates'][0]
        for i in range(len(stations)):
            station = tuple(stations[i])
            if station not in voisins_par_station:
                voisins_par_station[station] = []
            if i > 0:
                precedent = tuple(stations[i - 1])
                if precedent not in voisins_par_station[station]:
                    voisins_par_station[station].append(precedent)
            if i < len(stations) - 1:
                suivante = tuple(stations[i + 1])
                if suivante not in voisins_par_station[station]:
                    voisins_par_station[station].append(suivante)
    return voisins_par_station

def change_position(station):
    longitude, latitude = station
    return latitude, longitude

def print_path(chemin, depart, arrivee):
    p = 2
    list_name = []
    depart = change_position(depart)
    arrivee = change_position(arrivee)
    if chemin:
        print(f"Chemin trouvé : ")
        for station in chemin:
            station = change_position(station)
            list_name.append(coord_to_station_name(station))

        for i in range(len(list_name)):
            k = 2
            for j in range(i+1, len(list_name)):
                if list_name[i] == list_name[j]:
                    list_name[j] = f"{list_name[j]} ({k})"
                    k += 1
        for station in list_name:
            if station == coord_to_station_name(depart):
                print(f"Depart : {station}")
            elif station == coord_to_station_name(arrivee):
                print(f"Destination : {station}")
            else:
                print(f"noeud {p}: {station}")
                p += 1
        create_map_with_path(chemin)
    else:
        print("Aucun chemin possible entre ces 2 stations")

# Cache pour stocker les résultats du géocodage inversé
geocoding_cache = {}

def coord_to_station_name(coordinates):
    if coordinates in geocoding_cache:
        return geocoding_cache[coordinates]

    latitude, longitude = coordinates
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'address' in data:
            for key in ['railway', 'village', 'city_district', 'bus_stop', 'subway', 'town']:
                if key in data['address']:
                    station_name = data['address'][key]
                    geocoding_cache[coordinates] = station_name
                    return station_name
        return coordinates
    else:
        print("La requête à l'API de géocodage inversé a échoué avec le code de réponse :", response.status_code)
        return None

def print_queue(queue):
    queuetoprint = []
    for station in queue:
        station = change_position(station)
        queuetoprint.append(coord_to_station_name(station))
    print(queuetoprint)

def distance_cout(station1, station2):
    lat1, lon1 = station1
    lat2, lon2 = station2

    # Convertir les degrés en radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Rayon de la Terre en kilomètres
    rayon_terre = 6371.0

    # Calcul des écarts de latitude et de longitude
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    # Calcul de la distance à vol d'oiseau
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    distance = rayon_terre * c

    return distance

def distance_vol_oiseau(station1, station2):
    x1, y1 = station1
    x2, y2 = station2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

'''def distance_cout(coord1, coord2):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    origins = f"{coord1[1]},{coord1[0]}"
    destinations = f"{coord2[1]},{coord2[0]}"

    params = {
        'origins': origins,
        'destinations': destinations,
        'key': "AIzaSyCDs5xtMgDzxnA_eK6AKXoxEAy-_bmXMVo",
        'units': 'metric'  # pour obtenir la distance en kilomètres
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        elements = data['rows'][0]['elements'][0]
        if elements['status'] == 'OK':
            distance = elements['distance']['value'] / 1000  # convertir de mètres en kilomètres
            return distance
        else:
            raise ValueError(f"Error with element status: {elements['status']}")
    else:
        raise ValueError(f"Error with API request status: {data['status']}")
'''
def temps(distance):
    V = 1
    return distance/V

def get_neighbors_from_json_heur(goal):
    # Charger les données du fichier JSON
    with open('tc-trajet-train-statique-sncb.json', 'r') as f:
        data = json.load(f)
    # Initialiser le dictionnaire pour stocker les voisins de chaque station et les coûts
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
                distance = distance_vol_oiseau(precedent, goal)
                temps_mis = temps(distance)
                voisins_par_station[station].append((precedent, temps_mis))
            if i < len(stations) - 1:
                suivante = tuple(stations[i + 1])  # Station suivante
                distance = distance_vol_oiseau(goal, suivante)
                temps_mis = temps(distance)
                voisins_par_station[station].append((suivante, temps_mis))
    return voisins_par_station

def get_neighbors_from_json_cout(cost_function):
    # Charger les données du fichier JSON
    with open('tc-trajet-train-statique-sncb.json', 'r') as f:
        data = json.load(f)

    # Initialiser le dictionnaire pour stocker les voisins de chaque station et les coûts
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
                cost = temps(cost_function(station, precedent))
                voisins_par_station[station].append((precedent, cost))

            if i < len(stations) - 1:
                suivante = tuple(stations[i + 1])  # Station suivante
                cost = temps(cost_function(station, suivante))
                voisins_par_station[station].append((suivante, cost))

    return voisins_par_station

def memory(algo):
    return print(f"la mémoire utlisée est : {len(algo)}") if algo != None else print("Memoire vide")
