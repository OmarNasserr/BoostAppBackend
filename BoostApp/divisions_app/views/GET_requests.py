from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import DivisionSerializer
from ..models import Division
from ..pagination import DivisionPagination


class DivisionsList(generics.ListAPIView):
    serializer_class = DivisionSerializer
    queryset = Division.objects.all()

    pagination_class = DivisionPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['name', ]
    search_fields = ['name', ]

    def get(self, request, *args, **kwargs):
        DivisionPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
