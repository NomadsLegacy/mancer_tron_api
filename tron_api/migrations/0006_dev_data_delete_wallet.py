# Generated by Django 4.0.6 on 2022-07-20 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tron_api', '0005_remove_wallet_private_key_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='dev_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WALLET_ADDRESS', models.CharField(max_length=100)),
                ('PRIVATE_KEY', models.CharField(max_length=200)),
                ('TitleId', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
    ]
