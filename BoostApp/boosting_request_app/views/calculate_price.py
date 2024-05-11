from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..validations import CalculatePriceValidation
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from divisions_app.models import Division

aes = AESCipher(settings.SECRET_KEY[:16], 32)


@api_view(['Post',])
def calculate_price(request):
    if request.method == 'POST':

        data = {}
        response = CalculatePriceValidation.validate_calculate_price(request.data)
        current_division_id = aes.decrypt(request.data['current_division_id'])
        desired_division_id = aes.decrypt(request.data['desired_division_id'])

        if response.status_code == Status_code.bad_request:
            return response

        current_div = Division.objects.get(id=aes.decrypt(request.data['current_division_id']))
        desired_div = Division.objects.get(id=aes.decrypt(request.data['desired_division_id']))




        data['message'] = "Price was calculated successfully."
        data['price'] = "50$"
        data['status'] = Status_code.success


        return Response(data, status=Status_code.created)
