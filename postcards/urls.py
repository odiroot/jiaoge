from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import CardViewSet, CardFaceView, ContactViewSet
from .views import (
    CardClaimView, CardListView, claim_success, CodeClaimView, PregenerateView)


doc_paths = [
    # Receiver-facing: claiming.
    path(r'claim/<pk>/', CardClaimView.as_view(), name='claim_direct'),
    path(r'code-claim/', CodeClaimView.as_view()),
    path(r'claimed/', claim_success, name='claim_success'),

    # Creator-facing: create/manage.
    path(r'pregenerate/', PregenerateView.as_view(), name='pregenerate'),
    path(r'list/', CardListView.as_view(), name='list_cards'),
]


router = DefaultRouter()
router.register(r'cards', CardViewSet)
router.register(r'contacts', ContactViewSet)

api_paths = [
    path(r'cards/<pk>/face', CardFaceView.as_view(), name='upload_face'),
]
