# Generated by Django 4.2.2 on 2023-06-26 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
