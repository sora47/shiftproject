from django import forms


class DutyChoiceForm(forms.Form):
    choice = forms.ChoiceField(widget=forms.Select)
    choice2 = forms.ChoiceField(widget=forms.Select)
