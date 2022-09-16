"""Program to collect latest twitch clips from top streamers, compile into video and post to youtube"""
import os
import json
import pandas as pd
import requests
from dotenv import load_dotenv


# Import the required environment variables
twitch_client_id = os.getenv("twitch_client_id")
twitch_client_secret = os.getenv("twitch_client_secret")


# TODO: create a function which makes a request
def make_request(endpoint: str, method: str, **kwargs):
    """
    Function which handles the request process
    """

    response = requests.request(method=method, url=endpoint, **kwargs)

    if response.status_code not in [200, 201]:
        raise ValueError(f"There is an issue with the request: {response.text}")
    else:
        try:
            data = json.loads(response.text)
        except:
            data = json.dumps(response.text)

    return data


# TODO: Create a class for twitch api access.
# TODO: Setup authentication
# TODO: Create a function which gets the top streamers in a category
# TODO: Create a function which gets the most popular? recent clip from each streamer
# TODO:
# TODO:


class TwitchAPI:
    """Class to interact with Twitch"""

    def __init__(self, client_id, client_secret, url="https://id.twitch.tv"):
        self.url = url
        self.access_token = self.get_authentication()

    def get_authentication(self):
        """
        Function which gets the authentication token when provided credentials
        """

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = f"client_id={twitch_client_id}&client_secret={twitch_client_secret}&grant_type=client_credentials"

        response = make_request(
            endpoint=f"{self.url}/oauth2/token",
            method="POST",
            data=data,
            headers=headers,
        )

        return response["access_token"]

    def get_clips(self):
        """
        Function to return a list of clips???
        """

        response = make_request(
            endpoint=f"{self.url}/oauth2/token",
            method="POST",
            data=data,
            headers=headers,
        )
        return


# TODO: Create a class for video editing/appending.
# TODO: Create a function which conjoins clips/videos


# TODO: Create a class for youtube api access.
# TODO: Setup authentication
# TODO: Create function which uploads video to youtube
# TODO:
# TODO:


TwitchAPI(
    client_id=twitch_client_id,
    client_secret=twitch_client_secret,
)
