from rest_framework.response import Response
from rest_framework import status
import re
from helper_files.status_code import Status_code
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class BoostingRequestAppValidations():

    @staticmethod
    def validate_br_create(data, valid, err):

        if valid:
            # if len(data['name']) < 2:
            #     return Response(data={'message': "Boosting Request's name can't be less than two characters",
            #                           'status': Status_code.bad_request},
            #                     status=Status_code.bad_request)
            # if len(data['name']) > 30:
            #     return Response(data={'message': "Boosting Request's name can't be more than 20 characters",
            #                           'status': Status_code.bad_request},
            #                     status=Status_code.bad_request)
            # else:
            return Response(data={"message": "Boosting Request was added successfully.",
                                  'status': Status_code.created},
                            status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)

    @staticmethod
    def validate_br_update(data, valid, err):
        if valid:
            # if len(data['name']) < 2:
            #     return Response(data={'message': "Boosting Request's name can't be less than two characters",
            #                           'status': Status_code.bad_request},
            #                     status=Status_code.bad_request)
            # if len(data['name']) > 30:
            #     return Response(data={'message': "Boosting Request's name can't be more than 20 characters",
            #                           'status': Status_code.bad_request},
            #                     status=Status_code.bad_request)
            # else:
            return Response(data={"message": "Boosting Request was updated successfully.",
                                  'status': Status_code.created},
                            status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)


class CalculatePriceValidation():

    @staticmethod
    def validate_calculate_price(data):
        if aes.decrypt(data['current_division_id']) == data['desired_division_id']:
            return Response(data={'message': "The current division must be different from the desired division",
                                  'status': Status_code.bad_request},
                            status=Status_code.bad_request)
        return Response(data={"message": "Ok.",
                              'status': Status_code.success},
                        status=Status_code.success)
