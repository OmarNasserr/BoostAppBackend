from django.urls import path, include
from .views.POST_requests import BoostingRequestCreate
from .views.GET_requests import BoostingRequestList
from .views.PUT_DEL_requests import BoostingRequestDetailUpdateDelete
from .views.calculate_price import calculate_price

urlpatterns = [
    path('create/', BoostingRequestCreate.as_view(), name='boosting-req-create'),
    path('calculate_price/', calculate_price, name='calculate-price'),
    path('list/', BoostingRequestList.as_view(), name='boosting-req-list'),
    path('<path:boosting_req_id>/detail/', BoostingRequestDetailUpdateDelete.as_view(), name='boosting-req-detail'),
]
