from django.urls import path, include
from .views.POST_requests import ContactUsCreate

urlpatterns = [
    path('create/', ContactUsCreate.as_view(), name='contact-us-create'),
]
