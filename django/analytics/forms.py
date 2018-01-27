from django import forms
from .models import *
from dal import autocomplete

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('Logo',)
        fields=('ClientName',)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('LocationName',)

class KioskForm(forms.ModelForm):
    class Meta:
        model = Kiosk
        fields = '__all__'
        widgets = {
        'Client':autocomplete.ModelSelect2(url='analytics:client-autocomplete'),
        'Location':autocomplete.ModelSelect2(url='analytics:location-autocomplete')
        }


class PortForm(forms.ModelForm):
    class Meta:
        model = Port
        fields = '__all__'
        widgets = {
        'Kiosk':autocomplete.ModelSelect2(url='analytics:kiosk-autocomplete'),
        }
