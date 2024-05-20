from rest_framework.exceptions import APIException
from rest_framework import status


class PermissionDenied(APIException):
        status_code = status.HTTP_403_FORBIDDEN
        default_detail = {'message': 'You do not have permission to perform this action.',
                          'status': status.HTTP_403_FORBIDDEN,}
        default_code = 'permission_denied'

class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {'message': 'Authentication credentials were not provided.',
                    'status': status.HTTP_401_UNAUTHORIZED,}
    default_code = 'not_authenticated'


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'
    default_code = 'server_error'

    def __init__(self, detail, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        self.detail = {'message': detail, 'status': self.status_code}
    
    