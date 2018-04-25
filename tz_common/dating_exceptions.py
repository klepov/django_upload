from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response


# !sector ENUM

class NotOwnerImage(APIException):
    status_code = 403
    default_detail = 'не хозяин изображения'
    default_code = 'это фиаско, братан'

class ImageNotFound(APIException):
    status_code = 404
    default_detail = 'нет такого изображения'
    default_code = 'это фиаско, братан'

