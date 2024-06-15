# views.py
from rest_framework import generics, permissions
from ..models import Room, Message
from ..serializers import RoomSerializer, MessageSerializer
from ..pagination import ChatPagination
from helper_files.custom_exceptions import CustomException
from helper_files.status_code import Status_code
from helper_files.permissions import Permissions
from ..validations import ChatAppValidations


from django.conf import settings
from helper_files.cryptography import AESCipher
aes = AESCipher(settings.SECRET_KEY[:16], 32)


class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    pagination_class = ChatPagination

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Room.objects.all()
        return Room.objects.filter(player=user) | Room.objects.filter(booster=user)

    def perform_create(self, serializer):
        serializer.save()
    def get(self, request, *args, **kwargs):
        ChatPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def get_object(self):
        try:
            pk = aes.decrypt(str(self.kwargs['room_id']))
            room = Room.objects.filter(pk=int(pk))
            obj = room.first()
            self.check_object_permissions(self.request, obj)
            return obj
        except:
            raise CustomException(detail='No rooms were found for this ID.',status_code=Status_code.no_content)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    pagination_class = ChatPagination

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        if room_id:
            return Message.objects.filter(room__id=room_id)
        return Message.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        validation_response = ChatAppValidations.validate_messages_get(self.kwargs)
        if validation_response.status_code != Status_code.success:
            return validation_response

        self.kwargs = validation_response.data['kwargs']
        print('kww ',self.kwargs)
        ChatPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
