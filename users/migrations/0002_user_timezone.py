# Generated by Django 2.2.7 on 2020-03-14 19:51

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_user_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='Europe/Paris'),
        ),
    ]
