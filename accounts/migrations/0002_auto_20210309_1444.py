# Generated by Django 3.1.2 on 2021-03-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GuestEmail',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='full_name',
            new_name='other_names',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='chuks', max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='chuks', max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=1, max_length=225, unique=True),
            preserve_default=False,
        ),
    ]
