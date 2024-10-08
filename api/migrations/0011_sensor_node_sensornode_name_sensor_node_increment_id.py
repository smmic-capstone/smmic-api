# Generated by Django 5.0.2 on 2024-08-09 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_sink_node_autoname_increment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor_node',
            name='SensorNode_Name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sensor_node',
            name='increment_id',
            field=models.IntegerField(default=1, editable=False, unique=True),
            preserve_default=False,
        ),
    ]
