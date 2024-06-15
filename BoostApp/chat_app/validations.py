from rest_framework.response import Response
from helper_files.status_code import Status_code
from helper_files.cryptography import AESCipher
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class ChatAppValidations():

    @staticmethod
    def validate_messages_get(kwargs):
        print(kwargs)
        for key in kwargs:
            keys = ['room_id']
            if key in keys:
                try:
                    kwargs[key] = aes.decrypt(str(kwargs[key]))
                    id = int(kwargs[key])
                    print('kw key ',kwargs[key])
                except:
                    return Response(data={'message': "Wrong id format for " + key,
                                          'status': Status_code.bad_request},
                                    status=Status_code.bad_request)

        return Response(data={"message": "Success.",
                              "kwargs": kwargs,
                              'status': Status_code.success,
                              },
                        status=Status_code.success)

