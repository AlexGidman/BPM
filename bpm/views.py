"""
All web app views (aka routes) for BPM flask application found in here.
"""

from flask import Blueprint, render_template, url_for, redirect, request, flash
from pprint import pprint
from .spotify import SpotifyAPI
from api_key import api_key

main = Blueprint("main", __name__)

# Configure Spotify API
spotify = SpotifyAPI(api_key['client_id'], api_key['client_secret'])

@main.route('/')
def main_index():
    """Main index route 'Homepage'

    Returns:
        GET: index.html template

    """

    return render_template("index.html")


@main.route('/search', methods=["GET", "POST"])
def main_search():
    """Search route

    Returns:
        POST: search.html template with search results (tracks)
        GET: redirects to main index route.

    """

    if request.method == "POST":

        search_query = {}
        if request.form.get('track'):
            search_query = {'track': request.form.get('track')}

        tracks = spotify.get_tracks(search_query)
        return render_template("search.html", tracks=tracks)

    return redirect(url_for('main.main_index'))


@main.route('/advanced', methods=["GET", "POST"])
def main_advanced_search():
    """Advanced Search route

    Returns:
        POST: search.html template with search results (tracks)
        GET: advanced.html template

    """

    if request.method == "POST":
        search_query = {}
        if request.form.get('track'):
            search_query['track'] = request.form.get('track')
        if request.form.get('artist'):
            search_query['artist'] = request.form.get('artist')
        if request.form.get('album'):
            search_query['album'] = request.form.get('album')
        
        pprint(search_query)

        tracks = spotify.get_tracks(search_query)
        return render_template("search.html", tracks=tracks)

    return render_template("advanced.html")


@main.route('/track')
@main.route('/track/<id>')
def main_track_details(id: str = None):
    """Track Details route

    Args:
        id(str): 22 character alphaumeric string representing a Spotify track id

    Returns:
        GET: track.html template with track data, redirects to main index route if track doesn't exist.

    """

    try:
        track = spotify.get_track(id)
    except:
        flash('Incorrect Track ID entered! Try again.')
        return redirect(url_for('main.main_index'))
    return render_template("track.html", track=track)