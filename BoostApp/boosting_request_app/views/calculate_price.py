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
        request.data._mutable = True
        request.data['current_division_id'] = aes.decrypt(request.data['current_division_id'])
        request.data['desired_division_id'] = aes.decrypt(request.data['desired_division_id'])

        response = CalculatePriceValidation.validate_calculate_price(request.data)

        if response.status_code == Status_code.bad_request:
            return response

        current_div = Division.objects.get(id=request.data['current_division_id'])
        desired_div = Division.objects.get(id=request.data['desired_division_id'])

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
