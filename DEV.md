# EPA - Energy Planning Application
### Folders and Files

- DB: By default: sqlite is utilized as the development db. Can be altered in `epa/setting.py`.
- Docker and Compose: 
    - In `dev branch`, the repo is structured to easily deploy locally. Docker is not utilized in dev mode (branch).
    - In `production branch` the structure of the repo changes to ease the deployment with docker compose. To that end, all epa django app files are moved into the `app` folder. Instruction to cofigure and build are provided in `docker-compose.yml`, epa's `Dockerfile` and `epa.env`. Nginx is utilized for serving static files and act as reverse proxy, while a third container is created to hold the database (MySQL).

- import.sql: The way the app was designed required some data to be loadded in the database (ONLY ONCE AFTER CREATION). All the required data are provided either in sql format to directly load using the db container, or inside a fixture.

- Fixtures: utilized by django to easily export or import data in the underlying database.
    - fixture.json: equivalent to executing `import.sql` rather can be done from inside django's (app) container. Fixtures shall be loadded in the database after `makemigrations` and `migrate` are completed successfully.
    - benchmark_fixture.json: contains everything inside `fixture.json` along with a test user with a scenario set up and results page populated with data (testUser credential in README).
    - two_scenarios_fixture.json: Same as `benchmarks_fixture.json` with an extra scenario (testUser credential in README).

- Django App Structure: 3 distinct apps (users, projects, dashboard)
    - users app: all the required views, urls and helper files, to add user level functionality to the application (signup, login, etc).
    - dashboard app: Could be completely separated from the project and still function (might require slight tweeking). The app provides any required backend logic for the results visualization. This app along with the associated templates in the `templates` folder.
    - projects app: Everything else in the EPA project is implemented in this app. project, scenario, comments and all assets CRUD operations are accessible in this app.

- deployment_helpers: docker-compose and nginx conf required in production.

- setup.sh: A script to automate few set up steps for django server either in development or in production.
