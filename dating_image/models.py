import PIL
import os
from PIL import ImageFilter, Image as image_pil
from django.db import models



class Image(models.Model):
    image = models.ImageField(upload_to='images')
    image_75 = models.TextField(blank=True, null=True)
    image_130 = models.TextField(blank=True, null=True)
    image_604 = models.TextField(blank=True, null=True)
    image_807 = models.TextField(blank=True, null=True)
    image_1280 = models.TextField(blank=True, null=True)
    image_2560 = models.TextField(blank=True, null=True)
    owner = models.ForeignKey('dating_profile.Profile', null=True, on_delete=models.CASCADE)
    blur_image = models.TextField(null=True)

    def get_blur_thumb(self):
        if self.blur_image:
            return self.blur_image
        ip = image_pil.open(os.path.join(IMAGEKIT_CACHEFILE_DIR, self.image_75))
        ip = ip.filter(ImageFilter.GaussianBlur(radius=2))
        blur_path = "%s_blur.jpg" % self.image.name.split('.')[0].replace('images/', '')
        ip.save(
            os.path.join(IMAGEKIT_CACHEFILE_DIR, blur_path))
        self.blur_image = blur_path
        self.save()
        return "http://176.56.50.175:8088/media/CACHE/" + self.blur_image
