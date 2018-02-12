from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
import datetime
import dateutil
from dateutil import parser
from datetime import timedelta
from analytics.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from .filters import *
from django.shortcuts import get_object_or_404
from django import http
import re
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.views.decorators.csrf import ensure_csrf_cookie



@ensure_csrf_cookie
def mainpage(request):
    context={
    'user':request.user.username
    }
    print(context)
    return render(request,'sample_app.html',context)

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

def filter_dates(times,GET):
    start_date = datetime.datetime.now().replace(year=2015)
    end_date = datetime.datetime.now()
    last = GET.get("date",None)
    if last:
        if last == 'hour':
            start_date = end_date - timedelta(hours=1)
        elif last == 'day':
            start_date = end_date - timedelta(days=1)
        elif last == 'week':
            start_date = end_date - timedelta(days=7)
        elif last == 'month':
            start_date = end_date - relativedelta(months=1)
        elif last == 'quarter':
            start_date = end_date - relativedelta(months=3)
        elif last == 'year':
            start_date = end_date.replace(month=1,day=1)
    start = GET.get('start',None)
    if start != None and start !='':
        start_date = parser.parse(start)
    end = GET.get('end',None)
    if end != None and end!='':
        end_date = parser.parse(end)

    print('start',start_date,' end date',end_date)
    return times.filter(TimeIn__range=(start_date,end_date))

def kiosk_view(request,pk):
    if request.user.is_authenticated:
        print('POST',request.POST)
        kiosk = get_object_or_404(Kiosk, ID=pk)
        client = False
        partner = False
        if request.user.groups.filter(name='Partner').exists():
            partner = PartnerToKiosk.objects.get(Partner__PartnerName = request.user, Kiosk= kiosk)
            perm = 'partner'
        elif request.user.groups.filter(name='Client').exists():
            client  = request.user.username == kiosk.Client.ClientName
            perm = 'client'
        else:
            perm='admin'
        if client or partner or request.user.groups.filter(name='Admin').exists():
            port_arr = []
            port = Port.objects.filter(Kiosk=kiosk)
            times = Time.objects.filter(Port__in=port)
            times = filter_dates(times,request.GET)
            for p in port:
                try:
                    temp_time = times.filter(Port= p)
                    last_update = temp_time.latest('TimeOut').TimeOut.replace(tzinfo=None)
                    total_count = temp_time.count()
                    elasped_time =  last_update - datetime.datetime.now().replace(tzinfo=None)
                    if elasped_time.days < -10:
                        flag = True
                    else:
                        flag = False
                except Time.DoesNotExist:
                    last_update = None
                    total_count = 0
                    flag = True
                port_arr.append({'Type':p.Type,'Port':p.Port,'Last_Update':last_update,'Flag':flag,'Total':total_count})
            print(times.count(),times.aggregate(Sum('Duration'))['Duration__sum'])
            portform = PortForm(request.POST)
            if portform.is_valid():
                new_port = portform.save(commit=False)
                new_port.Kiosk = kiosk
                new_port.save()
                print(new_port)
                return HttpResponseRedirect(reverse('analytics:kiosk', args=[pk]))
            kioskform = KioskForm(request.POST or None,instance= kiosk)
            if kioskform.is_valid():
                kiosk = Kiosk.objects.get(ID=pk)
                kiosk.Location = kioskform.cleaned_data['Location']
                kiosk.Client = kioskform.cleaned_data['Client']
                kiosk.save()
                print(kiosk)
                return HttpResponseRedirect(reverse('analytics:kiosk', args=[pk]))

            context = {
            'ports':port_arr,
            'kioskform':kioskform,
            'portform':portform,
            'permission':perm,
            }
            return render(request,'kiosk.html',context)
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
    def post(self,request):
        if self.request.user.is_authenticated:
            if request.user.groups.filter(name='Partner').exists():
                client = Client.objects.create(ClientName = request.POST['text'])
                partner =  Partner.objects.get(PartnerName=request.user)
                PartnerToClient.objects.create(Client=client,Partner=partner)
                return http.JsonResponse({
                'id':client.pk,
                'text':client.ClientName
                })
            elif request.user.groups.filter(name='Admin').exists():
                client = Client.objects.create(ClientName = request.POST['text'])
                return http.JsonResponse({
                'id':client.pk,
                'text':client.ClientName
                })
            else:
                return http.JsonResponse({'id':-1,
                'text':'You dont have permission to do that'
                })
        else:
            return http.HttpResponseForbidden()
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        print(self.request.user)
        if self.request.user.groups.filter(name='Partner').exists():
            clients = PartnerToClient.objects.filter(Partner__PartnerName = self.request.user)
            qs = Client.objects.filter(pk__in=clients.values('Client')).order_by('ClientName')
        elif self.request.user.groups.filter(name='Admin').exists():
            qs = Client.objects.all().order_by("ClientName")
        elif self.request.user.groups.filter(name='Client').exists():
            qs = Client.objects.filter(ClientName = self.request.user).order_by('ClientName')
        else:
            qs = Client.objects.none()
        if self.q:
            qs = qs.filter(ClientName__icontains=self.q)
        return qs
