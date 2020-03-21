from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, reverse, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import FormMixin

from .forms import CardClaimForm, CodeClaimForm, PregenerateForm
from .models import Card


class CardClaimView(FormMixin, DetailView):
    """
    Legacy view. Claiming with code inside the URL.
    """

    # Don't allow claiming previously received cards.
    queryset = Card.objects.filter(received_at__isnull=True)
    form_class = CardClaimForm

    def get_success_url(self):
        return reverse("claim_success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object

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
    template_name = "postcards/code_claim.html"

    def get_success_url(self):
        return reverse("claim_success")

    def form_valid(self, form):
        id_ = form.cleaned_data["code"].upper()

        card = get_object_or_404(
            Card.objects.filter(received_at__isnull=True), id=id_
        )

        card.received_at = datetime.utcnow()
        card.claim_comment = form.cleaned_data["claim_comment"]
        card.save()

        return super().form_valid(form)


def claim_success(request):
    return render(request, "postcards/claimed.html")


@method_decorator(staff_member_required, name="dispatch")
class PregenerateView(FormView):
    form_class = PregenerateForm
    template_name = "postcards/pregenerate.html"

    def form_valid(self, form):
        to_save = []

        for contact in form.cleaned_data["to"]:
            card = Card(
                from_country=form.cleaned_data["from_country"],
                from_city=form.cleaned_data["from_city"],
                to=contact,
            )
            to_save.append(card)

        Card.objects.bulk_create(to_save)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("list_cards") + "?mode=unsent"


LIST_MODES = [
    ("all", "All postcards"),
    ("unsent", "Unsent only"),
    ("unclaimed", "Sent and not claimed"),
    ("received", "Claimed only"),
]


@method_decorator(staff_member_required, name="dispatch")
class CardListView(ListView):
    def setup(self, request, *args, **kwargs):
        # Make the date display nicer.
        timezone.activate(request.user.timezone)
        return super().setup(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        qs = Card.objects
        mode = self.request.GET.get("mode", None)

        if mode == "unsent":
            qs = qs.filter(sent_at__isnull=True)
        elif mode == "unclaimed":
            qs = qs.filter(sent_at__isnull=False, received_at__isnull=True)
        elif mode == "received":
            qs = qs.filter(sent_at__isnull=False, received_at__isnull=False)
        else:
            pass  # No filters by default == all.

        return qs.order_by("-created_at")
