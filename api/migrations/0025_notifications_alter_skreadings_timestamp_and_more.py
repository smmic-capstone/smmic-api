# Generated by Django 5.0.2 on 2024-10-02 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_alter_skreadings_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('type', models.TextField()),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='skreadings',
            name='timestamp',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='smsensorreadings',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
