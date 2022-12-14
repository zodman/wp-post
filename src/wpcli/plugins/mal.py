import requests

JIKAN_URL = "https://api.jikan.moe/v4/anime/{0}/full"


def fetch(mal_id):
    url = JIKAN_URL.format(mal_id)
    resp = requests.get(url)

    mal_data = resp.json().get("data")

    assert mal_data, "mal_id not found"
    return mal_data
