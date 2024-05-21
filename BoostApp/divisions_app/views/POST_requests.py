from rest_framework import generics

from ..models import Division
from ..serializers import DivisionSerializer
from helper_files.permissions import AdminOnly
from helper_files.status_code import Status_code
from helper_files.permissions import Permissions
from ..validations import DivisionAppValidations
from django.conf import settings

from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class DivisionCreate(generics.CreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = [AdminOnly]

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def check_object_permissions(self, request, obj):
        Permissions.check_object_permissions(self=self, request=request, obj=obj)

    def create(self, request, *args, **kwargs):
        if 'game_id' in request.data:
            request.data._mutable = True
            game_id = aes.decrypt(str(request.data['game_id']))
            request.data['game_id'] = game_id
        serializer = self.get_serializer(data=request.data)
        valid, err = serializer.is_valid(raise_exception=False)
        response = DivisionAppValidations.validate_division_create(self.request.data, valid, err)
        if response.status_code == Status_code.created:
            serializer.save()

        return response
