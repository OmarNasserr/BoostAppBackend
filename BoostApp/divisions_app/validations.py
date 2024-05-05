from rest_framework.response import Response
from rest_framework import status
import re
from helper_files.status_code import Status_code
from django.contrib.auth.models import User


class DivisionAppValidations():

    def validate_division_create(data, valid, err):

        if valid:
            if len(data['name']) < 2:
                return Response(data={'message': "Division's name can't be less than two characters",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if len(data['name']) > 30:
                return Response(data={'message': "Division's name can't be more than 30 characters",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            else:
                return Response(data={"message": "Division was added successfully.",
                                      'status': Status_code.created},
                                status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)

    def validate_division_update(data, valid, err):
        if valid:
            if len(data['name']) < 2:
                return Response(data={'message': "Division's name can't be less than two characters",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if len(data['name']) > 30:
                return Response(data={'message': "Division's name can't be more than 30 characters",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            else:
                return Response(data={"message": "Division was updated successfully.",
                                      'status': Status_code.created},
                                status=Status_code.created)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)
