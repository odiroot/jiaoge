from datetime import datetime

from django.shortcuts import render, reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from .forms import CardClaimForm
from .models import Card


class CardClaimView(FormMixin, DetailView):
    # Don't allow claiming previously received cards.
    queryset = Card.objects.filter(received_at__isnull=True)
    form_class = CardClaimForm

    def get_success_url(self):
        # TODO: Add this view!
        return reverse('claim_success')

    def get_form_kwargs(self):
        kwargs = super(CardClaimView, self).get_form_kwargs()
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
        return super(CardClaimView, self).form_valid(form)


def claim_success(request):
    return render(request, 'postcards/claimed.html')