#autocomplete for clients
class LocationAutoComplete(autocomplete.Select2QuerySetView):
    def post(self,request):
        if self.request.user.is_authenticated:
            reg = re.compile('\d{5}')
            reg_name = re.compile('(^[a-zA-Z ]*)')
            z = reg.search(request.POST['text'])
            if z:
                name = reg_name.search(request.POST['text']).group(0)
                try:
                    loc = Location.objects.get(LocationName = name)
                except Location.DoesNotExist:
                    loc = Location.objects.create(Address = z.group(0), LocationName=name)
                return http.JsonResponse({
                'id':loc.pk,
                'text':loc.LocationName
                })
            else:
                print('no zip')
                return http.JsonResponse({
                'id':-1,
                'text':'Add a zipcode'
                })
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        if self.request.user.groups.filter(name='Partner').exists():
            kiosks = PartnerToKiosk.objects.filter(Partner__PartnerName = self.request.user)
            qs = Location.objects.filter(pk__in=kiosks.values('Kiosk__Location') ).order_by("LocationName")
        elif self.request.user.groups.filter(name='Admin').exists():
            qs = Location.objects.all().order_by("LocationName")
        elif self.request.user.groups.filter(name='Client').exists():
            kiosks = Kiosk.objects.filter(Client__ClientName = self.request.user)
            qs = Location.objects.filter(pk__in=kiosks.values('Kiosk__Location') ).order_by("LocationName")
        else:
            qs = Location.objects.none()
        if self.q:
            qs = qs.filter(LocationName__icontains=self.q)
        return qs
#autocomplete for clients
class KioskAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        if self.request.user.groups.filter(name='Partner').exists():
            kiosks = PartnerToKiosk.objects.filter(Partner__PartnerName = self.request.user)
            qs = Kiosk.objects.filter(ID__in = kiosks.values('Kiosk')).order_by('ID')
        elif self.request.user.groups.filter(name='Admin').exists():
            qs = Kiosk.objects.all().order_by("ID")
        elif self.request.user.groups.filter(name='Client').exists():
            qs =  Kiosk.objects.filter(Client__ClientName = self.request.user).order_by('ID')
        else:
            qs = Kiosk.objects.none()
        if self.q:
            qs = qs.filter(ID__icontains=self.q)
        return qs
class TypeAutoComplete(autocomplete.Select2QuerySetView):
    def post(self,request):
        print(request.POST)
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        qs = Catergories.objects.all().order_by("Type")
        if self.q:
            qs = qs.filter(Type__icontains=self.q)
        return qs

def search(request):
    print(request.GET)
    query_set = Kiosk.objects.all()
    kioskFilter  = KioskFilter(request.GET,query_set)
    #print(Kiosk.objects.filter(''))
    return render(request,'search.html',{'kioskFilter':kioskFilter})
