import io
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from dating_image.models import Image as ImageModel
from PIL import Image

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

class CrewUploadPhotoTests(APITestCase):
    fixtures = []

    maxDiff = None

    def setUp(self):
        self.user = User(username="user", password=User.objects.make_random_password())
        self.user.save()
        Token.objects.create(user=self.user)
        Profile.objects.create(user=self.user, name="profile")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_upload_photo(self):
        photo_file = self.generate_photo_file()

        data = {
            'image': photo_file
        }

        response = self.client.post('/api/image/upload/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ImageModel.objects.count(), 1)
        self.assertEqual(response.data.get('id'), ImageModel.objects.get().pk)

    def test_delete_image(self):
        self.test_upload_photo()
        response = self.client.delete('/api/image/delete/{}/'.format(ImageModel.objects.get().pk))
        self.assertEqual(response.status_code, 204)

    def test_delete_image_not_owner(self):
        self.test_upload_photo()
        self.user1 = User.objects.create(username='test1', password='test1')
        Token.objects.create(user=self.user1)
        self.user1.save()
        self.profile1 = Profile(
            user=self.user1,
            name="ivan1",
            bdate=datetime(1997,1,1).date(),
            orientation=1,
            smoke=1,
        )
        self.profile1.save()

        self.client.force_authenticate(user=self.user1)

        response = self.client.delete('/api/image/delete/{}/'.format(ImageModel.objects.get().pk))

        self.assertEqual(response.status_code, 403)
        self.client.force_authenticate(user=self.user)
