from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from expenses.services.csv_reader import CsvReaderService


class CsvReaderServiceTest(TestCase):
    def setUp(self):
        self.service = CsvReaderService()

    def test_read_csv_file(self):
        
        content = b"date,description,value\n"
        content += b"2021-01-01,description,100.00\n"
        content += b"2021-01-02,description,200.00\n"
        
        file = SimpleUploadedFile(".tmp.csv", content)
        
        result = self.service.to_dict(file)
        
        self.assertDictEqual(
            result[0],
            {
                "date": "2021-01-01",
                "description": "description",
                "value": "100.00",
            }
        )