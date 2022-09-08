from django import forms


class ClientRequest(forms.Form):
    price = forms.IntegerField()
    start_sum = forms.IntegerField()
    for_year = forms.IntegerField()



