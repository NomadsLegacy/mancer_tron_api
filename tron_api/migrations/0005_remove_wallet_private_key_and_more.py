# Generated by Django 4.0.6 on 2022-07-20 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tron_api', '0004_rename_username_wallet_email_address_wallet_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='private_key',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='wallet_address',
        ),
    ]