import requests


backend_url: str = ''


def set_backend_url(url: str) -> None:
    global backend_url
    backend_url = url


def do_request(method: str, uri: str, data=None) -> dict:
    url = backend_url + uri
    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        response = requests.post(url, json=data)
    elif method == "PUT":
        response = requests.put(url, json=data)
    else:
        raise ValueError("Unknown method")

    if response.status_code == 200:
        return response.json()
    else:
        return dict()

