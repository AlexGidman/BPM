"""All pytest fixtures and configuration"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import pytest
from unittest.mock import Mock, patch


import api_key
from bpm import spotify


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
        mock_requests.return_value.json.return_value = {
            'access_token': 'mock_access_token', 'expires_in': 200}
        return spotify.SpotifyAPI("mock_client_id", "mock_client_secret")


@pytest.fixture
def invalid_request():
    mock = Mock()
    mock.status_code = 400
    mock.json.return_value = {'error': 'error'}
    return mock


@pytest.fixture
def valid_request():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {'tracks': {'items': [
        {'mock_json_data': 'mock_json_data',
         'id': 'mock_id',
         'name': 'mock_name',
         'artists': [{'name': 'mock_artist'}],
         'external_urls': {'spotify': 'mock_track_url'},
         'album': {'images': [{'url': 'mock_image_url'}]},
        }] # end of items list
        }} # end of ['tracks']['items'] dict
    return mock


@pytest.fixture
def valid_get_tracks_list():
    return [{'track_id': 'mock_id',
             'track_name': 'mock_name',
             'artist': 'mock_artist',
             'track_url': 'mock_track_url',
             'image_url': 'mock_image_url'
             }]
