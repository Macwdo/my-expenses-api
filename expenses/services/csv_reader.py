import csv


class CsvReaderService:
    def __init__(self):
        ...

    def to_dict(self, file):
        with file.open() as f:
            content = f.read().decode('utf-8')
        
        r = csv.reader(content.splitlines())
        lines = [line for line in r]

        header = lines[0]
        data = lines[1:]

        result = [dict(zip(header, row)) for row in data]
        
        return result
        