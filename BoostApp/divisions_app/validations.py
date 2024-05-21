from rest_framework.response import Response
from helper_files.status_code import Status_code
from helper_files.cryptography import AESCipher
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class DivisionAppValidations():

    @staticmethod
    def validate_division_get(kwargs):

        for key in kwargs:
            keys = ['game_id', 'parent_id']
            if key in keys:
                try:
                    kwargs[key] = aes.decrypt(str(kwargs[key]))
                except:
                    return Response(data={'message': "Wrong id format for " + key,
                                          'status': Status_code.bad_request},
                                    status=Status_code.bad_request)

        return Response(data={"message": "Success.",
                              "kwargs": kwargs,
                              'status': Status_code.success,
                              },
                        status=Status_code.success)

    @staticmethod
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

    @staticmethod
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
