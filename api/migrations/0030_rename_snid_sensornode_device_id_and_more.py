# Generated by Django 5.1.1 on 2024-10-22 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_sensornodealerts_sinknodealerts_delete_notifications_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensornode',
            old_name='SNID',
            new_name='device_id',
        ),
        migrations.RenameField(
            model_name='sensornode',
            old_name='SensorNode_Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='sensornode',
            old_name='SinkNode',
            new_name='sink_node',
        ),
        migrations.RenameField(
            model_name='sensornodealerts',
            old_name='type',
            new_name='alert_code',
        ),
        migrations.RenameField(
            model_name='sensornodealerts',
            old_name='deviceId',
            new_name='device_id',
        ),
        migrations.RenameField(
            model_name='sinknode',
            old_name='SKID',
            new_name='device_id',
        ),
        migrations.RenameField(
            model_name='sinknode',
            old_name='SK_Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='sinknodealerts',
            old_name='deviceID',
            new_name='device_id',
        ),
        migrations.RenameField(
            model_name='skreadings',
            old_name='Sink_Node',
            new_name='device_id',
        ),
        migrations.RenameField(
            model_name='smsensorreadings',
            old_name='Sensor_Node',
            new_name='device_id',
        ),
    ]