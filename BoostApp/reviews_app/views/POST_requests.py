from rest_framework import generics

from ..models import Review
from ..serializers import ReviewSerializer
from helper_files.permissions import AdminOnly
from helper_files.status_code import Status_code
from helper_files.permissions import Permissions
from ..validations import ReviewAppValidations


class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        decrypt_ids_response = ReviewAppValidations.decrypt_ids_in_request(request.data)
        if decrypt_ids_response.status_code != Status_code.success:
            return decrypt_ids_response
        serializer = self.get_serializer(data=request.data)
        valid, err = serializer.is_valid(raise_exception=False)
        response = ReviewAppValidations.validate_review_create(self.request.data, valid, err)
        if response.status_code == Status_code.created:
            serializer.save()

        return response
