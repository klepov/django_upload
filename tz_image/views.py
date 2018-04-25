import io
import json
# Create your views here.

import requests

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, DataAndFiles
from rest_framework.permissions import IsAuthenticated

from tz_common.dating_exceptions import ImageNotFound, NotOwnerImage
from tz_image.models import Image

from tz_image.serialization import ImageWriteSerializer, ImageReadSerializer


def get_pic_from_url(url):

    def getsize(f):
        f.seek(0)
        f.read()
        s = f.tell()
        f.seek(0)
        return s

    data_get = url
    if data_get:
        req = requests.get(data_get)
        image = io.BytesIO(req.content)
        return InMemoryUploadedFile(file=image, field_name=None, name=data_get,
                                    content_type=req.headers.get('content-type'),
                                    size=getsize(image), charset=None)


class MultipartJSONParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream, media_type, parser_context)
        data_imtb = result.data.copy()
        file_imtb = result.files.copy()
        resolution = data_imtb.get('resolution')
        if resolution:
            data_imtb['resolution'] = json.loads(resolution)
        if not result.files:
            file_imtb['original'] = get_pic_from_url(data_imtb.get('original'))
        return DataAndFiles(data_imtb, file_imtb)


class UploadImageView(CreateAPIView):
    serializer_class = ImageWriteSerializer
    # кастомный парсер для конверта из строки в джсон
    parser_classes = (MultipartJSONParser,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile

class GetImageByLink(RetrieveAPIView,DestroyAPIView):
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageReadSerializer

    def get_object(self):
        try:
            self.kwargs.get('pk')
            obj = Image.objects.get(link=self.kwargs.get('pk'))
        except Image.DoesNotExist:
            raise ImageNotFound()
        if obj.owner != self.request.user.profile:
            raise NotOwnerImage()
        return obj


