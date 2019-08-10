from string import ascii_uppercase, digits

from django.db import models
from django_countries.fields import CountryField
from hashid_field import HashidAutoField

from common.models import UUIDMixin


def face_upload_path(instance, filename):
    return f'postcards/{instance.id}-{filename}'


class Contact(UUIDMixin, models.Model):
    name = models.CharField(max_length=64)
    country = CountryField()
    city = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name} in {self.city}'


class Card(models.Model):
    id = HashidAutoField(
        primary_key=True, editable=False,
        min_length=3, alphabet=ascii_uppercase + digits,
        verbose_name='Readable postcard ID')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    face = models.ImageField(
        upload_to=face_upload_path, verbose_name='Postcard face design',
        blank=True)
    from_country = CountryField()
    from_city = models.CharField(max_length=32)
    to = models.ForeignKey(
        Contact, null=True, on_delete=models.SET_NULL, related_name='cards',
        blank=True, verbose_name='Receiver')
    sent_at = models.DateTimeField(null=True)
    received_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        receiver = self.to and self.to.name or 'N/A'

        return (f'Postcard from: {self.from_country}/{self.from_city} '
                f'to {receiver}')
