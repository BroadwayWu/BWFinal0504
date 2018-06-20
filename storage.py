from django.core.files.storage import FileSystemStorage
# from django.conf import settings
import os

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.exists(name):
            os.remove(os.path.join(BASE_DIR, 'pic/'+name))
        return name