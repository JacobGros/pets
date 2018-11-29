# Generated by Django 2.1.3 on 2018-11-28 02:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PUPG', '0005_auto_20181127_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='User_id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='age',
        ),
        migrations.RemoveField(
            model_name='person',
            name='password',
        ),
        migrations.RemoveField(
            model_name='person',
            name='username',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='animal_breed',
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pet',
            name='animal_type',
            field=models.CharField(help_text='Enter Animal Type', max_length=20),
        ),
    ]
