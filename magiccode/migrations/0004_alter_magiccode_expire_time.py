# Generated by Django 5.0 on 2023-12-26 09:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magiccode', '0003_alter_magiccode_code_alter_magiccode_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magiccode',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 26, 9, 49, 24, 397161, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]