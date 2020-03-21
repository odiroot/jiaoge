from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Card, Contact


class CardClaimForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ("claim_comment",)

    claim_comment = forms.CharField(
        label="Comment", max_length=160, required=False, widget=forms.Textarea
    )


class CodeClaimForm(forms.Form):
    code = forms.CharField(
        label="Code", max_length=8, min_length=5, required=True
    )
    claim_comment = forms.CharField(
        label="Comment", max_length=160, required=False, widget=forms.Textarea
    )


class PregenerateForm(forms.Form):
    from_country = CountryField(blank_label="-- Select country --").formfield(
        required=True, widget=CountrySelectWidget()
    )
    from_city = forms.CharField(required=False, max_length=32)
    to = forms.ModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={"size": "5", "class": "multi"}),
    )
