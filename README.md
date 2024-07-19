# DIANA
Diana is a portal for digital humanities projects, developed by the Gothenburg Research Infrastructure in Digital Humanities (GRIDH) at the University of Gothenburg. It is a database coordination solution, interface for data input, and a service for making data accessible through generated REST APIs.

## Structure
Diana is a solution for coordinating multiple potentially interacting databases. It has the following structure:

```
├── apps
│   ├── __init__ .py
│   ├── litteraturlabbet
│   ├── norfam
│   ├── rwanda
│   ├── saga
│   ├── shfa
│   └── ...
├── diana
│   ├── __init__.py
│   ├── abstract
│   ├── asgi.py
│   ├── routers.py
│   ├── settings.py
│   ├── storages.py
│   ├── urls.py
│   ├── utils.py
│   └── wsgi.py
├── locale
│   ├── en
│   └── sv
├── static
│   ├── admin-interface
│   ├── rwanda
│   └── shfa
├── templates
│   ├── redoc.html
│   └── swagger-ui.html
├── README.md
├── requirements.txt
├── environment.yml
└── manage.py
```

In `apps`, Diana stores a number of so-called applications, or projects, as git submodules. These all have a corresponding GitHub repository where development is done independently.

Another folder, `diana` technically also qualifies as an app. It coordinates the rest of the applications, and contains utility functions and common, abstract classes, in `abstract`. This is also where the global settings are located.

The `locale` folder contains files for internationalization of text in the admin interface of Diana. In the `static` and `templates` folders you will find static files, such as images and html templates (for customized frontends handled by Django itself) respectively.

## Local installation
To install the Digital Humanities Portal, we advise using a Conda distribution, such as [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html). 
This allows simultaneous installation of necessary binaries.

### Operative system support
Diana and its dependencies have been tested on Linux, e.g. Ubuntu 16.04+ and RedHat OS. Problems have been documented due to geographical dependencies on Windows and MacOS.

### Instructions
Clone the repository and change directory. 
```bash
git clone https://github.com/CDH-DevTeam/diana-backend.git
cd diana-backend
```

Create a new conda environment from the `environment.yml` file using
```bash
conda env create -n diana -f environment.yml
```
This will also install the required GDAL dependency for geographical databases.

Activate the conda environment:
```bash
conda activate diana
```

Before installing Diana, it is advised to first look through the Django [tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) and documentation.

For a local installation, a `configs` folder with database credentials for your local database is needed.
Your local database needs the `postgis` extension which can be added as postgres user with:
```bash
\connect <databasename>
CREATE EXTENSION postgis;
```
Also, a `settings_local.py` with local settings is needed. The description of it can be found in [deployment instructions](deployment.md).

Launch Django by migrating all the initial settings,
```bash
python manage.py migrate 
```
and create a suitable superuser.

```bash
python manage.py createsuperuser 
```

Run it locally via:
```bash
python manage.py runserver
```

## Installation and deployment
To also fetch the submodules of a specific branch and for more detailed instructions, please follow the instructions in the [deployment instructions](deployment.md).

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

## Current URLs

- http://localhost:8000/admin/ - Admin interface for  users and groups
- http://localhost:8000/api/ - REST API endpoints
- http://localhost:8000/api/<project>/ - Endpoint for a certain project
- http://localhost:8000/api/<project>/documentation/ - Dynamic API documentation with ReDoc/OpenAPI

