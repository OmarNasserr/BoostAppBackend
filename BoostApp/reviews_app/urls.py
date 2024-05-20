from urllib import request
from django.urls import path, include
from .views.POST_requests import ReviewCreate
from .views.GET_requests import ReviewsList
from .views.PUT_DEL_requests import ReviewDetailUpdateDelete

urlpatterns = [
    path('create/', ReviewCreate.as_view(), name='review-create'),
    path('list/', ReviewsList.as_view(), name='review-list'),
    path('<path:review_id>/detail/', ReviewDetailUpdateDelete.as_view(), name='review-detail'),
]
