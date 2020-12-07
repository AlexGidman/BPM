
BPM - README
============

A web application for searching Spotify for track information, built using the Flask framework.

Dependencies
------------

* Python3
  
* Project specific dependencies can be found in requirements.txt and can be installed via pip:

  .. code-block::

     pip install -r requirements.txt

Executing program (development only)
------------------------------------

Once you have installed dependencies, execute the following shell script:

  .. code-block::

     ./flask_run.sh

Open your local host URL on your web browser.

API_KEY
-------

You will need to set the api key environment variables for the application to work correctly. This
can be done as follows:

.. code-block::

   export CLIENT_ID="<client_id>"
   export CLIENT_SECRET="<client_id>"

Obtaining client id & client secret
-----------------------------------


* Register a Spotify account and login to the developer site `here <https://developer.spotify.com/>`_
* Go to the Dashboard, and "Create An App".
* Copy and paste client id & client secret into api_key.py file as shown above.

Authors
-------

* Alex Gidman

Version History
---------------

* Initial Release V1.0
