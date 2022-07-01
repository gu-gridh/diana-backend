from django.db import models
from django.core.files import File
    
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex 
from diana.storages import OriginalFileStorage, IIIFFileStorage

from PIL import Image
from typing import *
import uuid
import os
import pyvips

TIFF_KWARGS = {
    "tile": True, 
    "pyramid": True, 
    "compression": 'jpeg', 
    "Q": 89, 
    "tile_width": 256, 
    "tile_height": 256
}

DEFAULT_FIELDS  = ['created_at', 'updated_at', 'published']
DEFAULT_EXCLUDE = ['created_at', 'updated_at', 'published', 'polymorphic_ctype']


def get_fields(model: models.Model, exclude=DEFAULT_EXCLUDE):
    return [field.name for field in (model._meta.fields + model._meta.many_to_many) if field.name not in exclude]

def get_many_to_many_fields(model: models.Model, exclude=DEFAULT_EXCLUDE):
    return [field.name for field in (model._meta.many_to_many) if field.name not in exclude]

def get_media_directory(instance: models.Model, label: str):

    # Fetches the app name, e.g. 'arosenius'
    app = instance._meta.app_label
    
    # Resulting directory is e.g. 'arosenius/iiif/'
    return os.path.join(app, label)


def get_save_path(instance: models.Model, filename, label: str):

    # Fetches the closest directory
    directory = get_media_directory(instance, label)
    
    # Resulting directory is e.g. 'arosenius/iiif/picture.jpg'
    return os.path.join(directory, filename)


def get_iiif_path(instance: models.Model, filename):

    return get_save_path(instance, filename, "iiif")

def get_original_path(instance: models.Model, filename):

    return get_save_path(instance, filename, "original")


#####################################################
class CINameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(CINameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


########################################################

class AbstractBaseModel(models.Model):
    """Abstract base model for all new tables in the Diana backend.
    Supplies all rows with datetimes for publication and modification, 
    as well as a toggle for publication.
    """
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published  = models.BooleanField(default=True)

    class Meta:
        abstract = True


##########################################################


class AbstractTagModel(AbstractBaseModel):
    """Abstract model which creates a simple tag with a case-insensitive text field.
    """
    text = CINameField(max_length=256)

    class Meta:
        abstract = True


##########################################################

class AbstractImageModel(AbstractBaseModel):
    """Abstract image model for new image models in the Diana backend. Supplies all images
    with a corresponding UUID and file upload.

    Args:
        AbstractBaseModel (models.Model): The abstract base model for all models in Diana
    """

    # Create an automatic UUID signifier
    # This is used mainly for saving the images on the IIIF server
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    # The name of a supplied field is available in file.name
    file = models.ImageField(storage=OriginalFileStorage, upload_to=get_original_path)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.file}"


class AbstractTIFFImageModel(AbstractImageModel):
    """
    Abstract image model for new TIFF images in the Diana backend. Beside supplying all images with a 
    UUID and file, it also dynamically generates a pyramidization of the input file, saving it to the IIIF storage.
    """

    class Meta:
        abstract = True

    # The path to the IIIF file
    iiif_file = models.ImageField(storage=IIIFFileStorage, upload_to=get_iiif_path, blank=True, null=True)

    def _save_tiled_pyramid_tif(self, path=IIIFFileStorage().location):
        """Uses pyvips to generate a tiled pyramid tiff.

        Args:
            path (str, optional): The path to save the images. Defaults to IIIF_PATH.
        """

        # The images are saved with their uuid as the key
        filename = str(self.uuid) + ".tif"
        out_path = os.path.join(path, get_iiif_path(self, filename))

        tmp_name = get_iiif_path(self, f"{str(self.uuid)}_tmp.tif")
        tmp_path = os.path.join(path, tmp_name)


        # When updating the file, remove the iiif_file
        # print(out_path)
        if os.path.isfile(out_path):
            os.remove(out_path)
            self.iiif_file.delete(False) # Do not yet save the image deletion

        # Get the original image as a Pillow object before saving
        image_object = Image.open(self.file.open())
        image = pyvips.Image.new_from_array(image_object)
                
        # Create temporary file
        image.tiffsave(tmp_path, **TIFF_KWARGS)

        # Prepare saving the new IIIF file
        with open(tmp_path, 'rb') as f:
            tiff_image = File(f) 
            self.iiif_file.save(filename, tiff_image, save=False)
        
        # Remove the temporary path
        if os.path.isfile(tmp_path):
            os.remove(tmp_path)

    def save(self, **kwargs) -> None:

        self._save_tiled_pyramid_tif()

        super().save(**kwargs)



class AbstractDocumentModel(AbstractBaseModel):
    """
    The abstract document model supplies a model with an automatic UUID field, a text field as well as
    a text_vector field. The text_vector may be used as a generated column to hold a tokenized version of
    the text field. This must be generated for example by means of a PostgreSQL trigger, however
    """

    # Create an automatic UUID signifier
    # This is used mainly for saving the images on the IIIF server
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    # The textual content
    text    = models.TextField(default="")

    # The text vector is a generated column which holds
    # tokenized versions of all columns which should be searchable
    # Performance is vastly improved if accompanied by a manual migration 
    # which adds this column automatically, instead of at runtime
    text_vector = SearchVectorField(null=True)

    class Meta:
        abstract = True
        indexes = (GinIndex(fields=["text_vector"]),)

    def __str__(self) -> str:
        return f"{self.text[0:50]}"