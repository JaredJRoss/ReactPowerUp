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
    ID = forms.IntegerField(required=False)
    class Meta:
        model = Kiosk
        fields = '__all__'
        exclude = ('CreatedOn',)
        widgets = {
        'Client':autocomplete.ModelSelect2(url='analytics:client-autocomplete'),
        'Location':autocomplete.ModelSelect2(url='analytics:location-autocomplete')
        }

class PartnerToKioskForm(forms.ModelForm):
    class Meta:
        model = PartnerToKiosk
        fields= ('Partner',)
        widgets= {
        'Partner':autocomplete.ModelSelect2(url='analytics:partner-autocomplete'),
        }
class PortForm(forms.ModelForm):
    class Meta:
        model = Port
        fields = '__all__'
        exclude = ('Kiosk',)
