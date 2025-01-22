# Generated by Django 5.1.5 on 2025-01-22 05:40

import common.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, default=common.models.generate_code, editable=False, max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=common.models.upload_path)),
                ('source', models.CharField(choices=[('NOT_DEFINED', 'Not Defined'), ('ACCOUNT_IMAGE', 'Account Image')], default='NOT_DEFINED', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
