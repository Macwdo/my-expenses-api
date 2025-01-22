import json
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel

from common.decorators import retry
from common.services.openai import OpenAiService
from expenses.models import Transaction
from expenses.services.csv_reader import CsvReaderService


class CreditCardTransactionReportSchema(BaseModel):
    code: str | None
    date: date
    title: str
    amount: float
    category: str | None


class CreditCardTransactionReportSchemaWithId(BaseModel):
    id: UUID
    date: date
    title: str
    amount: float
    category: str | None


class CreditCardImporterService:
    def __init__(self):
        self.csv_reader_service = CsvReaderService()
        self.open_ai_service = OpenAiService()
        self.transaction_service = TransactionService()

    def import_transactions(self, *, file, transactions: list[Transaction]):
        data = self.csv_reader_service.to_dict(file)
        reports = self._serialize(data)
        
        non_categorized_transactions = self._get_non_categorized_transactions(reports, transactions)
        
        batches = self._batch_report(reports, batch_size=100)
        sources = self.transaction_service.get_transaction_sources()

        result_batches = self._get_result_batches(batches, sources)
        categorized_reports = self._get_categorized_reports(result_batches)

        self._update_transactions(categorized_reports, non_categorized_transactions)
        self._create_new_transactions(categorized_reports)

    def _serialize(self, data):
        return [CreditCardTransactionReportSchema(**row, category=None, code=None) for row in data]

    def _get_non_categorized_transactions(self, reports, transactions):
        non_categorized_transactions = []
        for report in reports:
            for transaction in transactions:
                if self._match(transaction, report) and transaction.category is None:
                    non_categorized_transactions.append(transaction)
                    break

        return non_categorized_transactions

    def _match(self, transaction: Transaction, report: CreditCardTransactionReportSchemaWithId | CreditCardTransactionReportSchema):
        return (
            report.date == transaction.date
            and report.title == transaction.source_name
            and Decimal(report.amount) == transaction.value
        )

    def _batch_report(self, reports, batch_size) -> list[list[CreditCardTransactionReportSchema]]:
        return [reports[i:i + batch_size] for i in range(0, len(reports), batch_size)]

    @retry(3)
    def _predict_source_category(self, batch, sources):
        formatted_sources = "\n".join(f"- {source}" for source in sources)
        json_batch = [report.model_dump_json() for report in batch]

        prompt = f"""
        I have a list of credit card transactions that need to be categorized into the following categories:

        {formatted_sources}

        Here are the transactions in JSON format:
        {json_batch}

        Please provide a list of JSON objects with the transaction id and the corresponding category in the following format:
        [
            {{
            "id": "uuid",
            "category": "category"
            }}
        ]

        Ensure the response is valid JSON that can be parsed using json.loads.

        Your response must be just the JSON array of objects.
        """
        response = (
            self
            .open_ai_service
            .prompt(prompt)
            .replace("json\n", "")
            .replace("```", "")
        )
        data = json.loads(response)

        dict_batch = [json.loads(report) for report in json_batch]
        for item in data:
            for batch_item in dict_batch:
                if item["id"] == batch_item["id"]:
                    batch_item["category"] = item["category"]

        return dict_batch

    def _get_result_batches(self, batches, sources):
        batches_with_id = [
            [CreditCardTransactionReportSchemaWithId(id=uuid4(), **report.model_dump()) for report in batch]
            for batch in batches
        ]
        result_batches = [
            self._predict_source_category(batch, sources) for batch in batches_with_id
        ]
        return result_batches

    def _get_categorized_reports(self, result_batches):
        categorized_reports = []
        for batch in result_batches:
            for report in batch:
                categorized_reports.append(CreditCardTransactionReportSchemaWithId(**report))
        return categorized_reports

    def _update_transactions(self, categorized_reports, non_categorized_transactions):
        for report in categorized_reports:
            for transaction in non_categorized_transactions:
                if self._match(transaction, report):
                    transaction.category = report.category
                    transaction.save()
                    categorized_reports.remove(report)
                    break

    def _create_new_transactions(self, categorized_reports):
        bulk_create_transactions = [
            Transaction(
                date=categorized_report.date,
                value=Decimal(categorized_report.amount),
                source_name=categorized_report.title,
                origin=Transaction.Origin.CREDIT_CARD,
                type=Transaction.Type.EXPENSE,
                category=categorized_report.category,
                updated=False,
            )
            for categorized_report in categorized_reports
        ]
        self.transaction_service.bulk_create_transactions(bulk_create_transactions)


class TransactionService:
    def create_transaction(
        self, 
        *, 
        date: date,
        value: Decimal, 
        source_name: str, 
        origin: Transaction.Origin,
        type: Transaction.Type,
        category: Transaction.Category,
        updated: bool,
        imported: bool,
    ):
        transaction = Transaction(
            date=date,
            value=value,
            source_name=source_name,
            origin=origin,
            type=type,
            category=category,
            updated=updated,
            imported=imported,
        )
        transaction.full_clean()
        transaction.save()
        return transaction

    def bulk_create_transactions(self, transactions: list[Transaction]):
        for transaction in transactions:
            transaction.full_clean()
        Transaction.objects.bulk_create(transactions)

    def get_transaction_sources(self):
        return Transaction.Category.values
