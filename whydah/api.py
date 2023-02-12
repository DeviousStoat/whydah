import requests
from gargle.result import Result, filter_to_result

from whydah.models import Category, PirateTorrent


def data_top_100(category: Category) -> Result[list[PirateTorrent], str]:
    url = f"https://apibay.org/precompiled/data_top100_{category.value}.json"

    return filter_to_result(
        requests.get(url),
        lambda resp: resp.status_code == 200,
        lambda resp: f"Unexpected response:\n[{resp.status_code}] {url}\n{resp.text}",
    ).map(lambda resp: [PirateTorrent.from_json(elem) for elem in resp.json()])


def data_search(
    search: str,
    category: Category = Category.NONE,
) -> Result[list[PirateTorrent], str]:
    url = f"https://apibay.org/q.php?q={search}&cat={category.value}"

    return filter_to_result(
        requests.get(url),
        lambda resp: resp.status_code == 200,
        lambda resp: f"Unexpected response:\n[{resp.status_code}] {url}\n{resp.text}",
    ).map(lambda resp: [PirateTorrent.from_json(elem) for elem in resp.json()])
