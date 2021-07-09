# EPA - Energy Planning Application
## Containerized Deployment (use `production` branch)

A Web App created for the needs of E-Land EU Project.  
The application provides a front-end environment where users can provide  
energy systems planning and economic related data which are afterwards  
utilized in a simulation environment.


<hr>

#### Deploy using Docker Compose

1. `git clone --single-branch --branch production https://colab-repo.intracom-telecom.com/colab-projects/eland/epa.git`
2. cd inside the created folder
3. Modify the proxy in app/epa.env to fit your needs.
4. `docker-compose up -d --build`
5. `docker-compose exec app sh setup.sh` (this will also load a default testUser account with sample scenario).
6. Open browser and navigate to localhost.

That should get everything up and running. (This setup utilizes the web based version of the MVS API).
<hr>

#### Deploy using Docker Compose (everything locally)

1. `git clone --single-branch --branch production https://colab-repo.intracom-telecom.com/colab-projects/eland/epa.git`
2. cd inside the created folder
3. Modify the proxy in app/epa.env to fit your needs.
4. (Optional) `git clone --single-branch --branch epa_stable https://github.com/rl-institut/mvs_eland_api.git` to clone the latest stable MVS API version.
5. `docker-compose -f docker-compose_with_mvs.yml up -d --build`
6. `docker-compose exec app sh setup.sh` (this will also load a default testUser account with sample scenario).
7. Open browser and navigate to localhost.

That should get everything up and running.
This setup utilizes a local copy of the MVS API.
You can either use the existing `mvs_eland_api` folder or clone the latest stable version of the MVS API with `git clone --single-branch --branch epa_stable https://github.com/rl-institut/mvs_eland_api.git`
<hr>

### Use
> To see the preconfigured energy grid and other data login with credentials:  `testUser:ASas12,.`

### Tear down
>To clear local data afer usage execute:
`docker-compose down --volumes --rmi 'local'`

Or `docker-compose -f docker-compose_with_mvs.yml down --volumes --rmi 'local'` if docker-compose_with_mvs.yml configuration was utilized.
<hr>

 ### Errors
 1. An error might occure on `setup.sh` execution.
 This is because of the underlying OS and the way it handles EOL.
 Windows (CRLF), Unix (LF) and Mac (CR). 
 Try to execute the commands in the file sequentially instead.
    
### Manage translations
to generate the translations .po files
```bash
 python manage.py makemessages -l de --ignore="src" --ignore="static" --ignore="cdn_static_root" --ignore="requirements.txt"
```
These will be located in the folder `app/locale`, perform the translations (or send the .po file for translation) and then compile the translations:

```bash
python manage.py compilemessages
```
