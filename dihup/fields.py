from django.db.models.fields.reverse_related import ManyToOneRel
from django.apps import apps


custom_visibility_settings = {
    "created": {
        "type": "varchar",
        "extra": "64",
        "label": "Skapad av",
        "readonly": True,
        "searchable": False
    },
    "modified": {
        "type": "varchar",
        "extra": "64",
        "label": "Ändrad av",
        "readonly": True,
        "searchable": False
    },
    "updated": {
        "type": "date",
        "extra": "",
        "label": "Senast ändrad",
        "readonly": True,
        "searchable": False
    }
}

"""
Get fields generates data needed for the frontend, same as `edit.php` in PHP backend.


DEFAULTS for fields
- hidden: False
- readonly: False
- searchable: True
"""
def get_fields(project, tb):
    model = apps.get_model(project, tb)
    fields = {}

    for model_field in model._meta.get_fields():
        field_id = model_field.name

        # ManyToOneRel is a backwards reference to current model, in our PHP backend we fetch those separately and can continue to do so 
        if isinstance(model_field, ManyToOneRel):
            continue 

        field_def = custom_visibility_settings.get(field_id, {})
        if ("searchable" not in field_def):
            field_def["searchable"] = True
        if ("readonly" not in field_def):
            field_def["readonly"] = False
        if ("hidden" not in field_def):
            field_def["hidden"] = False

        # fetch the internal type of the field and match to 
        model_internal_type = model_field.get_internal_type()
        extra = None
        if model_internal_type == 'TextField':
            field_type = "text"
        elif model_internal_type == 'CharField':
            field_type = "char"
            extra  = str(model_field.max_length)

        # id field
        elif model_internal_type == 'BigAutoField':
            field_type = "int"

        elif model_internal_type == 'ForeignKey':
            field_type = "int"
            # fcol hard-coded for now
            field_def["fcol"] = "id"
            field_def["ftab"] = model_field.related_model._meta.db_table
        
        # TODO Don't think anyone cares about difference between int / smallint, but maybe it should be used for validation
        elif model_internal_type == 'IntegerField':
            field_type = "int"
        elif model_internal_type == 'SmallIntegerField':
            field_type = "smallint"
        elif model_internal_type == 'DateField':
            field_type = "date"
        elif model_internal_type == 'GeometryField':
            field_type = "geometry"
        else:
            raise ValueError("Model field type not supported: ", field_id, model_internal_type)

        field_def["type"] = field_type
        field_def["extra"] = extra

        field_def["label"] = model_field.verbose_name
        field_def["help"] = model_field.help_text
    
        fields[field_id] = field_def

    return fields
