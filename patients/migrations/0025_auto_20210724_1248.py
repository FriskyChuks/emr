# Generated by Django 3.1.2 on 2021-07-24 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0024_auto_20210724_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='l_g_a',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='patients.lga'),
            preserve_default=False,
        ),
    ]