from rest_framework import serializers

from .models import Division, DivisionImage
from helper_files.serializer_helper import SerializerHelper
from helper_files.cryptography import AESCipher
from datetime import datetime
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class DivisionIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivisionImage
        fields = ["id", "image", ]

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )


class GameSerializer(serializers.ModelSerializer):
    division_icon = DivisionIconSerializer(many=False, read_only=True)

    uploaded_icon = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, use_url=False),
        write_only=True,
    )

    class Meta:
        model = Division
        exclude = ('created_at', 'updated_at',)

    def create(self, validated_data):
        uploaded_icon = validated_data.pop('uploaded_icon')
        game = Division.objects.create(**validated_data)

        for image in uploaded_icon:
            DivisionImage.objects.create(game=game, image=image)
            break

        return game

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')


        division_icon = DivisionImage.objects.filter(game=instance)
        print("DIVISION ICON FILTER ",division_icon)
        for image in uploaded_images:
            division_icon.update(image=image)
            # DivisionImage.objects.create(game=instance, image=image)
            break

        instance.updated_at = str(datetime.now().strftime("%d %b, %Y - %Ih%Mm%S %p"))
        instance = super().update(instance, validated_data)
        return instance

    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self, raise_exception=raise_exception)

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )
