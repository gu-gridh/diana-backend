from django.core.files.storage import FileSystemStorage
from django.conf import settings

class CDHDataFileStorage(FileSystemStorage):
    def __init__(self,) -> None:

        location = settings.MEDIA_ROOT
        base_url = settings.MEDIA_URL

        super().__init__(location, base_url)