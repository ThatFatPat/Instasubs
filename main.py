from flask import request, Flask, Response
import requests
import time

app = Flask(__name__)
app.url_map.strict_slashes = False

BAZARR_DETAILS = {
    "headers": {
        "X-API-KEY": "8c574419651a2223235e6f15ab5d516e",
    },
    "route": "http://localhost:6767/"
}


def send_request(route, extra_headers, body_dict):
    headers = {'User-Agent': 'PostmanRuntime/7.28.2', 'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive'}
    headers.update(extra_headers)
    print(
        f"{route}\n{headers}\n{body_dict}")
    resp = requests.request(
        method='POST',
        url=route,
        headers=headers,
        files=body_dict
    )

    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    resp.raise_for_status()


def send_bazarr_request(endpoint, body_dict):
    return send_request(BAZARR_DETAILS['route'] + endpoint, BAZARR_DETAILS['headers'], body_dict)


@app.route("/update_bazarr", methods=['POST'])
def update_bazarr():

    send_bazarr_request(
        'api/system/tasks', {"taskid": (None, "update_movies")})
    send_bazarr_request(
        'api/system/tasks', {"taskid": (None, "update_series")})
    time.sleep(3)

    send_bazarr_request(
        'api/system/tasks', {"taskid": (None, "sync_episodes")})
    time.sleep(3)

    send_bazarr_request(
        'api/system/tasks', {"taskid": (None, "wanted_search_missing_subtitles_series")})
    send_bazarr_request(
        'api/system/tasks', {"taskid": (None, "wanted_search_missing_subtitles_movies")})
    return '', 200
