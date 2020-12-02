# -*- coding: utf-8 -*-
"""
SpotifyAPI

This module implements the SpotifyAPI class for making requests to the Spotify API. It can return
search results and resources such as artist, track, and album data. It can also format the data
returned by the Spotify api as human-readable Python variables.

"""

import base64
import datetime
from urllib.parse import urlencode
import requests


class SpotifyAPI():
    """
    A class to make authorised api requests to Spotify.

    Can perform authentication to obtain an access token for the spotify api, and then make requests
    of that api such as searching for artist, album, or track data.

    Typical usage example::

        spotify = SpotifyAPI(client_id, client_secret)
        results = spotify.search(query={"track": "money", "artist": "pink floyd"},
                                    search_type="track",
                                    market_type="US")`

    Attributes:
        access_token: a time-limited access token string provided by spotify for making api
          requests.
        access_token_expires: time at which current access_token expires.
        access_token_did_expire: expresses whether access_token has expired or not.
        client_id: spotify client id for the application.
        client_secret: spotify client secret for the application, relates to specific client id.
        token_url: url for obtaining spotify access token.

    """

    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"


    def __init__(self, client_id: str, client_secret: str) -> None:
        """Inits SpotifyAPI class and performs authentication.

        Args:
            client_id (str): spotify client id for the application.
            client_secret (str): spotify client secret for the application, relates to specific
              client id.

        """
        self.client_id = client_id
        self.client_secret = client_secret
        self._perform_auth()


    def _get_client_credentials(self) -> str:
        """Combines client_id and client_secret to create a single base64 encoded string.

        Returns:
            client_creds_b64.decode(): client-id and client_secret combined as a base64 encoded
            string.

        """

        client_id = self.client_id
        client_secret = self.client_secret

        if client_secret is None or client_id is None:
            raise Exception("client_id and client_secret required.")

        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()


    def _get_token_headers(self) -> dict:
        """Creates headers for access token api request.

        Returns:
            A dict containing a formatted string for access token requests containing client
            credential information.

        """

        client_creds_b64 = self._get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }


    @staticmethod
    def _get_token_data() -> dict:
        """Creates token data as a dict.

        Returns:
            A dict containing access token request data, authorisation granted based on client
            credential information.

        """

        return {"grant_type": "client_credentials"}


    def _get_access_token(self) -> str:
        """Obtains and returns a valid access token.

        Returns:
            token(str): access token for making authenticated api requests to Spotify.

        """

        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self._perform_auth()
            return self._get_access_token()
        if token is None:
            self._perform_auth()
            return self._get_access_token()
        return token


    def _perform_auth(self) -> bool:
        """Performs authentication for making api requests to Spotify - obtains a token using client credentials.

        Returns:
            True once authentication has been successfully completed.

        Raises:
            Exception: Authentication failed - ensure client credentials are correct.

        """

        token_url = self.token_url
        token_data = self._get_token_data()
        token_headers = self._get_token_headers()

        result = requests.post(
            token_url, data=token_data, headers=token_headers)
        if result.status_code not in range(200, 299):
            raise Exception(
                "Authentication failed - ensure client credentials are correct.")
        data = result.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)

        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True


    def _get_resource_headers(self) -> dict:
        """Creates headers for resource api request.

        Returns:
            headers(dict): a dict containing access token for making  authorised api requests.

        """

        access_token = self._get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers


    def get_resource(self, lookup_id: str, resource_type: str = "tracks",
                     version: str = "v1") -> dict:
        """Makes an api request for resources from spotify.

        Retrieves JSON data related to resource request type and returns as a dict of
        unaltered data.

        Args:
            lookup_id(str): a string of 22 alphanumeric characters related to a specific object
              such as artist, track, album etc.
            resource_type(str): type of resource that relates to lookup_id such as 'track',
              'artist','album' etc.
            version(str): a string relating to version of spotify api. At point of creation only v1
              is available.

        Returns:
            r.json() (dict): a dict containing unaltered data related to the requested resource. If
            request is unsuccessful, returns an empty dict.

        """

        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self._get_resource_headers()
        result = requests.get(endpoint, headers=headers)
        if result.status_code not in range(200, 299):
            return {}
        return result.json()


    def get_artist(self, lookup_id: str) -> dict:
        """Gets artist data from spotify based on lookup_id

        Args:
            lookup_id(str): a string of 22 alphanumeric characters related to specific artist,
              usually obtained from SpotifyAPI.search().

        Returns:
            A dict containing unaltered json data related to the artist. If request is
              unsuccessful, returns an empty dict.

        """

        return self.get_resource(lookup_id, resource_type="artists")


    def get_album(self, lookup_id: str) -> dict:
        """Gets album data from spotify based on lookup_id

        Args:
            lookup_id(str): a string of 22 alphanumeric characters related to specific album,
              usually obtained from SpotifyAPI.search().

        Returns:
            A dict containing unaltered json data related to the album. If request is
              unsuccessful, returns an empty dict.

        """

        return self.get_resource(lookup_id, resource_type="albums")


    def get_track(self, lookup_id: str) -> dict:
        """Gets track data from spotify based on lookup_id

        Typical usage example::

            track = SpotifyAPI.get_track("XXXXyyyyYYYYxxxxZZZZab")
            print(track)
            {'artist': _,
            'image_url': _,
            'key': _,
            'tempo': _,
            'track_id': _,
            'track_name': _,
            'track_url': _}

        Args:
            lookup_id(str): a string of 22 alphanumeric characters related to specific track,
              usually obtained from SpotifyAPI.search().

        Returns:
            A dict containing formatted data related to the track. If request is
              unsuccessful, returns an empty dict.

        """

        track_data = self.get_resource(lookup_id, resource_type="tracks")
        track = self.get_musical_data(lookup_id)
        try:
            track["track_name"] = track_data['name']
            track["artist"] = track_data['artists'][0]['name']
            track["track_url"] = track_data['external_urls']['spotify']
            track["image_url"] = track_data['album']['images'][0]['url']
        except:
            return {}
        return track


    def _get_track_features(self, lookup_id: str) -> dict:
        """Gets audio features of track from spotify based on lookup_id

        Args:
            lookup_id(str): a string of 22 alphanumeric characters related to specific album,
              usually obtained from SpotifyAPI.search().

        Returns:
            A dict containing unaltered data related to the track. If request is
              unsuccessful, returns an empty dict.

        """

        return self.get_resource(lookup_id, resource_type="audio-features")


    def search(self, query: dict = None, search_type: str = "artist",
               market_type: str = "GB") -> dict:
        """Makes an api request for search data from spotify.

        Retrieves JSON data related to search request and returns as a dict of
        unaltered data.

        Args:
            query(dict): the search query as a dict of parameters such as {'track': '<song_title>'}
            search_type(str): the type of search to be conducted such as for a 'track', 'artists',
              'albums' etc.
            market_type(str): a string relating to market the searchable object is available in;
              "GB", "US" etc.

        Returns:
            r.json() (dict): a dict containing unaltered data related to the search request. If
              request is unsuccessful, returns an empty dict.

        Raises:
            Exception: A query is required.

        """

        if query is None:
            raise Exception("A query is required")

        query_string = ""
        for key, value in query.items():
            query_string += f"{key}:{value} "

        query_params = urlencode({"q": query_string, "type": search_type.lower(),
                                  "market": market_type})
        lookup_url = f"https://api.spotify.com/v1/search?{query_params}"
        headers = self._get_resource_headers()

        result = requests.get(lookup_url, headers=headers)
        print(result.status_code)
        if not result.status_code in range(200, 299):
            return {}
        return result.json()


    def get_tracks(self, query: dict = None) -> list:
        """Gets tracks from an api search request

        Retrieves JSON data related to search request and returns as a formatted list of dicts for
        easy lookup and manipulation.

        Typical usage Example::

            results = SpotifyAPI.get_tracks({'track': 'money'})
            first_result = results[0]
            print(first_result)
            {'track_id': _,
            'track_name: _,
            'artist': _,
            'track_url': _,
            'image_url': _}

        Args:
            query(dict): the search query as a dict of parameters such as {'track': '<song_title>'}

        Returns:
            tracks (list): a list of dicts containing formatted track data. See example above.

        Raises:
            Exception: Invalid search, no data found

        """

        json_data = self.search(query, "track")
        tracks = []
        try:
            tracks = [{'track_id': i['id'],
                       'track_name': i['name'],
                       'artist': i['artists'][0]['name'],
                       'track_url': i['external_urls']['spotify'],
                       'image_url': i['album']['images'][0]['url']
                       } for i in json_data['tracks']['items']]
        except:
            raise Exception("Invalid search, no data found")
        finally:
            return tracks


    def get_musical_data(self, track_id: str) -> dict:
        """Gets key and tempo info related to track

        Typical usage example::

            results = SpotifyAPI.get_musical_data("XXXXyyyyYYYYxxxxZZZZab")
            print(results)
            {'track_id': 'XXXXyyyyYYYYxxxxZZZZab',
            'key': 'B Minor',
            'tempo': 120}

        Args:
            lookup_id(str): a string of 22 alphanumeric characters related to specific track,
              usually obtained from SpotifyAPI.search().

        Returns:
            musical_data(dict): a dict containing formatted key & tempo information.

        Raises:
            Exception: No data found - check track_id

        """

        try:
            track_data = self._get_track_features(track_id)
            key = self.key_convert(track_data['key'], track_data['mode'])
            tempo = int(track_data['tempo'])
            musical_data = {"track_id": track_id,
                            "key": key,
                            "tempo": tempo}
            return musical_data
        except:
            raise Exception("No data found - check track_id")

    @staticmethod
    def key_convert(key: int, mode: int = None) -> str:
        """Converts key and mode value to musical key format (eg "B Minor")

        Args:
            key(int): a value that corresponds to one of 12 musical keys.
            mode(int): a value that indicates if major or minor key

         Returns:
            A formatted string that represents the musical key eg 'Gb', 'A Major', 'D Minor'.
            If no valid key present, returns "No Key Available"

        """

        if key < 0 or key > 11:
            return "No Key Available"

        keys = {0: "C", 1: "Db", 2: "D", 3: "Eb",
                4: "E", 5: "F", 6: "Gb", 7: "G",
                8: "Ab", 9: "A", 10: "Bb", 11: "B"}

        if mode == 1:
            return f"{keys[key]} Major"
        if mode == 0:
            return f"{keys[key]} Minor"
        return keys[key]

if __name__ == "__main__":
    pass