from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import BoostingRequestSerializer
from ..models import BoostingRequest
from ..pagination import BoostingRequestPagination
from helper_files.cryptography import AESCipher
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class BoostingRequestList(generics.ListAPIView):
    serializer_class = BoostingRequestSerializer
    queryset = BoostingRequest.objects.all()

    pagination_class = BoostingRequestPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['player_id', 'game_id', 'current_division_id', 'desired_division_id', 'is_approved',
                        'created_at']
    search_fields = ['player_id', 'game_id', 'current_division_id', 'desired_division_id', 'is_approved', 'created_at']

    def get(self, request, *args, **kwargs):
        if 'player_id' in self.kwargs:
            self.kwargs['player_id'] = aes.decrypt(str(self.kwargs['player_id']))
        BoostingRequestPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
