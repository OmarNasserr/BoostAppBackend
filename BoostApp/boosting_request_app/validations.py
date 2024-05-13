from rest_framework.response import Response
from rest_framework import status
import re
from helper_files.status_code import Status_code
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from divisions_app.models import Division
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class BoostingRequestAppValidations:

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
            # if 'payment_amount' not in data:
            #     return Response(data={'message': "payment_amount is a required field",
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

    @staticmethod
    def validate_confirm_br(data, valid, err):
        if valid:
            if 'boosting_request_id' not in data:
                return Response(data={'message': "boosting_request_id is a required field",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if 'payment_amount' not in data:
                return Response(data={'message': "payment_amount is a required field",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            else:
                return Response(data={"message": "Boosting Request was confirmed successfully.",
                                      'status': Status_code.created},
                                status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)


class CalculatePriceValidation:

    @staticmethod
    def validate_calculate_price(data):
        if 'current_division_id' not in data:
            return Response(data={'message': "current_division_id is a required field",
                                  'status': Status_code.bad_request},
                            status=Status_code.bad_request)
        if 'desired_division_id' not in data:
            return Response(data={'message': "desired_division_id is a required field",
                                  'status': Status_code.bad_request},
                            status=Status_code.bad_request)
        try:
            current_division_id = int(aes.decrypt(data['current_division_id']))
            desired_division_id = int(aes.decrypt(data['desired_division_id']))
        except:
            return Response(data={'message': "Wrong id format.",
                                  'status': Status_code.bad_request},
                            status=Status_code.bad_request)
        try:
            current_div = Division.objects.get(id=current_division_id)
            desired_div = Division.objects.get(id=desired_division_id)
        except:
            return Response(data={'message': "No divisions found with the given ids.",
                                  'status': Status_code.bad_request},
                            status=Status_code.bad_request)
        if current_div.rank > desired_div.rank:
            return Response(data={'message': "Cannot boost to a division with a lower rank than your current division.",
                                  'status': Status_code.bad_request},
                            status=Status_code.bad_request)
        if aes.decrypt(data['current_division_id']) == aes.decrypt(data['desired_division_id']):
            return Response(data={'message': "The current division must be different from the desired division",
                                  'status': Status_code.bad_request},
                            status=Status_code.bad_request)
        return Response(data={"message": "Ok.",
                              'status': Status_code.success,
                              "current_div": current_div,
                              "desired_div": desired_div,
                              },
                        status=Status_code.success)
