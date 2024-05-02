from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ..models import Game
from ..serializers import GameSerializer
from helper_files.permissions import AdminOrManager, Permissions, AdminOnly
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class GameDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

    permission_classes = [AdminOnly]

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def check_object_permissions(self, request, obj):
        Permissions.check_object_permissions(self=self, request=request, obj=obj)

    def get_object(self):
        try:
            pk = aes.decrypt(str(self.kwargs['game_id']))
            game = Game.objects.filter(pk=int(pk))
            obj = game[0]
        except:
            return ValueError('wrong id format')
        if game.count() == 0:
            return ValueError('wrong id format')

        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,Game):
            return Response(data={"message": "Game wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        return super().update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,Game):
            return Response(data={"message": "Game wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,Game):
            return Response(data={"message": "Game wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "Game was deleted successfully.",
                              "status": Status_code.no_content}, status=Status_code.no_content)
