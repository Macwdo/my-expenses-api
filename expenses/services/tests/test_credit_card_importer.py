from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from expenses.models import Transaction
from expenses.services.transaction import CreditCardImporterService


class CreditCardImporterServiceTestCase(TestCase):
    
    def setUp(self):
        self.service = CreditCardImporterService()
    
    @patch.object(CreditCardImporterService, "_predict_source_category")
    def test_import_transactions_when_a_non_existant_transaction(self, mock: MagicMock):
        """
        The import should create a new transaction and categorize it.
        
        """
        
        mock.return_value = [
                {
                    "id": "8a6a5e7e-2a4e-4b8d-9b4e-6c7b8e1c8f0c",
                    "category": "Food",
                    "date": "2021-01-01",
                    "title": "Lunch",
                    "amount": 10.0
                }
            ]

        content = b"date,title,amount\n2021-01-01,Lunch,10.0"
        file = SimpleUploadedFile("report.csv", content)

        self.service.import_transactions(file=file, transactions=[])
        
        Transaction.objects.get(
            date="2021-01-01",
            source_name="Lunch",
            value=Decimal("10.00")
        )
    
    @patch.object(CreditCardImporterService, "_predict_source_category")
    def test_import_transactions_when_a_existant_transaction(self, mock: MagicMock):
        """
        The import should update the transaction and categorize it.
        
        """
        
        mock.return_value = [
                {
                    "id": "8a6a5e7e-2a4e-4b8d-9b4e-6c7b8e1c8f0c",
                    "category": "Food",
                    "date": "2021-01-01",
                    "title": "Lunch",
                    "amount": 10.0
                }
            ]

        content = b"date,title,amount\n2021-01-01,Lunch,10.0"
        file = SimpleUploadedFile("report.csv", content)

        transaction = Transaction.objects.create(
            date=date(2021, 1, 1),
            source_name="Lunch",
            value=Decimal("10.00"),
            category=None
        )

        self.service.import_transactions(file=file, transactions=[transaction])
        transaction.refresh_from_db()
        
        self.assertEqual(len(Transaction.objects.all()), 1)
        self.assertEqual(transaction.category, "Food")

    # WIP
    @patch.object(CreditCardImporterService, "_predict_source_category")
    def test_import_transaction_with_existant_report_for_transaction(self, mock: MagicMock):
        mock.return_value = [
                {
                    "id": "8a6a5e7e-2a4e-4b8d-9b4e-6c7b8e1c8f0c",
                    "category": "Food",
                    "date": "2021-01-01",
                    "title": "Lunch",
                    "amount": 10.0
                }
            ]

        content = b"date,title,amount\n2021-01-01,Lunch,10.0"
        file = SimpleUploadedFile("report.csv", content)

        transaction = Transaction.objects.create(
            date=date(2021, 1, 1),
            source_name="Lunch",
            value=Decimal("10.00"),
            category=Transaction.Category.FOOD
        )
        content = b"date,title,amount\n2021-01-01,Lunch,10.0"
        file = SimpleUploadedFile("report.csv", content)
        
        self.service.import_transactions(file=file, transactions=[transaction])
        
        self.assertEqual(len(Transaction.objects.all()), 1)