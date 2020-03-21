from hashid_field.rest import HashidSerializerCharField
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import Card, Contact


class CardSerializer(ModelSerializer):
    id = HashidSerializerCharField(
        source_field="postcards.Card.id", read_only=True
    )
    to = SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Card
        fields = "__all__"


class CardFaceSerializer(ModelSerializer):
    id = HashidSerializerCharField(
        source_field="postcards.Card.id", read_only=True
    )

    class Meta:
        model = Card
        fields = ("id", "face")


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
