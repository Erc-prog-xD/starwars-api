import requests
_URL_CACHE: dict[str, dict] = {}


def fetch_data(resource):

    url = f"https://swapi.dev/api/{resource}/"
    response = requests.get(url)
    return response.json()["results"]



def fetch_data_by_id(resource, id):
    url = f"https://swapi.dev/api/{resource}/{id}"
    response = requests.get(url)
    return response.json()


def fetch_by_url(url: str) -> dict:
    if url not in _URL_CACHE:
        response = requests.get(url)
        response.raise_for_status()
        _URL_CACHE[url] = response.json()
    return _URL_CACHE[url]