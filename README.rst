
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

Once you have installed dependencies, execute the following command:

.. code-block::

    flask run

Open localhost:5000 URL on your web browser.

Using Docker
~~~~~~~~~~~~

If you have Docker installed on your system you can run the application by setting the api key
environment variables, and then running:

.. code-block::

    docker-compose up --build

For the application, open localhost:5000 URL on your web browser.
For the documentation, open localhost:80 URL on your web browser.

API key
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

Creating Documentation
----------------------

Documentation is built using sphinx. Once sphinx has been installed, ensure the docs/source folder
is present. If so, run the following shell script to make the documentation and view in browser:

.. code-block::

  ./create_docs.sh

Authors
-------

* Alex Gidman

Version History
---------------

* Initial Release V1.0
