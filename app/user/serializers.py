"""
Serializers for the API view.
"""
#https://www.django-rest-framework.org/api-guide/serializers/
from django.contrib.auth import get_user_model
from rest_framework import serializers


# Serializers are ways to conver objects from and to
# python objects. Takes json data, validates it, and
# turns it into an object or a model.
class UserSerializer(serializers.ModelSerializer):
    """Srializer for the user objects."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        # The default create method just creates a user without
        # encrypting the password.
        ### Serializers are just Forms for REST API's... ###
        return get_user_model().objects.create_user(**validated_data)
