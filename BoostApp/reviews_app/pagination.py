from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import InvalidPage
from helper_files.status_code import Status_code
from helper_files.custom_exceptions import CustomException

class ReviewsPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page_number'  # defines the name of /?page_number=, default is page
    page_size_query_param = 'page_size'  # gives the user the ability to control the number of
    # items returned
    max_page_size = 10  # controls max number a user can return, therefore page_size_query_param max value = 10
    last_page_strings = 'last page'

    def get_paginated_response(self, data):
        return Response({
            'status': status.HTTP_200_OK,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total number of objects': self.page.paginator.count,
            'number of pages': self.page.paginator.num_pages,
            'results': data,

        })

    # in case page_number or page_size wasn't declared in the url params
    # this sets a default value that insures that the request is delivered safely
    def set_default_page_number_and_page_size(request):
        if 'page_size' in request.GET:
            pass
        else:
            request.GET._mutable = True
            request.GET['page_size'] = 3
        if 'page_number' in request.GET:
            pass
        else:
            request.GET._mutable = True
            request.GET['page_number'] = '1'

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise CustomException(detail=msg, status_code=Status_code.bad_request)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)
