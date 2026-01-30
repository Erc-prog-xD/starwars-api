import requests


def fetch_data(resource):

    url = f"https://swapi.dev/api/{resource}/"
    response = requests.get(url)
    return response.json()["results"]
