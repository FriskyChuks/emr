# Generated by Django 3.1.2 on 2021-04-07 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(default='pending', max_length=10),
        ),
    ]
