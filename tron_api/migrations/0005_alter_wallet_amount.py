# Generated by Django 4.0.6 on 2022-07-07 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tron_api', '0004_rename_username_wallet_email_address_wallet_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.CharField(max_length=100),
        ),
    ]