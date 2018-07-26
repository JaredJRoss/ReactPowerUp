from django import forms
from .models import *
from dal import autocomplete
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')        

    def save(self,commit = True):   
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']


        if commit:
            user.save()

        return user

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        exclude=('User',)
        fields = '__all__'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields=('ClientName',)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

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
