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


class DivisionSerializer(serializers.ModelSerializer):
    division_icon = DivisionIconSerializer(many=True, read_only=True)

    uploaded_icon = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Division
        exclude = ('created_at', 'updated_at',)

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('name', 'game_id'),
                message="This division already exists in this game."
            )
        ]

    def create(self, validated_data):
        uploaded_icon = validated_data.pop('uploaded_icon')
        division = Division.objects.create(**validated_data)

        for image in uploaded_icon:
            DivisionImage.objects.create(division=division, image=image)
            break

        return division

    def update(self, instance, validated_data):
        if 'uploaded_icon' in validated_data:
            uploaded_icon = validated_data.pop('uploaded_icon')


            division_icon = DivisionImage.objects.filter(division=instance)
            for image in uploaded_icon:
                division_icon.update(image=image)
                # DivisionImage.objects.create(division=instance, image=image)
                break

        instance = super().update(instance, validated_data)
        instance.updated_at = str(datetime.now().strftime("%d %b, %Y - %Ih%Mm%S %p"))
        return instance

    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self, raise_exception=raise_exception)

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id','game_id']
        )
