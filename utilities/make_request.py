"""Tool to help make requests"""

import requests
import json


def make_request(endpoint: str, method: str, **kwargs):
    """
    Function which handles the request process.
    """

    response = requests.request(method=method, url=endpoint, **kwargs)

    if response.status_code not in [200, 201]:
        raise ValueError(
            f"There is an issue with the request: {response.text}\
            Endpoint: {endpoint}\n\
            Method: {method}\n\
            Kwargs: {kwargs}"
        )

    # Setup whether to get content or text.
    if response.headers["content-Type"] == "binary/octet-stream":
        data = response.content

    else:
        try:
            data = json.loads(response.text)
        except:
            data = json.dumps(response.text)

    return data
