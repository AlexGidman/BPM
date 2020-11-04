import pytest
from unittest.mock import Mock, patch
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bpm import spotify
import api_key


@pytest.fixture
def valid_client_id() -> str:
    '''Returns valid client id for api authentication as str'''

    return api_key.api_key['client_id']


@pytest.fixture
def valid_client_secret() -> str:
    '''Returns valid client secret for api authentication as str'''

    return api_key.api_key['client_secret']


@pytest.fixture
def invalid_client_id() -> str:
    '''Returns invalid client id for api authentication as str'''

    return "xxxxXXXXxxxxXXXXxxxx"


@pytest.fixture
def invalid_client_secret() -> str:
    '''Returns invalid client secret for api authentication as str'''

    return "yyyyYYYYyyyyYYYYyyyy"


@pytest.fixture
def mock_spotify_api_class():
    """Mock authenticated api class"""
    with patch('bpm.spotify.requests.post') as mock_requests:
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {'access_token': 'mock_access_token', 'expires_in': 200}
        return spotify.SpotifyAPI("mock_client_id", "mock_client_secret")


class TestClassInitialisation:
    '''Test for initialisation of the SpotifyAPI Class'''

    def test_failed_authentication_of_api_class(self, invalid_client_id, invalid_client_secret):
        with pytest.raises(Exception):
            spotify.SpotifyAPI(invalid_client_id, invalid_client_secret)


    def test_successful_authentication_of_api_class(self, valid_client_id, valid_client_secret):
        api_client = spotify.SpotifyAPI(valid_client_id, valid_client_secret)
        assert api_client


class TestPublicClassMethods:
    '''Test all publicly accessed methods in the SpotifyAPI Class'''
    
    def test_successful_authentication_of_mock_api_class(self, mock_spotify_api_class):
        assert mock_spotify_api_class


    # def test_failed_get_resource(self, spotify_api_class):
    #     result = spotify_api_class.get_resource("")
    #     assert result == {}


#     def test_successful_get_resource(self, spotify_api_class):
#         """Gets Track: Back In Black"""

#         result = spotify_api_class.get_resource(lookup_id="08mG3Y1vljYA6bvDt4Wqkj")
#         assert result != {}


#     def test_failed_get_artist(self, spotify_api_class):
#         result = spotify_api_class.get_artist("")
#         assert result == {}


#     def test_successful_get_artist(self, spotify_api_class):
#         """Gets Artist: AC/DC"""

#         result = spotify_api_class.get_artist(lookup_id="711MCceyCBcFnzjGY4Q7Un")
#         assert result != {}


#     def test_failed_get_album(self, spotify_api_class):
#         result = spotify_api_class.get_album("")
#         assert result == {}


#     def test_successful_get_album(self, spotify_api_class):
#         """Gets Album: Back In Black"""

#         result = spotify_api_class.get_album(lookup_id="6mUdeDZCsExyJLMdAfDuwh")
#         assert result != {}


#     def test_failed_get_track(self, spotify_api_class):
#         with pytest.raises(Exception):
#             spotify_api_class.get_track("")


#     def test_successful_get_track(self, spotify_api_class):
#         """Gets Track: Back In Black"""

#         result = spotify_api_class.get_track(lookup_id="08mG3Y1vljYA6bvDt4Wqkj")
#         assert result != {}


#     def test_failed_search(self, spotify_api_class):
#         with pytest.raises(Exception):
#             spotify_api_class.search("")


#     def test_successful_search(self, spotify_api_class):
#         result = spotify_api_class.search(query={"track": "back in black"}, 
#                                             search_type="track",
#                                             market_type="GB")
#         assert result != {}


#     def test_failed_get_tracks(self, spotify_api_class):
#         with pytest.raises(Exception):
#             spotify_api_class.get_tracks("")


#     def test_successful_get_tracks(self, spotify_api_class):
#         result = spotify_api_class.search(query={"track": "back in black"}) 
#         assert result != {}


#     def test_failed_get_musical_data(self, spotify_api_class):
#         with pytest.raises(Exception):
#             spotify_api_class.get_musical_data("")


#     def test_successful_get_musical_data(self, spotify_api_class):
#         """Gets musical data for Track: Back In Black"""

#         result = spotify_api_class.get_musical_data(track_id="08mG3Y1vljYA6bvDt4Wqkj") 
#         assert result != {}


#     def test_failed_key_convert(self, spotify_api_class):
#         result = spotify_api_class.key_convert(key=12) 
#         assert result == "No Key Available"


#     def test_successful_key_convert(self, spotify_api_class):
#         result = spotify_api_class.key_convert(key=6, mode=1) 
#         assert result == "Gb Major"