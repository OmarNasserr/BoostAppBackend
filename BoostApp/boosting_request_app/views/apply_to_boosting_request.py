from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..validations import CalculatePriceValidation, ApplyToBoostingRequestValidation
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from datetime import datetime

aes = AESCipher(settings.SECRET_KEY[:16], 32)


@api_view(['Post', ])
def apply_to_boosting_request(request):
    if request.method == 'POST':
        response = ApplyToBoostingRequestValidation.validate_apply_to_boosting_request(request.data)

        if response.status_code == Status_code.bad_request:
            return response

        data = {}

        boosting_request = response.data['boosting_request']
        booster = response.data['booster']

        current_time = datetime.now().strftime("%d %b, %Y - %Ih%Mm%S %p")
        boosting_request.booster_id = booster
        boosting_request.is_applied = True
        boosting_request.updated_at = datetime.now()
        boosting_request.applied_at = current_time

        boosting_request.save()

        data['message'] = (f"Booster {boosting_request.booster_id.first_name} "
                           f"has successfully applied to the Boosting Request posted by player "
                           f"{boosting_request.player_id.first_name}.")
        data['player_id'] = f"{aes.encrypt(str(boosting_request.player_id.id))}"
        data['booster_id'] = f"{aes.encrypt(str(boosting_request.booster_id.id))}"
        data['payment_amount'] = boosting_request.payment_amount
        data['current_division_id'] = f"{aes.encrypt(str(boosting_request.current_division_id.id))}"
        data['desired_division_id'] = f"{aes.encrypt(str(boosting_request.desired_division_id.id))}"
        data['applied_at'] = f"{boosting_request.applied_at}"
        data['status'] = Status_code.success

        return Response(data, status=Status_code.created)
