from django.urls import path
from .chat_views.GET_requests import RoomListCreateView, RoomDetailView, MessageListCreateView, MessageDetailView

urlpatterns = [
    path('rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<path:room_id>/', RoomDetailView.as_view(), name='room-detail'),
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),

]