from datetime import date
from string import ascii_uppercase, digits

from django.db import models
from django_countries.fields import CountryField
from hashid_field import HashidAutoField

from common.models import UUIDMixin
from jiaoge.storage import S3MediaStorage


def face_upload_path(instance, filename):
    today = date.today().isoformat()
    # Date _ City of origin _ Upload filename.
    return f'postcards/{today}_{instance.from_city}_{filename}'


class Contact(UUIDMixin, models.Model):
    SUPPORTED_LANGUAGES = [
        ('en', 'English'),
        ('de', 'German'),
        ('pl', 'Polish'),
    ]
    DEFAULT_LANGUAGE = 'en'

    name = models.CharField(max_length=64)
    country = CountryField()
    city = models.CharField(max_length=32)
    language = models.CharField(
        max_length=2, null=True, blank=True,
        choices=SUPPORTED_LANGUAGES, default=DEFAULT_LANGUAGE)

    def __str__(self):
        return f'{self.name} in {self.city}, {self.country}'


class Card(models.Model):
    id = HashidAutoField(
        primary_key=True, editable=False,
        min_length=5, alphabet=ascii_uppercase + digits,
        verbose_name='Readable postcard ID')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    face = models.ImageField(
        upload_to=face_upload_path, storage=S3MediaStorage(),
        verbose_name='Postcard face design', blank=True)
    from_country = CountryField()
    from_city = models.CharField(max_length=32)
    to = models.ForeignKey(
        Contact, null=True, on_delete=models.SET_NULL, related_name='cards',
        blank=True, verbose_name='Receiver')
    sent_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    claim_comment = models.CharField(max_length=100, null=False, blank=True)

    def __str__(self):
        receiver = self.to and self.to.name or 'N/A'

        return (f'Postcard from: {self.from_country}/{self.from_city} '
                f'to {receiver}')

    @property
    def is_sent(self):
        return self.sent_at is not None

    @property
    def is_claimed(self):
        return self.received_at is not None
