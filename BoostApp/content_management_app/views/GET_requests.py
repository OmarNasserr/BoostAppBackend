from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import ContactUsSerializer
from ..models import ContactUs
from ..pagination import ContactUsPagination
from django.utils.dateparse import parse_date



class ContactUsList(generics.ListAPIView):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()

    pagination_class = ContactUsPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['name', 'email', 'number', 'submitted_at']
    search_fields = ['name', 'email', 'number', 'submitted_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        submitted_at_start = self.request.query_params.get('submitted_at_start')
        submitted_at_end = self.request.query_params.get('submitted_at_end')

        if submitted_at_start and submitted_at_end:
            start_date = parse_date(submitted_at_start)
            end_date = parse_date(submitted_at_end)
            if start_date and end_date:
                queryset = queryset.filter(submitted_at__date__range=[start_date, end_date])

        return queryset
    def get(self, request, *args, **kwargs):
        ContactUsPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
