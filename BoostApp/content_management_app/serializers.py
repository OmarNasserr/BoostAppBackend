from rest_framework import serializers
from .models import ContactUs
from helper_files.serializer_helper import SerializerHelper
from helper_files.cryptography import AESCipher
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        exclude = ('submitted_at')

    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self, raise_exception=raise_exception)

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id', ]
        )##