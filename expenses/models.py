from django.db import models

from common.models import BaseModel, MoneyField

# We have Transactions

# There are Transactions from credit cards
# There are Transactions from PIX

# There are Recurring Transactions
## Those Recurring Transactions was defined to be monthly 
## Those Recurring Transactions can be linked to a Transaction
### We wanna link to a Transaction to know how much we spent in a month

# There are Sources
## Those Sources are where the Transactions came from
## Those Sources have a category
### We wanna know how much we spent in a month by category
### We wanna run an ai to categorize and try to identify the source
### We wanna try match with the current categories



    
class Transaction(BaseModel):
    class Type(models.TextChoices):
        EXPENSE = "EXPENSE", "Expense"
        INCOME = "INCOME", "Income"
        
    class Origin(models.TextChoices):
        CREDIT_CARD = "CREDIT_CARD", "Credit Card"
        PIX = "PIX", "Pix"
    
    class Category(models.TextChoices):
        FOOD = "Food", "Food"
        TRANSPORTATION = "Transportation", "Transportation"
        EDUCATION = "Education", "Education"
        HEALTH = "Health", "Health"
        ENTERTAINMENT = "Entertainment", "Entertainment"
        SHOPPING = "Shopping", "Shopping"
        TRANSFER = "Transfer", "Transfer"
        BILL = "Bill", "Bill"
        SUBSCRIPTION = "Subscription", "Subscription"
        OTHER = "Other", "Other"
        NOT_IDENTIFIED = "Not Identified", "Not Identified"
    
    
    type = models.CharField(max_length=20, choices=Type.choices)
    category = models.CharField(
        max_length=255,
        choices=Category.choices,
        default=Category.NOT_IDENTIFIED,
        null=True,
    )
    origin = models.CharField(max_length=20, choices=Origin.choices)

    updated = models.BooleanField(default=False)
    imported = models.BooleanField(default=False)
    
    value = MoneyField(decimal_places=2, max_digits=10)
    date = models.DateField()

    source_name = models.CharField(max_length=255)
    
class CreditTransaction(BaseModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    
class PixTransaction(BaseModel):
    class PixTransactionType(models.TextChoices):
        SENT = "SENT", "Sent"
        RECEIVED = "RECEIVED", "Received"
        APPLICATION = "APPLICATION", "Application"
        APPLICATION_WITHDRAW = "APPLICATION_WITHDRAW", "Application Withdraw"
        DEBIT_PAYMENT = "DEBIT_PAYMENT", "Debit Payment"
        CREDIT_PAYMENT = "CREDIT_PAYMENT", "Credit Payment"
        NOT_IDENTIFIED = "NOT_IDENTIFIED", "Not Identified"
        
    unique_code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=PixTransactionType.choices, default=PixTransactionType.NOT_IDENTIFIED)

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    
class RecurringTransactionCategory(BaseModel): 
    name = models.CharField(max_length=255)
    
class RecurringTransaction(BaseModel): 
    name = models.CharField(max_length=255)
    category = models.ForeignKey(RecurringTransactionCategory, on_delete=models.CASCADE)
    
class RecurringTransactionItem(BaseModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    monthly_transaction = models.ForeignKey(RecurringTransaction, on_delete=models.CASCADE)