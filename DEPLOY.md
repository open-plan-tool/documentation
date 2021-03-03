## Deployment

Override the existing production branch with a new based on dev branch changes.

 To create the production branch:
 1. Checkout a new temp branch `git checkout -b temp_prod dev`
 2. copy all django files and folder in 'app' folder
 3. move files and folder out of the 'deploymet_helpers' in the root of working directory, i.e. 'epa'
 4. modify epa.env to DEBUG=False
 5. modify app/epa/settings.py database to docker MySQL

6. Delete the old local and remote production branch `git push -d origin production` and `git branch -d production`
7. Rename 'temp_prod' to 'production' `git branch -m temp_prod production`
8. Push new branch to origin `git push -u origin production`

