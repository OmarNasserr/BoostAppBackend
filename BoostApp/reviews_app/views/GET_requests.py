from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import ReviewSerializer
from ..models import Review
from ..pagination import ReviewsPagination


class ReviewsList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    pagination_class = ReviewsPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['reviewer', 'reviewee', ]
    search_fields = ['reviewer', 'reviewee', ]

    def get(self, request, *args, **kwargs):
        ReviewsPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
