# Generated by Django 3.1.2 on 2021-04-29 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0010_delete_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/'),
        ),
        migrations.CreateModel(
            name='PatientImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='media/images/')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
            ],
        ),
    ]
