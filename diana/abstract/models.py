from django.db import models
from django.conf import settings
from diana.storages import CDHDataFileStorage
import uuid
import os
import pyvips

def get_fields(model: models.Model, exclude=['id']):
    return [field.name for field in model._meta.fields if field.name not in exclude]

def get_save_path(instance: models.Model, filename, label: str):

    # Fetches the app name, e.g. 'arosenius'
    app = instance._meta.app_label
    
    # Resulting directory is e.g. 'arosenius/iiif/picture.jpg'
    return os.path.join(app, label, filename)

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
    file = models.ImageField(upload_to=lambda instance, filename: get_save_path(instance, filename, "original"))

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.file}"


class AbstractTIFFImageModel(AbstractImageModel):

    class Meta:
        abstract = True

    # The path to the IIIF file
    iiif_file = models.ImageField(upload_to=lambda instance, filename: get_save_path(instance, filename, "iiif"))

    def _save_tiled_pyramid_tif(self, path=CDHDataFileStorage.location):
        """Uses pyvips to generate a tiled pyramid tiff.

        Args:
            path (str, optional): The path to save the images. Defaults to IIIF_PATH.
        """

        # The images are saved with their uuid as the key
        out_path = os.path.join(path, get_save_path(self, str(self.uuid)+".tif", "iiif"))

        image = pyvips.Image.new_from_file(self.file.path)
        image.tiffsave(out_path, tile=True, pyramid=True, compression='jpeg', Q=89, tile_width=256, tile_height=256)

        # Assign the new path to the IIIF file field and save again
        self.iiif_file = out_path
        self.save()
        

    def save(self, *args, **kwargs) -> None:
        """Redefines the save protocol to ensure that a .tif copy is created 
        at the IIIF server destination. The original file is still saved in the media location.
        """

        success = super().save(*args, **kwargs)

        # Call the saving routine
        self._save_tiled_pyramid_tif()

        return success
