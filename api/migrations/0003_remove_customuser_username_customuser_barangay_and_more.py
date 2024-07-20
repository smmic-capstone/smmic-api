# Generated by Django 5.0.2 on 2024-07-18 05:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_customuser_zip_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='barangay',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='city',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='province',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='zone',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
