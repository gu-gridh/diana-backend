# Digital humanities portal in Django

## Local installation
To install the Digital Humanities Portal, we advise using a Conda distribution, such as [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html). 
This allows simultaneous installation of necessary binaries.

Clone the repository and change directory. 
```bash
git clone https://github.com/CDH-DevTeam/diana-backend.git
# Or, if you want to get all submodule apps as well
# git clone --recurse-submodules https://github.com/CDH-DevTeam/diana-backend.git
cd diana-backend
```

Create a new conda environment from the `environment.yml` file using
```bash
conda env create -n diana -f environment.yml
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

## Localization
Localization is done by using the `gettext_lazy` translation utility, e.g.
```python
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _('admin.site.site_header')
```
where `admin.site.site_header` is an identifier to be translated into the local languages. By running
```
python manage.py makemessages -l <language-code>
```
a `.po` translation file is generated, with the format
```
#: directory/file.py:line
msgid "admin.site.site_header"
msgstr ""
```
where `msgstr` is the corresponding translation to be added, e.g. `"Admin site"` in English and `"Adminsajt"` in Swedish. 
When the `.po` file is complete, the translations need to be compiled with
```bash
django-admin compilemessages
```
which generates a binary `.mo` file.

## TODO

- [x] Added generic filtering
- [x] Added schema endpoint
- [x] Dynamic API documentation 
- [x] Added gis-input
- [x] Localization
- [ ] Customize admin interface
- [ ] Customize editing
- [ ] Add image in associated object previews
- [ ] Add more projects


## Current URLs

- http://localhost:8000/admin/ - Admin interface for  users and groups
- http://localhost:8000/iconographia/api/ - REST API endpoint
- http://localhost:8000/iconographia/redoc-ui/ - Dynamic API documentation with Redoc
- http://localhost:8000/iconographia/swagger-ui/ - Dynamic API documentation with Swagger/OpenAPI

