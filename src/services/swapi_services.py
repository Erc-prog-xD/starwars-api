import requests
_URL_CACHE: dict[str, dict] = {}


SWAPI_CACHE: dict[str, list[dict]] = {
    "people": [],
    "planets": [],
    "films": [],
    "species": [],
    "starships": [],
    "vehicles": [],
}

def fetch_data(resource: str) -> list[dict]:
    return SWAPI_CACHE.get(resource, [])

def _fetch_all_pages(resource: str) -> list[dict]:
    url = f"https://swapi.dev/api/{resource}/"
    results: list[dict] = []

    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        results.extend(data.get("results", []))
        url = data.get("next")

    return results


def load_swapi_cache() -> None:
    for resource in SWAPI_CACHE:
        if not SWAPI_CACHE[resource]:  # só carrega se estiver vazio
            SWAPI_CACHE[resource] = _fetch_all_pages(resource)


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

def extract_id_from_url(url: str | None) -> int:
    if not url:
        return 0
    return int(url.rstrip("/").split("/")[-1])
