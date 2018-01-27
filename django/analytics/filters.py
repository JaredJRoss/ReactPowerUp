import django_filters
from .models import *
from django import forms
from django.forms import TextInput
from dal import autocomplete

class KioskFilter(django_filters.FilterSet):
    Location = django_filters.ModelMultipleChoiceFilter(queryset=Location.objects.all(),
    widget = autocomplete.ModelSelect2Multiple(url="analytics:location-autocomplete"))

    Client =  django_filters.ModelMultipleChoiceFilter(queryset=Client.objects.all(),
    widget = autocomplete.ModelSelect2Multiple(url="analytics:client-autocomplete"))

    #Need to_filed_name or else it crashes becuase it returns Kiosk object which cant be used since
    #the model is a Kiosk so need it to return the int ID
    ID = django_filters.ModelMultipleChoiceFilter(name='ID',
    to_field_name='ID',
    queryset=Kiosk.objects.all(),
    widget = autocomplete.ModelSelect2Multiple(url="analytics:kiosk-autocomplete"))

    Type = django_filters.ModelMultipleChoiceFilter(method = 'customType',
    queryset= Catergories.objects.all())

    class Meta:
        model = Kiosk
        fields = ['Location','Client','ID','Type']

    def customType(self,queryset,name,value):
        client = ClientToType.objects.filter(Type__in=value)
        for c in client:
            return queryset.filter(**{'Client':c.Client.pk,})
