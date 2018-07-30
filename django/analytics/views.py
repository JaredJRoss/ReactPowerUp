from django.shortcuts import render
from django.contrib.auth.models import User, Group
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
from django.utils import timezone
import pytz
from pytz import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import Trunc
from django.db.models import Sum, Count
import json
from django.core.serializers.json import DjangoJSONEncoder

#pdf
from .render import Render


def signupPartner(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseRedirect(reverse('analytics:home'))

    form = MyRegistrationForm(request.POST or None)
    if request.method == 'POST':
        print("FORM",form.errors)
        if form.is_valid():
            p = request.POST.get("Partner", None)
            try:
                partner = Partner.objects.get(pk=p)
            except Partner.DoesNotExist:
                return render(request,'signupPartner.html',{'form':form,'alert':'Please pick a partner or use the drop down to create a new one'})

            user = form.save()
            UserToPartner.objects.create(User = user, Partner = partner)
            group = Group.objects.get(name='Partner')
            group.user_set.add(user)
            return HttpResponseRedirect(reverse('analytics:home'))
    return render(request, 'signupPartner.html', {'form': form,'alert':''})

def signupAdmin(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseRedirect(reverse('analytics:home'))

    form = MyRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Admin')
            group.user_set.add(user)
            return HttpResponseRedirect(reverse('analytics:home'))
    return render(request, 'signupAdmin.html', {'form': form})

def signupClient(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseRedirect(reverse('analytics:home'))

    form = MyRegistrationForm(request.POST or None)
    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            c = request.POST.get("Client",None)
            try:
                client = Client.objects.get(pk = c)
            except Client.DoesNotExist:
                return render(request, 'signupClient.html', {'form': form, 'alert':'Please select a client or use the dropdown to create a new one'})
            user = form.save()            
            UserToClient.objects.create(User = user, Client = client)
            group =  Group.objects.get(name='Client')
            group.user_set.add(user)
            return HttpResponseRedirect(reverse('analytics:home'))

    return render(request, 'signupClient.html', {'form': form,alert:''})

@ensure_csrf_cookie
def edit_client(request):
    print(request.POST)
    if request.user.is_authenticated and (request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Partner').exists()):
        form = False
        query_set = Kiosk.objects.none()
        kioskFilter  = KioskFilter(request.GET,query_set)
        clientform = ClientForm(request.POST or None)
        new_C_name = request.POST.get('ClientName',None)
        client = request.POST.get('Client',None)
        if new_C_name and client:
            c = Client.objects.get(pk=client)
            c.ClientName = new_C_name
            c.save()
            form = True
        if form:
            HttpResponseRedirect(reverse('analytics:editClient'))
        context ={
        'clientform':clientform,
        'filter':kioskFilter,
        }
        return render(request,'editClient.html',context)
    else:
        return HttpResponseRedirect(reverse('analytics:home'))

@ensure_csrf_cookie
def edit_location(request):
         
    if request.user.is_authenticated and (request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Partner').exists()):       
        
        l = request.POST.get('Location',None)
        
        if l:
            location = Location.objects.get(pk = l)
            locationform = LocationForm(data = request.POST,instance = location)

            if locationform.is_valid():
                l = locationform.save()
                return HttpResponseRedirect(reverse('analytics:home'))
            context ={
            'locationform':locationform,
            } 
        
            return render(request,'editLocation.html',context)
        else:
            locationform = LocationForm(data = request.POST)
            context ={
            'locationform':locationform,
            } 
        
            return render(request,'editLocation.html',context)
    else:
        return HttpResponseRedirect(reverse('analytics:home'))

@ensure_csrf_cookie
def edit_partner(request):
    if request.user.is_authenticated and (request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Partner').exists()):
        new_P_name = request.POST.get('PartnerName',None)
        partner =  request.POST.get('Partner',None)
        client = request.POST.get('Client',None)
        print(request.POST)
        if partner:
            p = Partner.objects.get(pk=partner)
            if new_P_name:
                p.PartnerName = new_P_name
                p.save()
                return HttpResponseRedirect(reverse('analytics:home'))
            if client:
                c = Client.objects.get(pk = client)
                PartnerToClient.objects.create(Partner = p, Client = c)    
                return render(request,'editPartner.html')
            return render(request,'editPartner.html')

        return render(request,'editPartner.html')
    else:
        return HttpResponseRedirect(reverse('analytics:home'))

def edit_kiosk(request,pk):
    if request.user.is_authenticated:
        kiosk = Kiosk.objects.get(ID=pk)
        kioskform = KioskForm(request.POST or None, instance = kiosk)
        if kioskform.is_valid():
            kioskform.save()
            return HttpResponseRedirect(reverse('analytics:home'))
        context ={
        'kioskform':kioskform,
        'pk':pk
        }
        return render(request,'edit_kiosk.html',context)
    else:
        return HttpResponseRedirect(reverse('analytics:home'))

def deleteKiosk(request,pk):
    if request.user.is_authenticated:
        kiosk = Kiosk.objects.get(ID=pk)
        if request.method == 'POST':
            kiosk.delete()
            return HttpResponseRedirect(reverse('analytics:home'))

def deletePartner(request,pk):
    if request.user.is_authenticated and  request.user.groups.filter(name='Admin').exists():
        partner = Partner.objects.get(pk=pk)
        partner.delete()
        return HttpResponseRedirect(reverse('analytics:home'))
    else:
        return HttpResponseRedirect(reverse('analytics:home'))
def deleteClient(request,pk):
    if request.user.is_authenticated and  request.user.groups.filter(name='Admin').exists():
        client = Client.objects.get(pk=pk)
        client.delete()
        return HttpResponseRedirect(reverse('analytics:home'))
    else:
        return HttpResponseRedirect(reverse('analytics:home'))
def deleteLocation(request,pk):
    if request.user.is_authenticated and  request.user.groups.filter(name='Admin').exists():
        location = Location.objects.get(pk=pk)
        location.delete()
        return HttpResponseRedirect(reverse('analytics:home'))
    else:
        return HttpResponseRedirect(reverse('analytics:home'))        
def edit_port(request,pk):
    if request.user.is_authenticated:
        port = Port.objects.get(pk=pk)
        portform = PortForm(request.POST or None, instance = port)
        if portform.is_valid():
            portform.save()
            return HttpResponseRedirect(reverse('analytics:kiosk', args=[port.Kiosk.ID]))
        context ={
        'portform':portform,
        }
        return render(request,'edit_port.html',context)


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

def kiosk_info(request):
    arr = []
    if request.user.groups.filter(name='Admin').exists():
        qs = Kiosk.objects.all()
    elif request.user.groups.filter(name='Partner').exists():
        partner = UserToPartner.objects.get(User = request.User)
        clients = PartnerToKiosk.objects.filter(Partner=partner.Partner)
        qs = Kiosk.objects.filter(ID__in = clients.values('Kiosk_id'))
    elif request.user.groups.filter(name='Client').exists():
        client = UserToClient.objects.get(User = request.user)
        qs = Kiosk.objects.filter(Client = client.Client)
    else:
        qs = Kiosk.objects.none()
    kioskFilter = KioskFilter(request.GET,qs)
    for kiosk in kioskFilter.qs:
        k = {}
        k['ID'] = kiosk.ID
        k['Client'] = kiosk.Client.ClientName
        k['Loc'] = kiosk.Location.LocationName
        ports = Port.objects.filter(Kiosk = kiosk)
        times = Time.objects.filter(Port__in = ports)
        times = filter_dates(times,request.GET)
        k['Tot'] = times.count()
        try:
            last = times.latest('TimeOut').TimeOut
            k['last_update'] = last.strftime("%m/%d")
            if (datetime.datetime.now().replace(tzinfo=None)-last.replace(tzinfo=None)).days > 5:
                k['online'] = False
            else:
                k['online'] = True
        except Time.DoesNotExist:
            k['last_update'] = None
            k['online'] = False
        arr.append(k)
    return arr

def TimeOfDayHigh(times):
    val = []
    for i in range(0,24):
        val.append(times.filter(TimeOut__hour=i).count())
    return val

#Does not filter right now
def DayBarHigh(times):
    val = []
    query_set = times.annotate(day = Trunc('TimeOut','day'))\
    .values('day')\
    .annotate(c=Count('pk'))\
    .values('day','c').order_by('day')
    
    for count in query_set:
        val.append([str(count['day'].year)+"-"+str(count['day'].month)+"-"+str(count['day'].day),count['c']])
    return val

def TypeOfChargePieHigh(ports,times):
    a = ports.filter(Type='Android')
    i = ports.filter(Type='IPhone')
    u = ports.filter(Type='USB-C')
    o = ports.filter(Type='Other')
    android = times.filter(Port__in =a)
    iphone =  times.filter(Port__in =i)
    usbc =  times.filter(Port__in =u)
    other =  times.filter(Port__in =o)
    total = iphone.count()+android.count()+usbc.count()+other.count()
    try:
        a_percent = str(int(100*(android.count()/total)))
    except ZeroDivisionError:
        a_percent=str(0)
    try:
        i_percent = str(int(100*(iphone.count()/total)))
    except ZeroDivisionError:
        i_percent=str(0)
    try:
        u_percent = str(int(100*(usbc.count()/total)))
    except ZeroDivisionError:
        u_percent=str(0)
    try:
        o_percent = str(int(100*(other.count()/total)))
    except ZeroDivisionError:
        o_percent=str(0)
    if total ==0:
        val = [{'name':'No Charges','y':100}]
    else:
        val = [{'name':'Android','y':100*(android.count()/total)},{'name':'Apple','y':100*(iphone.count()/total)},\
        {'name':'USB-C','y':100*(usbc.count()/total)},{'name':'Other','y':100*(other.count()/total)}]
    return val


def dashboardData(request):
    val = {}
    if request.user.groups.filter(name='Admin').exists():
        qs = Kiosk.objects.all()
    elif request.user.groups.filter(name='Partner').exists():
        partner = UserToPartner.objects.get(User = request.user)
        clients = PartnerToClient.objects.filter(Partner=partner.Partner)
        qs = Kiosk.objects.filter(Client__in = clients.values('Client'))
    elif request.user.groups.filter(name='Client').exists():
        client = UserToClient.objects.get(User = request.user)
        qs = Kiosk.objects.filter(Client = client.Client)
    else:
        qs = Kiosk.objects.none()
    kioskFilter = KioskFilter(request.GET,qs)
    ports = Port.objects.filter(Kiosk__in = kioskFilter.qs)
    times = Time.objects.filter(Port__in = ports)
    times = filter_dates(times,request.GET)
    val['count'] = times.count()
    try:
        val['avg'] = int(times.aggregate(Sum('Duration'))['Duration__sum']/times.count())
    except TypeError:
        val['avg'] = 0
    val['TimeOfDayHigh'] = TimeOfDayHigh(times)
    val['TypeOfChargeHigh'] = TypeOfChargePieHigh(ports,times)
    val['BarDay'] = DayBarHigh(times)
    return val


@ensure_csrf_cookie
def pdf(request):
    if request.user.is_authenticated:
        context={
        'user':request.user.username,
        'table':kiosk_info(request),
        'dashboard':dashboardData(request),
        }
        print(context)
        return Render.render('pdf.html',context)
    else:
        return HttpResponseRedirect(reverse('analytics:login'))
def testPdf(request):
    print(request.GET)
    dashboard = dashboardData(request)
    context={
        'user':request.user.username,
        'table':kiosk_info(request),
        'pie':json.dumps(dashboard['TypeOfChargeHigh'], cls=DjangoJSONEncoder),
        'barDay':json.dumps(dashboard['BarDay'], cls=DjangoJSONEncoder),
        'barTime':dashboard['TimeOfDayHigh'],
        'count':dashboard['count'],
        'avg':dashboard['avg']
        }
    #return Render.render('pdf_actual.html',context)
    return render(request,'pdf_actual.html',context)
    
#Takes a get request and parses the time in and out of each port kiosk combo
@csrf_exempt
def upload(request):
    test = ''
    if request.method == 'POST':
        test = test + 'POST:'+request.body.decode('utf-8')
    data = request.body.decode('utf-8')
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
                if port != '--':
                    print("Port int:",int(port))

                    try:
                        p = Port.objects.get(Port=int(port), Kiosk = K)
                    except Port.DoesNotExist:
                        if int(port) in [9,10]:
                            p = Port.objects.create(Port=int(port), Kiosk=K, Type='USB-C')
                        elif int(port) in [5,6,7,8]:
                            p = Port.objects.create(Port=int(port), Kiosk=K, Type='Android')
                        elif int(port) in [1,2,3,4]:
                            p = Port.objects.create(Port=int(port), Kiosk=K, Type='IPhone')
                        else:
                            p = Port.objects.create(Port=int(port), Kiosk=K, Type='Other')


                    month = date[0:2]
                    day = date[2:4]
                    year = '20'+date[4:6]
                    start_date = datetime.datetime.strptime(month+day+year+start,'%m%d%Y%H%M%S')
                    end_date = datetime.datetime.strptime(month+day+year+end,'%m%d%Y%H%M%S')

                    duration = round((end_date-start_date).total_seconds()/60)
                    if duration < 0:
                        end_date =  end_date+timedelta(days=1)
                        duration = round((end_date-start_date).total_seconds()/60)

                    Time.objects.create(Port = p,TimeIn=start_date,TimeOut=end_date,Duration=duration)
                    try:
                        days = DayCount.objects.get(Date__day = start_date.day, Date__month = start_date.month, Date__year = start_date.year)
                        days.Count = days.Count+1
                        days.save()
                    except DayCount.DoesNotExist:
                        DayCount.objects.create(Date = start_date, Count = 1)

            except Kiosk.DoesNotExist:
                client = Client.objects.get(ClientName="None")
                location = Location.objects.get(LocationName="None")
                K = Kiosk.objects.create(ID=int(ID), Client =client, CreatedOn=datetime.datetime.now(),Location=location)
                if port !='--':
                    p = Port.objects.create(Port=int(port), Kiosk=K,Type='Other')
                    month = date[0:2]
                    day = date[2:4]
                    year = '20'+date[4:6]
                    start_date = datetime.datetime.strptime(month+day+year+start,'%m%d%Y%H%M%S')
                    end_date = datetime.datetime.strptime(month+day+year+end,'%m%d%Y%H%M%S')
                    try:
                        day = DayCount.objects.get(Date__day = end_date.day, Date__month = end_date.month, Date__year = end_date.year)
                        day.Count = day.Count + 1
                        day.save()
                    except DayCount.DoesNotExist:
                        DayCount.objects.create(Date = end_date, Count = 1)

                    duration = round((end_date-start_date).total_seconds()/60)
                    Time.objects.create(Port = p,TimeIn=start_date,TimeOut=end_date,Duration=duration)
                return HttpResponse("New kiosk made")
    else:
        return HttpResponse("No data")

    return HttpResponse(status=200)

def filter_dates(times,GET):
    est = timezone('US/Eastern')
    start_date = datetime.datetime.now(est)
    start_date = start_date.replace(year=2016)
    end_date = datetime.datetime.now(est)
    start_date = start_date.replace(tzinfo=None)
    end_date = end_date.replace(tzinfo =None)
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


def resetKiosk(request,pk):
    print(pk)
    if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
        kiosk = Kiosk.objects.get(pk = pk)
        ports = Port.objects.filter(Kiosk = kiosk)
        times = Time.objects.filter(Port__in = ports)
        times.delete()
        return HttpResponseRedirect(reverse('analytics:kiosk',args = (pk,)))
    else:
        return HttpResponseRedirect(reverse('analytics:home')) 
@ensure_csrf_cookie
def kiosk_view(request,pk):
    if request.user.is_authenticated:
        kiosk = get_object_or_404(Kiosk, ID=pk)
        client = False
        partner = False
        if request.user.groups.filter(name='Partner').exists():
            partner = PartnerToKiosk.objects.get(Partner__User = request.user, Kiosk= kiosk)
            perm = 'partner'
        elif request.user.groups.filter(name='Client').exists():
            client  = request.user == kiosk.Client.User
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
                    kiosk = Kiosk.objects.get(ID=pk)
                    kiosk.Client = Client.objects.get(ClientName="None")
                    kiosk.Location = Location.objects.get(LocationName="None")

                    kiosk.save()
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

#creating everything that is needed like client location partner and kiosk
@ensure_csrf_cookie
def make_partner(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
        partnerform = PartnerForm(request.POST or None)
        if partnerform.is_valid():
            partner = partnerform.save(commit = False)
            myuser = User.objects.create_user(partner.PartnerName,'','password',is_staff=True)
            partner.User = myuser
            group =  Group.objects.get(name='Partner')
            group.user_set.add(myuser)
            partner.save()
            return HttpResponseRedirect(reverse('analytics:home'))
        return render(request,'new_partner.html',{'partnerform':partnerform})
    else:
        return HttpResponseRedirect(reverse('analytics:home'))


@ensure_csrf_cookie
def make_location(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
        locationform = LocationForm(request.POST or None)
        print(locationform.fields)
        if locationform.is_valid():
            location = locationform.save()
            return HttpResponseRedirect(reverse('analytics:home'))

        return render(request,'new_location.html',{'locationform':locationform})
    else:
        return HttpResponseRedirect(reverse('analytics:home'))
@ensure_csrf_cookie
def make_kiosk(request):
    if request.user.is_authenticated and not request.user.groups.filter(name='Client').exists():
        if request.user.groups.filter(name='Client').exists():
            return HttpResponseRedirect(reverse('analytics:home'))
        kiosk_form = KioskForm(request.POST or None)
        if kiosk_form.is_valid():
            k = kiosk_form.save(commit=False)
            k.CreatedOn = datetime.datetime.now()
            if request.user.groups.filter(name='Partner').exists():
                partner = Partner.objects.get(User=request.user)
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
        print('User',request)
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Admin').exists():
                client = Client.objects.create(ClientName = request.POST['text'])
                return http.JsonResponse({'id':client.pk,
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
            loc = Location.objects.create(Address = z.group(0), LocationName=name)
            return http.JsonResponse({
            'id':loc.pk,
            'text':loc.LocationName
            })
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        if self.request.user.groups.filter(name='Partner').exists():
            partner = UserToPartner.objects.get(User = self.request.user)
            kiosks = PartnerToKiosk.objects.filter(Partner = partner)
            qs = Location.objects.filter(pk__in=kiosks.values('Kiosk__Location') ).order_by("LocationName")
        elif self.request.user.groups.filter(name='Admin').exists():
            qs = Location.objects.all().order_by("LocationName")
        elif self.request.user.groups.filter(name='Client').exists():
            client = UserToClient.objects.get(User = request.user)
            kiosks = Kiosk.objects.filter(Client = client)
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
            partner = UserToPartner.objects.get(User = self.request.user)
            kiosks = PartnerToKiosk.objects.filter(Partner = partner)
            qs = Kiosk.objects.filter(ID__in = kiosks.values('Kiosk')).order_by('ID')
        elif self.request.user.groups.filter(name='Admin').exists():
            qs = Kiosk.objects.all().order_by("ID")
        elif self.request.user.groups.filter(name='Client').exists():
            client = UserToClient.objects.get(User = request.user)
            qs =  Kiosk.objects.filter(Client = client).order_by('ID')
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
    def post(self,request):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Admin').exists():
            partner = Partner.objects.create(PartnerName = request.POST['text'])
            return http.JsonResponse({
                    'id':partner.pk,
                    'text':partner.PartnerName
                    })
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
