from rest_framework.response import Response
from rest_framework import status
import re
from helper_files.status_code import Status_code
from django.contrib.auth.models import User
from helper_files.cryptography import AESCipher
from django.conf import settings
aes = AESCipher(settings.SECRET_KEY[:16], 32)


class ReviewAppValidations():

    @staticmethod
    def decrypt_ids_in_request(data):
        for key in data:
            keys = ['reviewer','reviewee']
            if key in keys:
                try:
                    data[key] = aes.decrypt(str(data[key]))
                except:
                    return Response(data={'message': "Wrong id format for " + key,
                                          'status': Status_code.bad_request},
                                    status=Status_code.bad_request)

        return Response(data={"message": "Success.",
                              "data": data,
                              'status': Status_code.success,
                              },
                        status=Status_code.success)
    @staticmethod
    def validate_review_create(data, valid, err):

        if valid:
            if data['reviewer'] == data['reviewee']:
                return Response(data={'message': "Reviewer can't review himself.",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if len(data['review']) < 2:
                return Response(data={'message': "Review can't be less than two characters.",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            else:
                return Response(data={"message": "Review was added successfully.",
                                      'status': Status_code.created},
                                status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)

    @staticmethod
    def validate_review_update(data, valid, err):
        if valid:
            if 'reviewer' in data or 'reviewee' in data:
                return Response(data={'message': "Review's reviewer and reviewee can't be changed.",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if len(data['review']) < 2:
                return Response(data={'message': "Review can't be less than two characters",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if len(data['review']) > 150:
                return Response(data={'message': "Review can't be more than 150 characters",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            else:
                return Response(data={"message": "Review was updated successfully.",
                                      'status': Status_code.created},
                                status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)
