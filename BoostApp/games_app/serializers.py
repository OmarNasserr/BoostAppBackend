from rest_framework import serializers

from .models import Game, GameImage
from helper_files.serializer_helper import SerializerHelper
from helper_files.cryptography import AESCipher
from datetime import datetime
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class GameImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameImage
        fields = ["id", "image", "thumbnail", ]

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )


class GameSerializer(serializers.ModelSerializer):
    pics_from_the_game = GameImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, use_url=False),
        write_only=True,
    )

    class Meta:
        model = Game
        exclude = ('created_at', 'updated_at',)

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        game = Game.objects.create(**validated_data)

        create_thumbnail = True
        for image in uploaded_images:
            GameImage.objects.create(game=game, image=image, thumbnail=create_thumbnail)
            create_thumbnail = False

        return game

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')

        create_thumbnail = False
        for image in uploaded_images:
            GameImage.objects.create(game=instance, image=image, thumbnail=create_thumbnail)

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
