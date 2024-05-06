from rest_framework import generics

from ..models import BoostingRequest
from ..serializers import BoostingRequestSerializer
from helper_files.permissions import AdminOnly
from helper_files.status_code import Status_code
from helper_files.permissions import Permissions
from ..validations import BoostingRequestAppValidations

from helper_files.cryptography import AESCipher
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)

class BoostingRequestCreate(generics.CreateAPIView):
    queryset = BoostingRequest.objects.all()
    serializer_class = BoostingRequestSerializer
    # permission_classes = [AdminOnly]

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def check_object_permissions(self, request, obj):
        Permissions.check_object_permissions(self=self, request=request, obj=obj)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        if 'player_id' in request.data:
            request.data['player_id'] = aes.decrypt(str(request.data['player_id']))
        if 'game_id' in request.data:
            request.data['game_id'] = aes.decrypt(str(request.data['game_id']))
        if 'current_division_id' in request.data:
            request.data['current_division_id'] = aes.decrypt(str(request.data['current_division_id']))
        if 'desired_division_id' in request.data:
            request.data['desired_division_id'] = aes.decrypt(str(request.data['desired_division_id']))
        serializer = self.get_serializer(data=request.data)
        valid, err = serializer.is_valid(raise_exception=False)
        response = BoostingRequestAppValidations.validate_br_create(self.request.data, valid, err)
        if response.status_code == Status_code.created:
            serializer.save()

        return response
