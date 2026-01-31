import requests


def apply_filters(data, filters):
    for key, value in filters.items():
        data = [
            item for item in data
            if value.lower() in str(item.get(key, "")).lower()
        ]
    return data


def apply_exact_filters(data, filters):
    for key, value in filters.items():
        data = [
            item for item in data
            if str(item.get(key, "")).lower() == str(value).lower()
        ]
    return data

def filter_no_gender(data):
    return [
        person for person in data
        if person.get("gender", "").lower() not in ("male", "female")
    ]

EXACT_FIELDS = {"gender", "birth_year"}

def apply_smart_filters(data, filters):
    for key, value in filters.items():
        if value is None:
            continue

        value = str(value).lower()

        if key in EXACT_FIELDS:
            data = [
                item for item in data
                if str(item.get(key, "")).lower() == value
            ]
        else:
            data = [
                item for item in data
                if value in str(item.get(key, "")).lower()
            ]

    return data

_url_cache: dict[str, dict] = {}

def fetch_by_url(url: str) -> dict:
    if url not in _url_cache:
        response = requests.get(url)
        response.raise_for_status()
        _url_cache[url] = response.json()
    return _url_cache[url]