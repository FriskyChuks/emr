# Generated by Django 3.1.2 on 2021-04-12 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadiologyService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('radiology_service', models.CharField(max_length=150)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=65)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RaiseRadiologyService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
                ('unit', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('encounter_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visits.patientencounter')),
                ('radiology_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radiology.radiologyservice')),
            ],
        ),
        migrations.CreateModel(
            name='RadiologyServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=150)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='radiologyservice',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radiology.radiologyservicetype'),
        ),
    ]