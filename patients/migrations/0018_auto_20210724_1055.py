# Generated by Django 3.1.2 on 2021-07-24 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0017_auto_20210429_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('lagos', 'Lagos'), ('nasarawa', 'Nasarawa'), ('abia', 'Abia'), ('adamawa', 'Adamawa'), ('anambra', 'Anambra'), ('akwa-ibom', 'Akwa-Ibom'), ('delta', 'Delta'), ('edo', 'Edo'), ('enugu', 'Enugu'), ('jigawa', 'Jigawa'), ('ondo', 'Ondo'), ('imo', 'Imo'), ('bauchi', 'Bauchi'), ('plateau', 'Plateau'), ('ogun', 'Ogun'), ('kaduna', 'Kaduna'), ('katsina', 'Katsina'), ('sokoto', 'Sokoto'), ('osun', 'Osun'), ('benue', 'Benue'), ('kogi', 'Kogi'), ('fct(Abuja)', 'FCT(Abuja)'), ('ebonyi', 'Ebonyi'), ('cross-rivers', 'Cross-Rivers')], max_length=20, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone_1',
            field=models.CharField(max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='state',
            field=models.CharField(choices=[('lagos', 'Lagos'), ('nasarawa', 'Nasarawa'), ('abia', 'Abia'), ('adamawa', 'Adamawa'), ('anambra', 'Anambra'), ('akwa-ibom', 'Akwa-Ibom'), ('delta', 'Delta'), ('edo', 'Edo'), ('enugu', 'Enugu'), ('jigawa', 'Jigawa'), ('ondo', 'Ondo'), ('imo', 'Imo'), ('bauchi', 'Bauchi'), ('plateau', 'Plateau'), ('ogun', 'Ogun'), ('kaduna', 'Kaduna'), ('katsina', 'Katsina'), ('sokoto', 'Sokoto'), ('osun', 'Osun'), ('benue', 'Benue'), ('kogi', 'Kogi'), ('fct(Abuja)', 'FCT(Abuja)'), ('ebonyi', 'Ebonyi'), ('cross-rivers', 'Cross-Rivers')], max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='patient',
            unique_together={('first_name', 'last_name', 'date_of_birth')},
        ),
        migrations.CreateModel(
            name='LGA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lga', models.CharField(max_length=50)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.state')),
            ],
        ),
    ]
