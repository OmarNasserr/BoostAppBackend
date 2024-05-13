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

        response = CalculatePriceValidation.validate_calculate_price(request.data)

        if response.status_code == Status_code.bad_request:
            response.data['price']='0$'
            return response

        current_div = response.data['current_div']
        desired_div = response.data['desired_div']

        data = {}

        price = 0
        while current_div.id != desired_div.id:
            price += desired_div.price
            if desired_div.previous_division:
                desired_div = Division.objects.get(id=desired_div.previous_division.id)
            else:
                break


        data['message'] = "Price was calculated successfully."
        data['price'] = f"{price}$"
        data['status'] = Status_code.success


        return Response(data, status=Status_code.created)
