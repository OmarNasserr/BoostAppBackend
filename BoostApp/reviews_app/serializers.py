from rest_framework import serializers
from .models import Review
from helper_files.serializer_helper import SerializerHelper
from datetime import datetime


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('created_at', 'updated_at',)

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
            fields_to_be_encrypted=['id', 'reviewer', 'reviewee']
        )
