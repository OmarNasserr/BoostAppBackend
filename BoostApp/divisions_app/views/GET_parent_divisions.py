from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from divisions_app.models import Division
from ..serializers import DivisionSerializer
from ..serializers import ParentDivisionSerializer

aes = AESCipher(settings.SECRET_KEY[:16], 32)


@api_view(['GET', ])
def get_parent_divisions(request):
    if request.method == 'GET':
        data = {}
        try:
            divisions = Division.objects.filter(parent_id=None)
            serializer = ParentDivisionSerializer(divisions, many=True)
            serialized_data = serializer.data

            data['message'] = "Parent divisions was retrieved successfully."
            data['divisions'] = serialized_data
            data['status'] = Status_code.success
            return Response(data, status=Status_code.created)
        except:
            data['message'] = "Couldn't get parent divisions."
            data['status'] = Status_code.bad_request
            return Response(data, status=Status_code.bad_request)
