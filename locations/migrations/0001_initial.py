# Generated by Django 4.2.4 on 2024-01-30 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic', models.CharField(max_length=100)),
                ('female_only', models.BooleanField(default=False)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('created_by', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'ordering': ('clinic',),
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward', models.CharField(max_length=100)),
                ('female_only', models.BooleanField(default=False)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('created_by', models.CharField(blank=True, max_length=30, null=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.clinic')),
            ],
            options={
                'ordering': ('ward',),
            },
        ),
    ]
