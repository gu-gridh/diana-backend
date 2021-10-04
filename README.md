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

Fetch dumps of saints and strand (flojtur) from CDH03. Or start with empty databases.
Edit `DATABASES` settings in `settings.py` to reflect your local database names and users. Then:

`python manage.py makemigrations`

`python manage.py migrate --database django`

`python manage.py migrate --database saints`

`python manage.py migrate --database strand`

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

### Admin interface

It was easy to create a separate admin interface for each project, by extending
`admin.AdminSite` and add models to this instance instead of the default one. A
route to the new instance must be added in `dihup.urls`. Also see `admin.py` in `saints` and `strand`.

### Model definitions using meta-programming

Dynamically creating models could work, but may not be needed.

```
def create_model(tb_name, fields):

    opts = {
        '__module__': __name__,
        'Meta': type('Meta', (object,), { "db_table": tb_name })
    }

    for field_name in (field_name for field_name in fields if field_name not in ["id", "created", "modified", "updated"]):
        field = fields[field_name]
        if field["type"] == "char":
            field_def = models.CharField(max_length=int(field["extra"]))
        elif field["type"] == "geometry":
            field_def = models.GeometryField(spatial_index=True)
        elif field["type"] == "text":
            field_def = models.TextField()
        # ... etc
        else:
            raise SomeError()
        opts[field_name] = field_def

    type('Location', (BaseModel,), opts)
```

`__name__` could be replaced with the current projects models module name. `"strand.models"`, `"saints.models"` etc. to make integration with
Django as seamless as possible. This is only here in case it's needed when starting to work with customizing queries, forms etc.


### Translations

Do translate a value in Django import:

`from django.utils.translation import gettext_lazy as _`

And then use it, for example when creating a label and help text in a model:

`owner = models.IntegerField(label="_("autom.owner.help"), help_text=_("autom.owner.help"))`

When there are new strings to be translated, update the translation files by running:

`python manage.py makemessages -l en`
`python manage.py makemessages -l sv`

All new keys to be translated will automatically be added. Use the same command to add languages.

Open `locale/en/django.po` to add translations in English etc.

After changing the `*.po` files, run:

``python manage.py compilemessages`

Here is a nice blog post about how to do translations and also how to make an app for language switching in the admin interface https://automationpanda.com/2018/04/21/django-admin-translations/

Prefixing paths with a language code will change language, right now English is default, see Swedish example here: http://localhost:8000/sv/admin/


### Authentication

Current assumption is that the API layer does not need authentication, since editing is done in Admin. Groups are stil untested,
but must work, since members in one project should not be able to access another project.
