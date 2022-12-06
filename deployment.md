# Deployment instructions
Diana is only tested on Linux systems, and only confirmed to work there. This is due to a number of Linux-only dependencies, such as VIPS and GDAL. The following instructions will thus assume a Linux operative system.

## Local settings
Add a local settings file by the name `settings_local.py` with the following parameters:
```python

from django.core.management.utils import get_random_secret_key  

SECRET_KEY = get_random_secret_key() # Required
DEBUG = True # For local development, should otherwise be false
MEDIA_ROOT = '<root>/diana-backend/static/' # Location of static files
MEDIA_URL  = '<root>/Projects/diana-backend/test/'
ORIGINAL_URL    = 'http://127.0.0.1:8000/static/' # URL where static files are served
IIIF_URL        = 'http://127.0.0.1:8000/static/' # URL where IIIF files are served
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
APPS_LOCAL = [ # Add the applications you would like to test here

    {
        "name": "<app-name>", # Name of the application
        "config": "<app-config-name>", # Found in apps.py in the application directory
        "managed": True, # True if Django manages the database, otherwise False
    },
]
```


## Testing locally
### Adding a new application
Make sure the project has a GitHub remote repository

```bash
# In the project root...
git init .
git remote add origin https://github.com/CDH-DevTeam/<project>

git branch --set-upstream-to=origin/main master

# Verify
git remote -v

# Make sure you do not push migrations
git add * # Or whatever to add
git commit -m "First commit"
git push
```

Add the project as a submodule in Diana. If is not already in the Diana project structure, pull it into the apps folder.

```bash
# In diana-backend...
git submodule add https://github.com/CDH-DevTeam/<project> apps/<project>

git submodule update --init
```

## Deploy to the server
1. As the `cdhdev` user, find the diana directory
    ```bash
    sudo su cdhdev
    cd /appl/cdh/diana
    ```
    and run the deploy script.
    ```bash
    ./deploy.sh
    ```
    This will fetch the current master branch of the GitHub repository, and all the submodule repositories. Note: You might have to run `./deploy.sh` twice, due 
    to some weirdness with `git submodule`.

2. Add a database configuration file (compare with current files in the directory), to connect to the PostgreSQL database:
    ```json
    {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "diana",
        "USER": <username>,
        "PASSWORD": <password>,
        "HOST": <host/server name>,
        "PORT": 5432
    }
    ```

3. Add the new app(s) to the `APPS_LOCAL` list in the `diana/settings_local.py` file:

    ```python
    APPS_LOCAL = [
        ...,
        {
            "name": <app name>,
            "config": <app config name>,
            "managed": True
        },
    ]
    ```
    the app and app configuration names are found in the `apps.py` file of the app repository.

4. To prepare the changes to the database for a certain app, create the migration scripts in Django:

    ```bash
    python manage.py makemigrations <app name>
    ```

5. To execute the change to the database for a certain app, run the migrations:
    ```bash
    python manage.py migrate <app name>
    ```
6. The next step is to restart the Diana server. Exit the `cdhdev` user, and run
   ```bash
    sudo systemctl restart diana
   ```
