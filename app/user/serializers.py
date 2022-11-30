"""
Serializers for the API view.
"""
#https://www.django-rest-framework.org/api-guide/serializers/
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
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

    def update(self, instance, validated_data):
        """Update and return user."""
        # instance is the Model instance to be updated
        password = validated_data.pop('password', None) # remove pass from dict
        user = super().update(instance, validated_data)

        if password: # changing password is optional
            user.set_password(password) # password is stored unhashed by default
            user.save()
        
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False, # allow space at the end of pass
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs
