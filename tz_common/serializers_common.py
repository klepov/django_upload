from rest_framework import serializers


class CurrentProfileDefault(serializers.CurrentUserDefault):

    def set_context(self, serializer_field):
        super().set_context(serializer_field)
        self.user = self.user.profile
