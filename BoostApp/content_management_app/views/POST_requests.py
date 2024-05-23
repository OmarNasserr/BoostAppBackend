from rest_framework import generics

from ..models import ContactUs
from ..serializers import ContactUsSerializer
from helper_files.status_code import Status_code
from ..validations import ContactUsAppValidations


class ContactUsCreate(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid, err = serializer.is_valid(raise_exception=False)
        response = ContactUsAppValidations.validate_contact_create(self.request.data, valid, err)
        if response.status_code == Status_code.created:
            serializer.save()

        return response
