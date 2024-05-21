from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import BoostingRequestSerializer
from ..models import BoostingRequest
from ..pagination import BoostingRequestPagination
from ..validations import BoostingRequestAppValidations
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class BoostingRequestList(generics.ListAPIView):
    serializer_class = BoostingRequestSerializer
    queryset = BoostingRequest.objects.all()

    pagination_class = BoostingRequestPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['player_id', 'booster_id', 'game_id', 'current_division_id', 'desired_division_id',
                        'is_confirmed', 'is_applied', 'is_completed', 'is_cancelled',
                        'payment_amount', 'updated_at', 'cancelled_at']
    search_fields = ['player_id', 'booster_id', 'game_id', 'current_division_id', 'desired_division_id',
                     'is_confirmed', 'is_applied', 'is_completed', 'is_cancelled',
                     'payment_amount', 'updated_at', 'cancelled_at']

    def get(self, request, *args, **kwargs):
        validation_response = BoostingRequestAppValidations.validate_br_get(self.kwargs)
        if validation_response.status_code != Status_code.success:
            return validation_response

        self.kwargs = validation_response.data['kwargs']
        BoostingRequestPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
