# Create your views here.
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from tz_common.dating_exceptions import NotOwnerImage, ImageNotFound
from dating_image.models import Image
from tz_image.serialization import ImageWriteSerializer


class UploadImageView(CreateAPIView):
    serializer_class = ImageWriteSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class DeleteImageView(DestroyAPIView):
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            obj = Image.objects.get(id=self.kwargs.get('pk'))
        except Image.DoesNotExist:
            raise ImageNotFound()
        if obj.owner != self.request.user.profile:
            raise NotOwnerImage()
        return obj
