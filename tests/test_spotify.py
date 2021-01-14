"""Tests for spotify.py module"""
import pytest
from unittest.mock import Mock, patch
from bpm import spotify


class TestClassInitialisation:
    '''Test for initialisation of the SpotifyAPI Class'''

    def test_failed_authentication_of_api_class(self, invalid_client_id, invalid_client_secret):
        with pytest.raises(Exception):
            spotify.SpotifyAPI(invalid_client_id, invalid_client_secret)
    
    @pytest.mark.skip  # system test, not unit test
    def test_successful_authentication_of_api_class(self, valid_client_id, valid_client_secret):
        api_client = spotify.SpotifyAPI(valid_client_id, valid_client_secret)
        assert api_client


class TestPublicClassMethods:
    '''Test all publicly accessed methods in the SpotifyAPI Class using Mock'''

    def test_successful_authentication_of_mock_api_class(self, mock_spotify_api_class):
        assert mock_spotify_api_class

    def test_failed_get_resource(self, mock_spotify_api_class, invalid_request):
        """Mock invalid resource request"""
        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = invalid_request
            result = mock_spotify_api_class.get_resource("")
            assert result == {}

    def test_successful_get_resource(self, mock_spotify_api_class, valid_request):
        """Mock valid resource request - note that mock json data is inaccurate!"""

        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = valid_request
            result = mock_spotify_api_class.get_resource(
                lookup_id="mock_track_id")
            assert result == valid_request.json.return_value

    def test_failed_get_artist(self, mock_spotify_api_class, invalid_request):
        """Mock invalid get_artist request"""

        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = invalid_request
            result = mock_spotify_api_class.get_artist("")
            assert result == {}

    def test_successful_get_artist(self, mock_spotify_api_class, valid_request):
        """Mock valid get_artist request - note that mock json data is inaccurate!"""

        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = valid_request
            result = mock_spotify_api_class.get_artist(
                lookup_id="mock_artist_id")
            assert result == valid_request.json.return_value

    def test_failed_get_album(self, mock_spotify_api_class, invalid_request):
        """Mock invalid get_album request"""

        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = invalid_request
            result = mock_spotify_api_class.get_album("")
            assert result == {}

    def test_successful_get_album(self, mock_spotify_api_class, valid_request):
        """Mock valid get_artist request - note that mock json data is inaccurate!"""

        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = valid_request
            result = mock_spotify_api_class.get_album(
                lookup_id="mock_album_id")
            assert result == valid_request.json.return_value


    def test_failed_search(self, mock_spotify_api_class):
        with pytest.raises(Exception):
            mock_spotify_api_class.search("")


    def test_successful_search(self, mock_spotify_api_class, valid_request):
        """Mock valid search request - note that mock json data is inaccurate!"""

        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = valid_request
            result = mock_spotify_api_class.search(query={"track": "mock_track_name"},
                                                   search_type="track",
                                                   market_type="GB")
            assert result == valid_request.json.return_value


    def test_failed_get_tracks(self, mock_spotify_api_class):
        with pytest.raises(Exception):
            mock_spotify_api_class.get_tracks("")


    def test_successful_get_tracks(self, mock_spotify_api_class, valid_request, valid_get_tracks_data):
        """Mock valid get_tracks request - note that mock json data is inaccurate!"""

        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = valid_request
            result = mock_spotify_api_class.get_tracks(query={"track": "mock_track_name",
                                                              "artist": "mock_artist"})
            assert result == valid_get_tracks_data


    def test_failed_get_musical_data(self, mock_spotify_api_class):
        with pytest.raises(Exception):
            mock_spotify_api_class.get_musical_data("")


    def test_successful_get_musical_data(self, mock_spotify_api_class, valid_track_data_request, valid_get_musical_data):
        """Mock valid get_musical_data request - note that mock json data is inaccurate!"""

        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = valid_track_data_request
            result = mock_spotify_api_class.get_musical_data(track_id="mock_track_id")
            assert result == valid_get_musical_data

    def test_failed_key_convert(self, mock_spotify_api_class):
        result = mock_spotify_api_class.key_convert(key=12)
        assert result == "No Key Available"

    def test_successful_key_convert(self, mock_spotify_api_class):
        result = mock_spotify_api_class.key_convert(key=6, mode=1) # key 6 = Gb, mode 1 = Major
        assert result == "Gb Major"

    def test_failed_get_track(self, mock_spotify_api_class):
            """Invalid get_track """
            with pytest.raises(Exception):
                mock_spotify_api_class.get_track("")

    def test_successful_get_track(self, mock_spotify_api_class, valid_track_data_request, valid_get_track_data):
        """Mock valid get_track request - note that mock json data is inaccurate!"""

        with patch('bpm.spotify.requests.get') as mock_requests:
            mock_requests.return_value = valid_track_data_request
            result = mock_spotify_api_class.get_track(lookup_id="mock_track_id")
            assert result == valid_get_track_data