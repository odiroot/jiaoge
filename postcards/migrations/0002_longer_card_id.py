# Generated by Django 2.2.3 on 2019-08-21 20:00

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [("postcards", "0001_card_contact_models")]

    operations = [
        migrations.AlterField(
            model_name="card",
            name="id",
            field=hashid_field.field.HashidAutoField(
                alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                editable=False,
                min_length=5,
                primary_key=True,
                serialize=False,
                verbose_name="Readable postcard ID",
            ),
        )
    ]
