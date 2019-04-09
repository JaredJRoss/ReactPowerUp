from django import forms
from .models import *
from dal import autocomplete
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

#This form is used to create a new user for clients, admin and partners
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

#creates a new partner not including the user which is hooked up in the views
class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        exclude=('User',)
        fields = '__all__'

#creates a new client with a clientname

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields=('ClientName',)

#creates a new location with all fields from the model
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

#creates a new kiosk that can use the autocomplete fields 
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

#Links a partner to a kiosk
class PartnerToKioskForm(forms.ModelForm):
    class Meta:
        model = PartnerToKiosk
        fields= ('Partner',)
        widgets= {
        'Partner':autocomplete.ModelSelect2(url='analytics:partner-autocomplete'),
        }

#creates a new port not including the kiosk which is hooked up in views         
class PortForm(forms.ModelForm):
    class Meta:
        model = Port
        fields = '__all__'
        exclude = ('Kiosk',)
