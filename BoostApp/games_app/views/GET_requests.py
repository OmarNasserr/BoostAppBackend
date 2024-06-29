from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import GameSerializer
from ..models import Game
from ..pagination import GamesPagination


class GamesList(generics.ListAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all().order_by('id')

    pagination_class = GamesPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['name', 'most_popular', ]
    search_fields = ['name', 'most_popular', ]

    def get(self, request, *args, **kwargs):
        print('IN GETTT')
        GamesPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
