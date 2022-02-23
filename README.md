# Digital humanities portal in Django

## Short TODO

- Search filters and queries
- Map endpoint
- Finish model definitions for saints and strand
- Add expansion
- Customize editing

## Install requirements 

This is one setup of many possible. Works on Linux.

Create a virtual env: `python3 -m venv .venv`
Activate virtual env: `source .venv bin activate`

`pip install -r requirements.txt`

We depend on the GDAL library which must be installed with `pip` and in the OS. In Ubuntu/Mint
the library package is called libgdal-dev.

To install in Python run:

`pip install GDAL==<version>` where version matches the version you have installed. Use `gdalinfo --version` to check.

## Initial database setup

Fetch dumps of *iconographia* from CDH03. Or start with empty databases.
Edit `DATABASES` settings in `settings.py` to reflect your local database names and users. Then:

`python manage.py makemigrations`

`python manage.py migrate --database iconographia`

## Creating admin user

`python manage.py createsuperuser --database django`

## Current URLs

http://localhost:8000/admin/ - Admin interface for  users and groups
http://localhost:8000/sv/admin/ - Admin interface for users and groups, but in Swedish
http://localhost:8000/saints-admin/ - Admin interface for the Saints project (not our real database model yet)
http://localhost:8000/strand-admin/ - Admin interface for the Per Strand project (not our real database model yet)

Prefixing the two last URLs with `/sv/` also works.

## Development

Information about the development process, to be updated, removed or moved to a better place later.
