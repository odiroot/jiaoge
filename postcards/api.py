from datetime import datetime

from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from rest_framework.viewsets import ModelViewSet

from .models import Card, Contact
from .serializers import CardSerializer, CardFaceSerializer, ContactSerializer


class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    @action(methods=['post'], detail=True, url_path='send')
    def send_out(self, requset, pk=None):
        card = self.get_object()

        # No point dispatching the card again.
        if card.sent_at is not None:
            return Response(
                'Card already sent', status=HTTP_409_CONFLICT)
        # Probably a mistake.
        if not card.to:
            return Response(
                'No card receiver specified', status=HTTP_400_BAD_REQUEST)

        card.sent_at = datetime.utcnow()
        card.save()

        return Response(status=200)


class CardFaceView(UpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardFaceSerializer
    parser_class = (FileUploadParser,)


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
