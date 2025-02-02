# Generated by Django 5.1.5 on 2025-01-22 05:40

import common.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringTransactionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, default=common.models.generate_code, editable=False, max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, default=common.models.generate_code, editable=False, max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('EXPENSE', 'Expense'), ('INCOME', 'Income')], max_length=20)),
                ('category', models.CharField(choices=[('Food', 'Food'), ('Transportation', 'Transportation'), ('Education', 'Education'), ('Health', 'Health'), ('Entertainment', 'Entertainment'), ('Shopping', 'Shopping'), ('Transfer', 'Transfer'), ('Bill', 'Bill'), ('Subscription', 'Subscription'), ('Other', 'Other'), ('Not Identified', 'Not Identified')], default='Not Identified', max_length=255)),
                ('origin', models.CharField(choices=[('CREDIT_CARD', 'Credit Card'), ('PIX', 'Pix')], max_length=20)),
                ('updated', models.BooleanField(default=False)),
                ('imported', models.BooleanField(default=False)),
                ('value', common.models.MoneyField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('source_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecurringTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, default=common.models.generate_code, editable=False, max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.recurringtransactioncategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecurringTransactionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, default=common.models.generate_code, editable=False, max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('monthly_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.recurringtransaction')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PixTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, default=common.models.generate_code, editable=False, max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unique_code', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('SENT', 'Sent'), ('RECEIVED', 'Received'), ('APPLICATION', 'Application'), ('APPLICATION_WITHDRAW', 'Application Withdraw'), ('DEBIT_PAYMENT', 'Debit Payment'), ('CREDIT_PAYMENT', 'Credit Payment'), ('NOT_IDENTIFIED', 'Not Identified')], default='NOT_IDENTIFIED', max_length=20)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CreditTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, default=common.models.generate_code, editable=False, max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
