# Generated by Django 4.1.6 on 2023-02-11 19:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stux_auth', '0002_customuser_email_verified_onetimepassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='onetimepassword',
            name='time',
            field=models.TimeField(default=datetime.time(19, 41, 54, 865069)),
        ),
    ]