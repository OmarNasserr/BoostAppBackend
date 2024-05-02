from rest_framework import generics

from ..models import Division
from ..serializers import GameSerializer
from helper_files.permissions import AdminOnly
from helper_files.status_code import Status_code
from helper_files.permissions import Permissions
from ..validations import GameAppValidations


class GameCreate(generics.CreateAPIView):
    queryset = Division.objects.all()
    serializer_class = GameSerializer
    permission_classes = [AdminOnly]

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def check_object_permissions(self, request, obj):
        Permissions.check_object_permissions(self=self, request=request, obj=obj)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid, err = serializer.is_valid(raise_exception=False)
        response = GameAppValidations.validate_game_create(self.request.data, valid, err)
        if response.status_code == Status_code.created:
            serializer.save()

        return response
