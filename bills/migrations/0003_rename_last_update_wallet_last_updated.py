# Generated by Django 4.0.6 on 2022-12-20 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_wallet_last_update'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='last_update',
            new_name='last_updated',
        ),
    ]
