# Digital humanities portal in Django

## Local installation
To install the Digital Humanities Portal, we advise using a Conda distribution, such as [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html). 
This allows simultaneous installation of necessary binaries.

Clone the repository and change directory. 
```bash
git clone https://github.com/CDH-DevTeam/dihup-backend.git
cd dihup-backend
```

Create a new conda environment from the `environment.yml` file using
```bash
conda create -n dihup -f environment.yml
```
This will also install the required GDAL dependency for geographical databases.

###
Launch Django by migrating all the initial settings,
```bash
python manage.py migrate 
```
and create a suitable superuser.

```bash
python manage.py createsuperuser 
```
## Initial database setup

Edit `DATABASES` settings in `settings.py` to reflect your local database names and users, e.g. `iconographia`. Then:

```bash
python manage.py makemigrations

python manage.py migrate --database <your-database>
```

## TODO

- [x] Added generic filtering
- [x] Added schema endpoint
- [x] Dynamic API documentation 
- [x] Added gis-input
- [ ] Customize editing
- [ ] Add model definitions for other projects
- [ ] Add expansion
- [ ] Localization


## Current URLs

- http://localhost:8000/admin/ - Admin interface for  users and groups
- http://localhost:8000/iconographia/api/ - REST API endpoint
- http://localhost:8000/iconographia/redoc-ui/ - Dynamic API documentation with Redoc
- http://localhost:8000/iconographia/swagger-ui/ - Dynamic API documentation with Swagger/OpenAPI

