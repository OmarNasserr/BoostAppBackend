from rest_framework.response import Response
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class ContactUsAppValidations:

    @staticmethod
    def validate_contact_create(data, valid, err):
        if valid:
            return Response(data={"message": "Request was sent successfully.",
                                  'status': Status_code.created},
                            status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)
