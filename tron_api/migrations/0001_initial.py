# Generated by Django 4.0.6 on 2022-07-05 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_address', models.CharField(max_length=500)),
                ('private_key', models.CharField(max_length=500)),
                ('amount', models.DecimalField(decimal_places=20, max_digits=20)),
            ],
        ),
    ]