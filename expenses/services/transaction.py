from datetime import date
from pydantic import BaseModel
from expenses.services.csv_reader import CsvReaderService

class CreditCardTransactionReportSchema(BaseModel):
    date: date
    title: str
    amount: float


class CreditCardImporter:
    def __init__(self):
        self.transaction_service = TransactionService()
        self.csv_reader_service = CsvReaderService()
        
    def serialize(self, data):
        return [CreditCardTransactionReportSchema(**row) for row in data]        

    def import_transactions(self, file):
        data = self.csv_reader_service.to_dict(file)
        reports = self.serialize(data)
        
        
        
        return 
    
    def predict_category(self, report: ):
        return "Others"

