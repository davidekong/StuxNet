# Generated by Django 4.1.7 on 2023-02-23 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stux_auth', '0004_alter_onetimepassword_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default='xxxxxxxxxxxxxxx', max_length=20),
        ),
    ]