# Generated by Django 5.0.2 on 2024-11-03 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_sensornodealerts_readings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensornodealerts',
            name='readings',
            field=models.JSONField(default=dict),
        ),
    ]