import os
import time


from django_upload.celery import app

from imagekit import ImageSpec
from imagekit.processors import ResizeToFit, ResizeToFill

from django_upload.settings import IMAGEKIT_CACHEFILE_DIR
from tz_image.models import Image as ImageModel


class GenerateProcessor(ImageSpec):

    def __init__(self, source, name, **kwargs):
        self.width, self.height = source.width, source.height
        self.resolution = kwargs
        source = source.file
        quality = kwargs.get('quality')
        self.name = name
        self.format = kwargs.pop('format_required')
        if self.format in ('jpg', 'jpeg') and quality:
            self.options = {'quality': quality}
        super().__init__(source)

    @property
    def cachefile_name(self):
        return self.name

    def generate(self):
        if self.resolution:
            height_required = self.resolution.get('height')
            width_required = self.resolution.get('width')
            if height_required and width_required:
                self.processors = [ResizeToFill(width_required, height_required)]
                return super().generate()
            if height_required:
                self.processors = [ResizeToFit((self.width) / (self.height / height_required), height_required)]
                return super().generate()
            elif width_required:
                self.processors = [ResizeToFit((self.height) / (self.width / width_required), width_required)]
                return super().generate()


@app.task
def upload_pic(image_id, name, **kwargs):
    image = ImageModel.objects.get(id=image_id).original
    time.sleep(10)
    image_generator = GenerateProcessor(source=image, name=name, **kwargs)

    result = image_generator.generate()
    if result is None:
        return
    if not os.path.exists(IMAGEKIT_CACHEFILE_DIR):
        os.mkdir(IMAGEKIT_CACHEFILE_DIR)
    file = open(os.path.join(IMAGEKIT_CACHEFILE_DIR, image_generator.cachefile_name), 'wb')
    file.write(result.read())
    file.close()
