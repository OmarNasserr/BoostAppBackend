from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from helper_files.custom_exceptions import CustomException
from ..models import Division
from ..serializers import DivisionSerializer
from helper_files.permissions import AdminOrManager, Permissions, AdminOnly
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from ..validations import DivisionAppValidations

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class DivisionDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DivisionSerializer
    queryset = Division.objects.all()

    permission_classes = [AdminOnly]

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def check_object_permissions(self, request, obj):
        Permissions.check_object_permissions(self=self, request=request, obj=obj)

    def get_object(self):
        try:
            pk = aes.decrypt(str(self.kwargs['division_id']))
            division = Division.objects.filter(pk=int(pk))
            obj = division[0]
            self.check_object_permissions(self.request, obj)
            return obj
        except:
            raise CustomException(detail='No divisions were found for this ID.',status_code=Status_code.bad_request)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,Division):
            return Response(data={"message": "Division wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        else:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data,partial=partial)
            valid, err = serializer.is_valid(raise_exception=False)
            response = DivisionAppValidations.validate_division_update(self.request.data, valid, err)
            if response.status_code == Status_code.updated:
                serializer.save()

            return response

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,Division):
            return Response(data={"message": "Division wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,Division):
            return Response(data={"message": "Division wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "Division was deleted successfully.",
                              "status": Status_code.no_content}, status=Status_code.no_content)
