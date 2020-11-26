# EPA - Energy Planning Application

A Web App created for the needs of E-Land EU Project.  
The application provides a front-end environment where users can provide  
energy systems planning and economic related data which are afterwards  
utilized in a simulation environment.


<hr>
### For development purposes follow the provided [Guidelines](Guidelines.txt).
download the repo dev branch tarball or clone the repo locally.

<hr>
### To build and test locally

#### Option 1: Build using python.
!! INSIDE the extracted repo directory (you need to be able to see manage.py in your current directory), run a terminal
1)	Setup a virtual environment
2)	Install dependencies in requirements.txt
3)	`python manage.py makemigrations`
4)	`python manage.py migrate`
5)	open a sqlite console and execute import.sql to add data required by the app to the db (the grid model will not work properly without this step)
6)	`python manage.py runserver` # to run the app locally

#### Option 2: Build using Docker
1)	Install Docker to your system (if not check this link for your OS)
2)	Download the dev branch of epa repo and navigate to the repo directory
3)	If you work behind a proxy please open the Dockerfile and edit the dummy proxy (company.proxy.com:port) to fit yours, otherwise delete the dummy proxy in lines 4 and 13 and save.
4)	Open your terminal in this directory (`ls | grep manage` should return manage.py file if you are in the correct directory) and execute `docker build -t epa_image .`  (with the dot in the end)
5)	After creating the image run the command: `docker run -d -p 127.0.0.1:80:8000 epa_image `
6)	Open your favorite browser and navigate to `localhost:80`
<hr>