from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from helper_files.custom_exceptions import CustomException
from ..models import BUser
from ..serializers import UserSerializer
from helper_files.permissions import AdminOrManager, Permissions
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class UserDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = BUser.objects.all()

    permission_classes = [AdminOrManager]

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def check_object_permissions(self, request, obj):
        Permissions.check_object_permissions(self=self, request=request, obj=obj)

    def get_object(self):
        try:
            pk = aes.decrypt(str(self.kwargs['user_id']))
            user = BUser.objects.filter(pk=int(pk))
            obj = user[0]
            self.check_object_permissions(self.request, obj)
            return obj
        except:
            raise CustomException(detail='No user was found for this ID.',status_code=Status_code.bad_request)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,BUser):
            return Response(data={"message": "User wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        return super().update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,BUser):
            return Response(data={"message": "User wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,BUser):
            return Response(data={"message": "User wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "User was deleted successfully.",
                              "status": Status_code.no_content}, status=Status_code.no_content)
