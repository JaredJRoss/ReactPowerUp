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
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import HttpResponse


def login(request):
    return render(request,'login.html')

@ensure_csrf_cookie
def mainpage(request):
    if request.user.is_authenticated:
        context={
        'user':request.user.username
        }
        print(context)
        return render(request,'sample_app.html',context)
    else:
        return HttpResponseRedirect(reverse('analytics:login'))

#Takes a get request and parses the time in and out of each port kiosk combo
@csrf_exempt
def upload(request):
    test = ''
    if request.method == 'POST':
        test = test + 'POST:'+request.body.decode('utf-8')
    data = request.body.decode('utf-8')
    print("data ",data)
    ServerTest.objects.create(Test=test)
    if data:
        arr = data.split("%")
        arr = arr[1:]
        print("arr ",arr)
        for i in arr:
            kiosk = i.split(',')
            ID= kiosk[0]
            port = kiosk[3]
            date = kiosk[2]
            start = kiosk[4]
            end = kiosk[5]
            try:
                K = Kiosk.objects.get(ID=int(ID))
                print(K)
                if port != '--':
                    p = Port.objects.get(Port=int(port), Kiosk = K)
                    month = date[0:2]
                    day = date[2:4]
                    year = '20'+date[4:6]
                    start_date = datetime.datetime.strptime(month+day+year+start,'%m%d%Y%H%M%S')
                    end_date = datetime.datetime.strptime(month+day+year+end,'%m%d%Y%H%M%S')
                    duration = round((end_date-start_date).total_seconds()/60)
                    print('start:', start_date,' end:',end_date)
                    Time.objects.create(Port = p,TimeIn=start_date,TimeOut=end_date,Duration=duration)
            except Kiosk.DoesNotExist:
                return HttpResponse("Kiosk does not exist")
    return HttpResponse(status=200)

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

    return times.filter(TimeIn__range=(start_date,end_date))


@ensure_csrf_cookie
def kiosk_view(request,pk):
    if request.user.is_authenticated:
        kiosk = get_object_or_404(Kiosk, ID=pk)
        client = False
        partner = False
        if request.user.groups.filter(name='Partner').exists():
            partner = PartnerToKiosk.objects.get(Partner__PartnerName = request.user, Kiosk= kiosk)
            perm = 'partner'
        elif request.user.groups.filter(name='Client').exists():
            client  = request.user.username == kiosk.Client.ClientName
            perm = 'client'
        elif request.user.groups.filter(name='Admin').exists():
            perm='admin'
        else:
            print('not authorized')

        if client or partner or request.user.groups.filter(name='Admin').exists():
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

            try:
                partner2kiosk = PartnerToKiosk.objects.get(Kiosk__ID=pk)
            except PartnerToKiosk.DoesNotExist:
                partner2kiosk=None

            partnerform = PartnerToKioskForm(request.POST or None,instance=partner2kiosk)
            if partnerform.is_valid():
                try:
                    partner2kiosk = PartnerToKiosk.objects.get(Kiosk__ID = pk)
                    partner2kiosk.Partner = partnerform.cleaned_data['Partner']
                    partner2kiosk.save()
                except PartnerToKiosk.DoesNotExist:
                    kiosk2p = Kiosk.objects.get(ID=pk)
                    PartnerToKiosk.objects.create(Kiosk=kiosk2p,Partner= partnerform.cleaned_data['Partner'])

                return HttpResponseRedirect(reverse('analytics:kiosk', args=[pk]))

            context = {
                'partnerform':partnerform,
                'kioskform':kioskform,
                'portform':portform,
                'permission':perm,
                'ID':pk,
            }
            return render(request,'kiosk.html',context)
#creating everything that is needed like client location and kiosk
@ensure_csrf_cookie
def make_kiosk(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Client').exists():
            return HttpResponseRedirect(reverse('analytics:home'))
        kiosk_form = KioskForm(request.POST or None)
        if kiosk_form.is_valid():
            k = kiosk_form.save(commit=False)
            k.CreatedOn = datetime.datetime.now()
            if request.user.groups.filter(name='Partner').exists():
                partner = Partner.objects.get(PartnerName=request.user)
                p2k = PartnerToKiosk(Kiosk = k, Partner=partner)
                k.save()
                p2k.save()
            else:
                k.save()


            return HttpResponseRedirect(reverse('analytics:home'))
        context = {
        'kioskform':kiosk_form,
        }
        return render(request, 'new_kiosk.html',context)
    else:
        return HttpResponseRedirect(reverse('analytics:home'))

#autocomplete for clients

class ClientAutoComplete(autocomplete.Select2QuerySetView):
    def post(self,request):
        print('User',request.user)
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Partner').exists():
                client = Client.objects.create(ClientName = request.POST['text'])
                partner =  Partner.objects.get(PartnerName=request.user)
                PartnerToClient.objects.create(Client=client,Partner=partner)
                User.objects.create_user(request.POST['text'],'','password',is_staff=True)
                return http.JsonResponse({
                'id':client.pk,
                'text':client.ClientName
                })
            elif request.user.groups.filter(name='Admin').exists():
                client = Client.objects.create(ClientName = request.POST['text'])
                User.objects.create_user(request.POST['text'],'','password',is_staff=True)
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
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        qs = Catergories.objects.all().order_by("Type")
        if self.q:
            qs = qs.filter(Type__icontains=self.q)
        return qs
class PartnerAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.request.user.groups.filter(name='Admin').exists():
            qs = Partner.objects.all().order_by("PartnerName")
        else:
            qs = Partner.objects.none()
        if self.q:
            qs = qs.filter(PartnerName__icontains=self.q)
        return qs

def search(request):
    print(request.GET)
    query_set = Kiosk.objects.all()
    kioskFilter  = KioskFilter(request.GET,query_set)
    #print(Kiosk.objects.filter(''))
    return render(request,'search.html',{'kioskFilter':kioskFilter})
