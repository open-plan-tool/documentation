# EPA - Energy Planning Application
## Containerized Deployment

A Web App created for the needs of E-Land EU Project.  
The application provides a front-end environment where users can provide  
energy systems planning and economic related data which are afterwards  
utilized in a simulation environment.


<hr>

#### Deploy using Docker Compose

1. `git clone --single-branch --branch dc-deploy https://colab-repo.intracom-telecom.com/colab-projects/eland/epa.git`
2. cd inside the created folder
3. Modify the proxy in app/Dockerfile to fit your needs.
3. `docker-compose up -d --build`
4. `docker-compose exec app sh ./setup.sh`
5. Open browser and navigate to localhost.

#### That should get everything up and running.

To clear local data afer usage execute:
`docker-compose down --volumes --rmi 'local'`
<hr>
 