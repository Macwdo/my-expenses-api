
from h11 import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from api.views.base import BaseModelViewSet
from expenses.models import Transaction
from expenses.services.transaction import CreditCardImporter, PixImporter


class TransactionModelSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
    

class TransactionModelViewSet(BaseModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer
    
    
    @action(methods=["POST"], detail=False, url_path="import-credit-card")
    def import_credit_card(self, request):
        file = request.FILES["report"]
        CreditCardImporter().import_transactions(file=file)
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=["POST"], detail=False, url_path="import-pix")
    def import_pix(self, request):
        file = request.FILES["report"]
        PixImporter().import_transactions(file=file)
        return Response(status=status.HTTP_200_OK)