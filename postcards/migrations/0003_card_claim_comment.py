# Generated by Django 2.2.3 on 2019-08-21 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postcards', '0002_longer_card_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='claim_comment',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
