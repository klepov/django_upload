from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from dating_image.views import UploadImageView, DeleteImageView

urlpatterns = [
    path('upload/', UploadImageView.as_view()),
    path('delete/<int:pk>/', DeleteImageView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
