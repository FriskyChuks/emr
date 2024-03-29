# Generated by Django 3.1.2 on 2021-05-08 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labs', '0009_labrequest_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=225)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lab_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='labs.labrequest')),
            ],
        ),
    ]
