# Generated by Django 3.1.2 on 2021-04-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0012_auto_20210429_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]