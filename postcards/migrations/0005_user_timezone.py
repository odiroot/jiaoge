# Generated by Django 2.2.7 on 2020-03-14 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postcards', '0004_contact_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
