# Generated by Django 4.2.2 on 2023-06-25 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_room_days_room_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='days',
        ),
        migrations.RemoveField(
            model_name='room',
            name='location',
        ),
    ]