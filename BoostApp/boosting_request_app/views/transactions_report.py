from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from ..models import BoostingRequest
from django.db.models import Sum
from datetime import datetime

aes = AESCipher(settings.SECRET_KEY[:16], 32)

from rest_framework import serializers


class TransactionReportSerializer(serializers.Serializer):
    total_requests = serializers.IntegerField()
    not_applied_to_requests = serializers.IntegerField()
    applied_to_not_completed_requests = serializers.IntegerField()
    completed_requests = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


@api_view(['GET'])
def transactions_report(request):
    data = {}
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    filters = {}
    try:
        if start_date:
            filters['created_at__gte'] = datetime.strptime(start_date, '%d-%m-%Y')
        if end_date:
            filters['created_at__lte'] = datetime.strptime(end_date, '%d-%m-%Y')
    except:
        data['message'] = 'Invalid date format, expected format %d-%m-%Y'
        data['status'] = Status_code.bad_request
        return Response(data, status=Status_code.bad_request)

    total_requests = BoostingRequest.objects.filter(**filters).count()
    not_applied_requests = BoostingRequest.objects.filter(is_applied=False, **filters).count()
    applied_not_completed_requests = BoostingRequest.objects.filter(is_applied=True, is_completed=False,
                                                                    **filters).count()
    completed_requests = BoostingRequest.objects.filter(is_completed=True, **filters).count()
    total_amount = BoostingRequest.objects.filter(**filters).aggregate(total=Sum('payment_amount'))['total'] or 0

    report_data = {
        'total_requests': total_requests,
        'not_applied_to_requests': not_applied_requests,
        'applied_to_not_completed_requests': applied_not_completed_requests,
        'completed_requests': completed_requests,
        'total_amount': total_amount,
    }

    serializer = TransactionReportSerializer(report_data)
    data['message'] = 'Transactions report retrieved successfully.'
    data['report'] = serializer.data
    data['status'] = Status_code.success
    return Response(data, status=Status_code.success)
