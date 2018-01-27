from django.shortcuts import render
from django.contrib.auth.models import User
import datetime
from analytics.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from .filters import *

#Takes a get request and parses the time in and out of each port kiosk combo
def upload(request):
    data = request.GET.get("id",None)
    if data:
        arr = data.split("<CR>")
        for i in arr:
            kiosk = i.split(',')
            port= kiosk[0]
            ID = kiosk[1]
            start = kiosk[2]
            end = kiosk[3]
            K = Kiosk.objects.get(ID=ID)
            p = Port.object.get(Port=int(port), Kiosk = K)
            print('Kiosk:',K,' Port:',p,' Start:',start," End:",end)
    return render(request,'admin_view.html')

#creating everything that is needed like client location and kiosk
def make_user(request):
    print(request.POST)
    client_form = ClientForm(request.POST)
    if client_form.is_valid():
        print("Client")
        User.objects.create_user(request.POST['ClientName'],'','password',is_staff=True)
        client_form.save()
        return HttpResponseRedirect(reverse('analytics:add_user'))

    location_form = LocationForm(request.POST)
    if location_form.is_valid():
        print('location')
        print(location_form)
        location_form.save()
        return HttpResponseRedirect(reverse('analytics:add_user'))
    kiosk_form = KioskForm(request.POST)
    if kiosk_form.is_valid():
        print('kiosk')
        kiosk_form.save()
        return HttpResponseRedirect(reverse('analytics:add_user'))
    port_form = PortForm(request.POST)
    if port_form.is_valid():
        port_form.save()
        return HttpResponseRedirect(reverse('analytics:add_user'))

    context = {
    'clientform':client_form,
    'locationform':location_form,
    'kioskform':kiosk_form,
    'portform':port_form,
    }
    return render(request, 'new_user.html',context)



#autocomplete for clients
class ClientAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        qs = Client.objects.all().order_by("ClientName")
        if self.q:
            qs = qs.filter(ClientName__icontains=self.q)
        return qs
#autocomplete for clients
class LocationAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        qs = Location.objects.all().order_by("LocationName")
        if self.q:
            qs = qs.filter(LocationName__icontains=self.q)
        return qs
#autocomplete for clients
class KioskAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        qs = Kiosk.objects.all().order_by("ID")
        if self.q:
            qs = qs.filter(ID__icontains=self.q)
        return qs

def search(request):
    print(request.GET)
    query_set = Kiosk.objects.all()
    kioskFilter  = KioskFilter(request.GET,query_set)
    #print(Kiosk.objects.filter(''))
    print(kioskFilter.qs)
    return render(request,'search.html',{'kioskFilter':kioskFilter})
