# Generated by Django 5.1.6 on 2025-02-25 09:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_company_expiry_date_alter_user_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 12, 9, 35, 57, 440874, tzinfo=datetime.timezone.utc)),
        ),
    ]
