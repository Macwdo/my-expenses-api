from datetime import date

from expenses.models import Transaction


def list_transactions_in_range(start_date: date, end_date: date):
    return list(Transaction.objects.filter(date__range=[start_date, end_date]))
