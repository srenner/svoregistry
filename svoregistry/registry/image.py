# -*- coding: utf-8 -*-
from PIL import Image #@UnresolvedImport

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.db.models.fields.files import ImageField, ImageFieldFile
from django.core.files.base import ContentFile


def _update_ext(filename, new_ext):
    parts = filename.split('.')
    parts[-1] = new_ext
    return '.'.join(parts)


class ResizedImageFieldFile(ImageFieldFile):
    
    def save(self, name, content, save=True):
        new_content = StringIO()
        content.file.seek(0)

        img = Image.open(content.file)
        img.thumbnail((
            self.field.max_width, 
            self.field.max_height
            ), Image.ANTIALIAS)
        img.save(new_content, format=self.field.format)

        new_content = ContentFile(new_content.getvalue())
        new_name = _update_ext(name, self.field.format.lower())

        super(ResizedImageFieldFile, self).save(new_name, new_content, save)


class ResizedImageField(ImageField):
    
    attr_class = ResizedImageFieldFile

    def __init__(self, max_width=850, max_height=1000, format='JPG', *args, **kwargs):
        self.max_width = max_width
        self.max_height = max_height
        self.format = format
        super(ResizedImageField, self).__init__(*args, **kwargs)