# Generated by Django 5.0.2 on 2024-11-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_alter_sensornode_latitude_alter_sensornode_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensornode',
            name='registered',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='sinknode',
            name='registered',
            field=models.BooleanField(default=0),
        ),
    ]
