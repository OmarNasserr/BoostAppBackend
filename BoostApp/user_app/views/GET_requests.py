from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import UserSerializer
from ..models import BUser
from ..pagination import UsersPagination


class UsersList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = BUser.objects.all()
    
    pagination_class=UsersPagination  

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    filterset_fields=['username','is_staff','is_superuser','is_booster','is_player']
    search_fields = ['username','is_staff','is_superuser','is_booster','is_player']
    
    def get(self, request, *args, **kwargs):
        UsersPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
    