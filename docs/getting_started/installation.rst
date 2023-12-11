============
Installation
============

open-plan-tool runs already live at open-plan-tool https://open-plan.rl-institut.de and the simulation server at https://mvs-open-plan.rl-institut.de/
However it is possible to install both of them locally on your machine or on your own server


Prior to the deploy you should find yourself at the root of the open-plan-tool GUI repository

.. code-block:: bash

    git clone https://github.com/open-plan-tool/gui.git open-plan-tool-GUI
    cd open-plan-tool-GUI


Deploy GUI locally using and using our open plan MVS server
-----------------------------------------------------------

Prior to be able to develop locally, you might need to install postgres,
simply google ``install postgres`` followed by your os name
(``linux/mac/windows``)

1. Create a virtual environment
2. Activate your virtual environment
3. Install the dependencies with
   ``pip install -r app/requirements/postgres.txt``
4. Install extra local development dependencies with
   ``pip install -r app/dev_requirements.txt``
5. Move to the ``app`` folder with ``cd app``
6. Create environment variables (only replace content surrounded by
   ``<>``)

::

   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=<your db name>
   SQL_USER=<your user name>
   SQL_PASSWORD=<your password>
   SQL_HOST=localhost
   SQL_PORT=5432
   DEBUG=(True|False)

8.  Add an environment variable ``MVS_HOST_API`` and set the url of the
    simulation server you wish to use for your models (https://mvs-open-plan.rl-institut.de/ if you wish to use our simulation server). You can deploy your own `simulation server <https://github.com/open-plan-tool/simulation-server>`_ locally if you need
9.  Execute the ``local_setup.sh`` file (``. local_setup.sh`` on
    linux/mac ``bash local_setup.sh`` on windows) you might have to make
    it executable first. Answer yes to the question
10. Start the local server with ``python manage.py runserver``
11. You can then login with ``testUser`` and ``ASas12,.`` or create your
    own account

Deploy using Docker Compose
---------------------------

The following commands should get everything up and running, using the
web based version of the MVS API.

You need to be able to run docker-compose inside your terminal. If you
can’t you should install `Docker
desktop <https://www.docker.com/products/docker-desktop/>`__ first.

-  Clone the repository locally
   ``git clone --single-branch --branch main https://github.com/open-plan-tool/gui.git open_plan_gui``
-  Move inside the created folder (``cd open_plan_gui``)
-  Edit the ``.envs/epa.postgres`` and ``.envs/db.postgres`` environment
   files

   -  Change the value assigned to ``EPA_SECRET_KEY`` with a `randomly
      generated one <https://randomkeygen.com/>`__

   -  Make sure to replace dummy names with you preferred names

   -  The value assigned to the variables ``POSTGRES_DB``,
      ``POSTGRES_USER``, ``POSTGRES_PASSWORD`` in ``.envs/db.postgres``
      should match the ones of the variables ``SQL_DATABASE``,
      ``SQL_USER``, ``SQL_PASSWORD`` in ``.envs/epa.postgres``,
      respectively

   -  Define an environment variable ``MVS_HOST_API`` in
      ``.envs/epa.postgres`` and set the url of the simulation server
      you wish to use for your models (for example
      ``MVS_API_HOST="<url to your favorite simulation server>"``), you
      can deploy your own `simulation
      server <https://github.com/open-plan-tool/simulation-server>`__
      locally if you need

   -  Assign the domain of your website (without ``http://`` or
      ``https://``) to ``TRUSTED_HOST`` , see
      https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins
      for more information

Next you can either provide the following commands inside a terminal
(with ubuntu you might have to prepend ``sudo``)

::

    docker-compose --file=docker-compose-postgres.yml up -d --build

(you can replace ``postgres`` by ``mysql`` if you want to use mysql)

::

    docker-compose --file=docker-compose-postgres.yml exec -u root app_pg sh initial_setup.sh

(this will also load a default testUser account with sample scenario).

Or you can run a python script with the following command

::

    python deploy.py -db postgres

Finally, open a browser and navigate to http://localhost:8080 (or to http://localhost:8090 if you chose to use ``mysql`` instead of ``postgres``): you should see the login page of the open-plan-tool app. You can then login with ``testUser`` and ``ASas12,.`` or create your own account.

Proxy settings (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~

If you use a proxy you will need to set ``USE_PROXY=True`` and edit
``PROXY_ADDRESS=http://proxy_address:port`` with your proxy settings in
``.envs/epa.postgres``.

.. note:: If you wish to use mysql instead of postgres, simply
   replace ``postgres`` by ``mysql`` and ``app_pg`` by ``app`` in the
   above commands or filenames


.. note:: Grab a cup of coffee or tea for this…



Test Account
------------

   You can access a preconfigured project using the following login
   credentials: ``testUser:ASas12,.``

   .. raw:: html

      <hr>

Tear down (uninstall) docker containers
---------------------------------------

To remove the application (including relevant images, volumes etc.), one
can use the following commands in terminal:

::

    docker-compose down --file=docker-compose-postgres.yml -v

you can add ``--rmi local`` if you wish to also remove the images (this
will take you a long time to rebuild the docker containers from scratch
if you want to redeploy the app later then)

Or you can run a python script with the following command

::

    python deploy.py -db postgres --down