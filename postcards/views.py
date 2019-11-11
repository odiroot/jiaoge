from datetime import datetime

from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import DetailView, FormView
from django.views.generic.edit import FormMixin

from .forms import CardClaimForm, CodeClaimForm
from .models import Card


class CardClaimView(FormMixin, DetailView):
    """
    Legacy view. Claiming with code inside the URL.
    """
    # Don't allow claiming previously received cards.
    queryset = Card.objects.filter(received_at__isnull=True)
    form_class = CardClaimForm

    def get_success_url(self):
        return reverse('claim_success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object.received_at = datetime.utcnow()
        form.save()
        return super().form_valid(form)


class CodeClaimView(FormView):
    """
    New view. Claiming with an explicit code.
    """
    form_class = CodeClaimForm
    template_name = 'postcards/code_claim.html'

    def get_success_url(self):
        return reverse('claim_success')

    def form_valid(self, form):
        id_ = form.cleaned_data['code'].upper()

        card = get_object_or_404(
            Card.objects.filter(received_at__isnull=True), id=id_)

        card.received_at = datetime.utcnow()
        card.claim_comment = form.cleaned_data['claim_comment']
        card.save()

        return super().form_valid(form)


def claim_success(request):
    return render(request, 'postcards/claimed.html')
