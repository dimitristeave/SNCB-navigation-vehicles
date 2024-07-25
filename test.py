import requests


def get_distance_between_coordinates(coord1, coord2):
    """
    Calcule la distance réelle entre deux points géographiques en utilisant l'API Google Maps Distance Matrix.

    :param coord1: tuple contenant (latitude, longitude) du premier point
    :param coord2: tuple contenant (latitude, longitude) du second point
    :param api_key: clé API Google Maps
    :return: distance entre les deux points en kilomètres
    """
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


# Exemple d'utilisation
coord1 = (4.011095, 51.00315)  # Paris (latitude, longitude)
coord2 = (4.266485, 50.7519)  # Lyon (latitude, longitude)
api_key = 'AIzaSyCDs5xtMgDzxnA_eK6AKXoxEAy-_bmXMVo'

try:
    distance = get_distance_between_coordinates(coord1, coord2)
    print(f"La distance entre Paris et Lyon est de {distance:.2f} km.")
except ValueError as e:
    print(e)
