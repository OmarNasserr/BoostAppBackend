from django.urls import path, include
from .views.POST_requests import DivisionCreate
from .views.GET_requests import DivisionsList
from .views.PUT_DEL_requests import DivisionDetailUpdateDelete
from .views.GET_parent_divisions import get_parent_divisions

urlpatterns = [
    path('create/', DivisionCreate.as_view(), name='division-create'),
    path('list/', DivisionsList.as_view(), name='division-list'),
    path('get_parent_divisions/', get_parent_divisions, name='get-parent-divisions'),
    path('<path:division_id>/detail/', DivisionDetailUpdateDelete.as_view(), name='division-detail'),
]
