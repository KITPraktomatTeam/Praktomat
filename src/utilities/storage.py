# -*- coding: utf-8 -*-

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class UploadStorage(FileSystemStorage):
    def __init__(self, location=settings.UPLOAD_ROOT,
                 base_url=settings.BASE_PATH + 'upload/', *args, **kwargs):
        super(UploadStorage, self).__init__(*args, **kwargs)
        self.location = os.path.abspath(location)
        self.base_url = base_url
