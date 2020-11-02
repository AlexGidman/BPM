# BPM
A web application for searching Spotify for track information. Built using thee Flask framework.

### Dependencies
* Python3
Project specific dependencies can be found in requirements.txt and can be installed via pip:
```
pip install -r requirements.txt
```
### Executing program (development only)
Once you have installed dependencies, you need to set the FLASK_APP & FLASK_ENV variables: 
* Mac / Linux 
```
export FLASK_APP=bpm
export FLASK_ENV=development
```
* Windows
```
set FLASK_APP=bpm
set FLASK_ENV=development
```
Finally, providing you have a client_id & client_secret configured for the SpotifyAPI class, you can run:
```
flask run
```

### API_KEY
You will need to create an api_key.py file and store it in the parent directory 'BPM'. Within the api_key.py file you should define a python dict 'api_key':
```
api_key = {'client_id': "<client id>",
            'client_secret': "<client secret>"}
```
##### Obtaining client id & client secret
* Register a Spotify account and login to the developer site [here](https://developer.spotify.com/)
* Go to the Dashboard, and "Create An App".
* Copy and paste client id & client secret into api_key.py file as shown above.

### Authors
* Alex Gidman
### Version History
* Initial Release
