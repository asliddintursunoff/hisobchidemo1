# Generated by Django 5.1.6 on 2025-03-01 22:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_company_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 16, 22, 53, 13, 368432, tzinfo=datetime.timezone.utc)),
        ),
    ]
