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
        decrypt_ids_response = BoostingRequestAppValidations.decrypt_ids_in_request(request.data)
        if decrypt_ids_response.status_code != Status_code.success:
            return decrypt_ids_response
        serializer = self.get_serializer(data=request.data)
        valid, err = serializer.is_valid(raise_exception=False)
        response = BoostingRequestAppValidations.validate_br_create(self.request.data, valid, err)
        if response.status_code == Status_code.created:
            serializer.save()

        return response
