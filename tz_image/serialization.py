import datetime

import os
import uuid

from rest_framework import serializers

from django_upload import settings
from tz_common.serializers_common import CurrentProfileDefault
from tz_image.models import Image, Resolution
from tz_image.tasks import upload_pic
from tz_profile.models import Profile


class ResolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resolution
        exclude = ('link',
                   'original')

    height = serializers.IntegerField(required=False)
    width = serializers.IntegerField(required=False)
    quality = serializers.IntegerField(required=False)


class ImageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

    owner = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), default=CurrentProfileDefault())

    def to_internal_value(self, data):

        return super().to_internal_value(data)

    def create(self, validated_data):
        # вырываем прямо из контекста данные, потому что nested serializer не вызывается из-за того,
        # что нет правильного content-type
        results = None

        cached_pic_url = []

        resolution_raw = self.context.get('request').data.get('resolution')

        validated_data.get('original').name = "{}.{}".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                                                             validated_data.get('original').content_type.split(
                                                                 '/')[
                                                                 1])
        original = super().create(validated_data)
        original.link = original.original.url.split('/')[3]
        original.save()

        if resolution_raw:
            resolution_serializer = ResolutionSerializer(data=resolution_raw, many=True, )
            if resolution_serializer.is_valid(raise_exception=True):
                results = GenerateImageCache(original, resolution_serializer.validated_data).generate()

        if results:
            for result in results:
                name = result.get('name')
                Resolution.objects.create(link=name, original=original)

                cached_pic_url.append(
                    {"link": "%s%s" % (settings.CACHE_media, name)})

        result_dict = {"original": original.original.url}
        if cached_pic_url:
            result_dict["resize"] = cached_pic_url

        return result_dict

    def to_representation(self, instance):
        if type(instance) == dict:
            return instance
        return ImageReadSerializer(instance).data


class ResolutionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resolution
        fields = ("link",)

    def to_representation(self, instance):
        return super().to_representation(instance)


class ImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("original","resize")

    resize = ResolutionReadSerializer(many=True,  source='resolution_set')


class GenerateImageCache:

    def __init__(self, image, params=None):
        self.image = image
        self.params = params

    def generate(self):
        result_gen = []

        for param in self.params:
            ext = param.get('format_required')

            if ext is None:
                param['format_required'] = os.path.splitext(self.image.original.url)[1].replace('.', '')

            filename = "%s.%s" % (uuid.uuid4().hex, param.get('format_required'))

            upload_pic.delay(self.image.id, filename, **param)

            print(filename)
            result_gen.append({"name": filename})

        return result_gen