# Generated by Django 3.1.2 on 2021-07-06 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0009_user_lab_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='lab_unit',
        ),
        migrations.CreateModel(
            name='SubGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_group', models.CharField(max_length=50)),
                ('parent_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]