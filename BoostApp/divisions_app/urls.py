from urllib import request
from django.urls import path, include
from .views.POST_requests import GameCreate
from .views.GET_requests import GamesList
from .views.PUT_DEL_requests import GameDetailUpdateDelete

urlpatterns = [
    path('create/', GameCreate.as_view(), name='game-create'),
    path('list/', GamesList.as_view(), name='game-list'),
    path('<path:game_id>/detail/', GameDetailUpdateDelete.as_view(), name='game-detail'),
]
