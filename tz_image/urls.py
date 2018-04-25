from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tz_image.views import UploadImageView,  GetImageByLink

urlpatterns = [
    path('upload/', UploadImageView.as_view()),
    path('<str:pk>/', GetImageByLink.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
