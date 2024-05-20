from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ..models import Review
from ..serializers import ReviewSerializer
from helper_files.permissions import Permissions
from ..permissions import IsReviewOwnerOrAdmin
from ..validations import ReviewAppValidations
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class ReviewDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    permission_classes = [IsReviewOwnerOrAdmin]

    def permission_denied(self, request, message=None, code=None):
        Permissions.permission_denied(self=self, request=request)

    def check_object_permissions(self, request, obj):
        Permissions.check_object_permissions(self=self, request=request, obj=obj)

    def get_object(self):
        try:
            pk = aes.decrypt(str(self.kwargs['review_id']))
            review = Review.objects.filter(pk=int(pk))
            obj = review[0]
        except:
            return ValueError('wrong id format')
        if review.count() == 0:
            return ValueError('wrong id format')

        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,Review):
            return Response(data={"message": "Review wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        else:
            request.data._mutable = True
            decrypt_ids_response = ReviewAppValidations.decrypt_ids_in_request(request.data)
            if decrypt_ids_response.status_code != Status_code.success:
                return decrypt_ids_response
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            valid, err = serializer.is_valid(raise_exception=False)
            response = ReviewAppValidations.validate_review_update(self.request.data, valid, err)
            if response.status_code == Status_code.updated:
                serializer.save()

            return response

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,Review):
            return Response(data={"message": "Review wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not isinstance(instance,Review):
            return Response(data={"message": "Review wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "Review was deleted successfully.",
                              "status": Status_code.no_content}, status=Status_code.no_content)
