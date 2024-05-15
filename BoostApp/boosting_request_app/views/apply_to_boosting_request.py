from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..validations import CalculatePriceValidation, ApplyToBoostingRequestValidation
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from divisions_app.models import Division

aes = AESCipher(settings.SECRET_KEY[:16], 32)


@api_view(['Post',])
def apply_to_boosting_request(request):
    if request.method == 'POST':

        response = ApplyToBoostingRequestValidation.validate_apply_to_boosting_request(request.data)

        if response.status_code == Status_code.bad_request:
            return response

        data = {}
        request.data._mutable = True
        boosting_request = response.data['boosting_request']
        booster = response.data['booster']

        boosting_request.update({'booster_id': response.data['']})

        data['message'] = "Price was calculated successfully."
        # data['price'] = f"{price}$"
        data['status'] = Status_code.success


        return Response(data, status=Status_code.created)
