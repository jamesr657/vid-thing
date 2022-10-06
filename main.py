"""Program to collect latest twitch clips from top streamers, compile into video and post to youtube"""
import os
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv

from utilities.make_request import make_request
from utilities.web_scraper import get_webpage_data

# Import the required environment variables
load_dotenv()
twitch_client_id = os.getenv("twitch_client_id")
twitch_client_secret = os.getenv("twitch_client_secret")
chrome_webdriver = os.getenv("chrome_webdriver")

# TODO: Create a class for twitch api access.
# TODO: Setup authentication
# TODO: Create a function which gets the top streamers in a category
# TODO: Create a function which gets the most popular? recent clip from each streamer
# TODO:
# TODO:


class TwitchAPI:
    """Class to interact with TwitchAPI"""

    def __init__(
        self,
        client_id,
        client_secret,
        url=["https://id.twitch.tv", "https://api.twitch.tv"],
    ):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.access_token = self.get_authentication()

    def get_authentication(self):
        """
        Function which gets the authentication token when provided credentials

        Args:
            self

        Returns:
            access_token: [str]
        """

        data = f"client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials"

        dto = make_request(
            endpoint=f"{self.url[0]}/oauth2/token",
            method="POST",
            data=data,
            headers=self.headers,
        )

        return dto["access_token"]

    def get_top_games(self, records):
        """
        Function to get a list of the most popular twitch games

        Args:
            self
            records: [int] Number of categories to show

        Returns:
            df: [pd.DataFrame] containing name and id
        """

        params = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
        }

        dto = make_request(
            endpoint=f"{self.url[1]}/helix/games/top?first={records}",
            method="GET",
            headers=params,
        )
        df = pd.DataFrame(dto["data"])[["id", "name"]]
        df["id"] = df["id"].astype(int)

        return df

    def get_game_id(self, game_name):
        """
        Function which returns the id of the specified game

        Args:
            self
            game_name: [str] the game name.

        Returns:
            df [pd.DataFrame] containing the id and name of game.
        """

        params = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
        }

        dto = make_request(
            endpoint=f"{self.url[1]}/helix/games?name={game_name}",
            method="GET",
            headers=params,
        )
        df = pd.DataFrame(dto["data"])[["id", "name"]]
        df["id"] = df["id"].astype(int)
        df = df.rename(columns={"id": "game_id"})
        return df

    def get_clips(self, game_info):
        """
        Function to return a list of clips

        Args:
            self
            game_data: [pd.DataFrame] a dataframe containing game id's

        Returns:
            df [pd.DataFrame] containing information
        """

        # Create start/end times based on UTC+0, this is what Twitch uses.
        time_start = (datetime.now() - timedelta(days=1, hours=10)).strftime(
            "%Y-%m-%dT%H:00:00.00Z"
        )
        time_end = (datetime.now() - timedelta(hours=10)).strftime(
            "%Y-%m-%dT%H:00:00.00Z"
        )

        df = pd.DataFrame()

        params = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
        }
        for game_id in game_info["game_id"].to_list():

            dto = make_request(
                endpoint=f"{self.url[1]}/helix/clips?game_id={game_id}&started_at={time_start}&ended_at={time_end}&first={100}",
                method="GET",
                headers=params,
            )
            df = pd.concat([df, pd.DataFrame(dto["data"])])

        # Only return english clips.
        df = df[df["language"] == "en"]
        df = df.drop(columns={"embed_url", "thumbnail_url", "vod_offset", "id"})

        # Add game name to the df.
        df["game_id"] = df["game_id"].astype(int)

        df = df.merge(game_info.rename(columns={"name": "game_name"}), on="game_id")

        return df

    def download_clips(self, df):
        """
        Function which downloads the clips

        Args:
            self
            df: [pd.DataFrame] containing required info.

        Returns:
            videos stored in a folder??

        """

        r = requests.get(
            "https://clips.twitch.tv/clips/DeafIgnorantEyeballCorgiDerp-KBkCq0lGvGID56k-"
        )

        # create beautiful-soup object
        soup = BeautifulSoup(r.content, "html.parser")

        # find all links on web-page

        return soup


# TODO: Create a class for video editing/appending.
# TODO: Create a function which conjoins clips/videos


# TODO: Create a class for youtube api access.
# TODO: Setup authentication
# TODO: Create function which uploads video to youtube
# TODO:
# TODO:


# a = TwitchAPI(client_id=twitch_client_id, client_secret=twitch_client_secret)
# b = a.get_top_games(records=25)
# c = a.get_clips(b)
# d = a.get_game_id(game_name="League of Legends")
# e = a.get_clips(d)
# f = a.download_clips(e)
g = get_webpage_data(
    url="https://clips.twitch.tv/DeafIgnorantEyeballCorgiDerp-KBkCq0lGvGID56k-",
    webdriver_path=r"C:\Users\James\Documents\Code\vid-thing\chromedriver.exe",
    # webdriver_path=r"C:\Users\James\Documents\Code\vid-thing\geckodriver.exe",
)

# This is the url from the returned scraper. it doesnt work for some reason
# f = r"https://production.assets.clips.twitchcdn.net/65Rr9SgZAqtJRrxiA-epPg/AT-cm%7C65Rr9SgZAqtJRrxiA-epPg.mp4?sig=cc0666844033c10cebdb78a594546c05f13d0238&amp;token=%7B%22authorization%22%3A%7B%22forbidden%22%3Afalse%2C%22reason%22%3A%22%22%7D%2C%22clip_uri%22%3A%22https%3A%2F%2Fproduction.assets.clips.twitchcdn.net%2F65Rr9SgZAqtJRrxiA-epPg%2FAT-cm%257C65Rr9SgZAqtJRrxiA-epPg.mp4%22%2C%22device_id%22%3A%22a5a74de87f6b6cc8%22%2C%22expires%22%3A1664106550%2C%22user_id%22%3A%22%22%2C%22version%22%3A2%7D"

# This is the url from inspect
f = r"https://production.assets.clips.twitchcdn.net/65Rr9SgZAqtJRrxiA-epPg/AT-cm%7C65Rr9SgZAqtJRrxiA-epPg.mp4?sig=5f35aa6bf3947842306d1e64b2dce1682c31c682&token=%7B%22authorization%22%3A%7B%22forbidden%22%3Afalse%2C%22reason%22%3A%22%22%7D%2C%22clip_uri%22%3A%22https%3A%2F%2Fproduction.assets.clips.twitchcdn.net%2F65Rr9SgZAqtJRrxiA-epPg%2FAT-cm%257C65Rr9SgZAqtJRrxiA-epPg.mp4%22%2C%22device_id%22%3A%22uH03Q2tsNnyjRsX1WorbAev94SXJFmcW%22%2C%22expires%22%3A1664106680%2C%22user_id%22%3A%2298329711%22%2C%22version%22%3A2%7D"
f = r"https://www.ozbargain.com.au/"
driver = uc.Chrome(f)

driver.get(url)
g = driver.page_source
g = g.split("src")[6]
g = g.split("><")
g = g[0][1:]
r = requests.get(g)
r = r.content
try:
    f = open("demofile2.mp4", "wb")
    f.write(r)
    f.close()
except:
    print("failed url")

# g[6] contains the url after split, for some reasoin the url is forbidden??? doesnt work
g = g.split("src")[6]
g = g.split("><")
g = g[0]
g = g[2 : len(g) - 12]
## I believe this is because there is anti bot detection when scraping, need to figure out how to disable/bypass this.
