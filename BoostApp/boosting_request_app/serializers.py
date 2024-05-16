from rest_framework import serializers

from .models import BoostingRequest
from helper_files.serializer_helper import SerializerHelper
from divisions_app.serializers import DivisionSerializer
from helper_files.cryptography import AESCipher
from datetime import datetime
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class BoostingRequestSerializer(serializers.ModelSerializer):
    divisions = DivisionSerializer(many=True, read_only=True)

    class Meta:
        model = BoostingRequest
        exclude = ('created_at', 'updated_at', 'completed_at', 'cancelled_at')

    def update(self, instance, validated_data):
        instance.updated_at = str(datetime.now().strftime("%d %b, %Y - %Ih%Mm%S %p"))
        instance = super().update(instance, validated_data)
        return instance

    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self, raise_exception=raise_exception)

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id', 'player_id', 'game_id', 'current_division_id', 'desired_division_id']
        )
