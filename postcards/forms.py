from django import forms

from .models import Card


class CardClaimForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('claim_comment',)

    claim_comment = forms.CharField(
        label='Comment', max_length=160, required=False, widget=forms.Textarea)


class CodeClaimForm(forms.Form):
    code = forms.CharField(
        label='Code', max_length=8, min_length=5, required=True)
    claim_comment = forms.CharField(
        label='Comment', max_length=160, required=False, widget=forms.Textarea)
