from rest_framework.response import Response
from rest_framework import status
import re
from helper_files.status_code import Status_code
from django.contrib.auth.models import User


class BoostingRequestAppValidations():

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
