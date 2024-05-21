from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import DivisionSerializer
from ..models import Division
from ..pagination import DivisionPagination
from ..validations import DivisionAppValidations
from helper_files.status_code import Status_code


class DivisionsList(generics.ListAPIView):
    serializer_class = DivisionSerializer
    queryset = Division.objects.all()

    pagination_class = DivisionPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['name', 'game_id']
    search_fields = ['name', 'game_id']

    def get(self, request, *args, **kwargs):
        validation_response = DivisionAppValidations.validate_division_get(self.kwargs)
        if validation_response.status_code != Status_code.success:
            return validation_response

        self.kwargs = validation_response.data['kwargs']
        DivisionPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
