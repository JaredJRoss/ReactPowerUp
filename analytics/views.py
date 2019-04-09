import datetime
import dateutil
from dateutil import parser
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import re
import pytz
from pytz import timezone
import json

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django import http
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import Trunc
from django.db.models import Sum, Count
from django.core.serializers.json import DjangoJSONEncoder
from django.db import utils

from analytics.forms import *

from .filters import *
#pdf
from .render import Render


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

#Creates a new partner with a user login that is linked together
def signupPartner(request):
    #only admin can use this view otherwise redirect them to the homepage
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseRedirect(reverse('analytics:home'))

    #User form
    form = MyRegistrationForm(request.POST or None)
    alert = ''
    if request.method == 'POST':
        #If the the user is valid continue
        if form.is_valid():
            #get the partner from the post request
            p = request.POST.get("Partner", None)
            try:
                partner = Partner.objects.get(pk=p)
            except Partner.DoesNotExist:
                #If no partner exists send the alert
                return render(request,'signupPartner.html',{'form':form,'alert':'Please pick a partner or use the drop down to create a new one'})
            #If a valid user and partner create a user 
            user = form.save()
            #link the user to the partner
            UserToPartner.objects.create(User = user, Partner = partner)
            #add the user to the partner group
            group = Group.objects.get(name='Partner')
            group.user_set.add(user)
            return HttpResponseRedirect(reverse('analytics:home'))
        else:
            alert = form.errors
            print(alert)

    return render(request, 'signupPartner.html', {'form': form,'alert':alert})

#create a new admin user
def signupAdmin(request):
    #Only admins can create new admin
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseRedirect(reverse('analytics:home'))

    form = MyRegistrationForm(request.POST or None)
    alert = ''
    #if a valid user is made link them up to the admin group
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Admin')
            group.user_set.add(user)
            return HttpResponseRedirect(reverse('analytics:home'))
        else:
            alert = form.errors
    return render(request, 'signupAdmin.html', {'form': form,'alert':alert})

#Create a user for a new client
def signupClient(request):
    #only admins can make new clients
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseRedirect(reverse('analytics:home'))

    #form to make a new user
    form = MyRegistrationForm(request.POST or None)
    alert = ''
    
    if request.method == 'POST':
        if form.is_valid():

            #get a client and if a valid one isnt provided return with an alert
            c = request.POST.get("Client",None)
            try:
                client = Client.objects.get(pk = c)
            except Client.DoesNotExist:
                return render(request, 'signupClient.html', {'form': form, 'alert':'Please select a client or use the dropdown to create a new one'})
            user = form.save()            
            #link a client to a user
            UserToClient.objects.create(User = user, Client = client)
            #add the user to the client group
            group =  Group.objects.get(name='Client')
            group.user_set.add(user)
            return HttpResponseRedirect(reverse('analytics:home'))
        else:
            alert = form.errors

    return render(request, 'signupClient.html', {'form': form,"alert":alert})

@ensure_csrf_cookie
def edit_client(request):
    #check to make sure the user is an admin or partner
    if request.user.is_authenticated and (request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Partner').exists()):
        form = False
        query_set = Kiosk.objects.none()
        kioskFilter  = KioskFilter(request.GET,query_set)
        clientform = ClientForm(request.POST or None)
        new_C_name = request.POST.get('ClientName',None)
        client = request.POST.get('Client',None)

        #if a new name and client is specified edit the client name 
        if new_C_name and client:
            c = Client.objects.get(pk=client)
            c.ClientName = new_C_name
            c.save()
            form = True
        #if the form was submitted redirect to editClient    
        if form:
            HttpResponseRedirect(reverse('analytics:editClient'))
        context ={
        'clientform':clientform,
        'filter':kioskFilter,
        }
        return render(request,'editClient.html',context)
    else:
        return HttpResponseRedirect(reverse('analytics:home'))

#Edits a locaiton
@ensure_csrf_cookie
def edit_location(request):
    #If the user is an admin or partner
    if request.user.is_authenticated and (request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Partner').exists()):       
        
        l = request.POST.get('Location',None)
        #get the location
        if l:
            location = Location.objects.get(pk = l)
            #pass in the post data to the new model
            locationform = LocationForm(data = request.POST,instance = location)
            #if its valid save the new information
            if locationform.is_valid():
                l = locationform.save()
                return HttpResponseRedirect(reverse('analytics:home'))
            context ={
            'locationform':locationform,
            } 
        
            return render(request,'editLocation.html',context)
        #pass in the form so the fields can be rendered
        else:
            locationform = LocationForm(data = request.POST)
            context ={
            'locationform':locationform,
            } 
        
            return render(request,'editLocation.html',context)
    else:
        return HttpResponseRedirect(reverse('analytics:home'))

#Edit a partner
@ensure_csrf_cookie
def edit_partner(request):
    #Only admins and partners can do this
    if request.user.is_authenticated and (request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Partner').exists()):
        new_P_name = request.POST.get('PartnerName',None)
        partner =  request.POST.get('Partner',None)
        #gets the list of clients
        try:
            clients = request.POST.getlist('Client')
        except KeyError:
            clients = None
        #if a partner is passed get the mode
        if partner:
            p = Partner.objects.get(pk=partner)
            #If there is a new name edit the name
            if new_P_name:
                p.PartnerName = new_P_name
                p.save()
            #if theres clients added create new relational
            if clients:
                for client in clients:
                    #get the client
                    c = Client.objects.get(pk = client)
                    #Create a new relation unless it exists then ignore it
                    try:
                        PartnerToClient.objects.create(Partner = p, Client = c)   
                    except utils.IntegrityError:
                        pass     
                           
            return render(request,'editPartner.html')

        return render(request,'editPartner.html')
    else:
        return HttpResponseRedirect(reverse('analytics:home'))

#Edit a kiosk
def edit_kiosk(request,pk):
    #any user can edit a kiosk if they are signed in
    if request.user.is_authenticated:
        kiosk = Kiosk.objects.get(ID=pk)
        #take in the post data and edit the kiosk specified
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
#delete a kiosk with pk
def deleteKiosk(request,pk):
    if request.user.is_authenticated:
        kiosk = Kiosk.objects.get(ID=pk)
        if request.method == 'POST':
            kiosk.delete()
            return HttpResponseRedirect(reverse('analytics:home'))
#delete a partner with primary key pk
def deletePartner(request,pk):
    #only admins can do this
    if request.user.is_authenticated and  request.user.groups.filter(name='Admin').exists():
        partner = Partner.objects.get(pk=pk)
        partner.delete()
        return HttpResponseRedirect(reverse('analytics:home'))
    else:
        return HttpResponseRedirect(reverse('analytics:home'))
#delete a client with primary key pk
def deleteClient(request,pk):
    #only admin can do this
    if request.user.is_authenticated and  request.user.groups.filter(name='Admin').exists():
        client = Client.objects.get(pk=pk)
        client.delete()
        return HttpResponseRedirect(reverse('analytics:home'))
    else:
        return HttpResponseRedirect(reverse('analytics:home'))
#delete a location with primary key pk        
def deleteLocation(request,pk):
    #only admin can do this
    if request.user.is_authenticated and  request.user.groups.filter(name='Admin').exists():
        location = Location.objects.get(pk=pk)
        location.delete()
        return HttpResponseRedirect(reverse('analytics:home'))
    else:
        return HttpResponseRedirect(reverse('analytics:home'))   

#edit a port         
def edit_port(request,pk):
    #any user can do this
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

#pass in the user name from request and load the react from sample_app.html
@ensure_csrf_cookie
def mainpage(request):
    if request.user.is_authenticated:
        context={
        'user':request.user.username
        }
        print(context)
        return render(request,'homePage.html',context)
    else:
        return HttpResponseRedirect(reverse('analytics:login'))
        
#Added the api functions in here because django does not like the circular imports since api uses
#filter dates so just copied them here they both do the same thing
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

#creates the pdf using the information from the request
def PDF(request):
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
#This is only used by the board to post times
@csrf_exempt
def upload(request):
    #this is for testing purposes once the boards work you can remove
    test = ''
    if request.method == 'POST':
        test = test + 'POST:'+request.body.decode('utf-8')
    #decodes the data into a string    
    data = request.body.decode('utf-8')
    ServerTest.objects.create(Test=test)
    #if data is passed parse the times
    if data:
        #split by % to get the parts we want
        arr = data.split("%")
        arr = arr[1:]

        for i in arr:
            #comma seperated list is sent
            kiosk = i.split(',')
            ID= kiosk[0]
            port = kiosk[3]
            date = kiosk[2]
            start = kiosk[4]
            end = kiosk[5]
            #if a kiosk that is already in use is passed use this
            try:
                K = Kiosk.objects.get(ID=int(ID))
                #sometimes data is sent that doesn't record a time ignore that
                if port != '--':
                    #get the port if it exists
                    try:
                        p = Port.objects.get(Port=int(port), Kiosk = K)
                    #if it doesn't exists create a new port based on the breakdown provided by Scott
                    except Port.DoesNotExist:
                        if int(port) in [9,10]:
                            p = Port.objects.create(Port=int(port), Kiosk=K, Type='USB-C')
                        elif int(port) in [5,6,7,8]:
                            p = Port.objects.create(Port=int(port), Kiosk=K, Type='Android')
                        elif int(port) in [1,2,3,4]:
                            p = Port.objects.create(Port=int(port), Kiosk=K, Type='IPhone')
                        else:
                            p = Port.objects.create(Port=int(port), Kiosk=K, Type='Other')

                    #break the date into sections to then have datetime parse
                    month = date[0:2]
                    day = date[2:4]
                    year = '20'+date[4:6]
                    #create the start and end datetime objects
                    start_date = datetime.datetime.strptime(month+day+year+start,'%m%d%Y%H%M%S')
                    end_date = datetime.datetime.strptime(month+day+year+end,'%m%d%Y%H%M%S')
                    #get the total time that passed between the start and end 
                    duration = round((end_date-start_date).total_seconds()/60)
                    #if the time is for example 11:55pm - 12:05 am change the day so its not a negative number
                    if duration < 0:
                        end_date =  end_date+timedelta(days=1)
                        duration = round((end_date-start_date).total_seconds()/60)
                    #create a new time with all the information
                    Time.objects.create(Port = p,TimeIn=start_date,TimeOut=end_date,Duration=duration)
            #if no kiosk exists create a new one and add all fields needed
            except Kiosk.DoesNotExist:
                #defualt to the None kiosk and None location
                client = Client.objects.get(ClientName="None")
                location = Location.objects.get(LocationName="None")
                #create the new kiosk with passed information
                K = Kiosk.objects.create(ID=int(ID), Client =client, CreatedOn=datetime.datetime.now(),Location=location)
                #same as above
                if port !='--':
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
                    #create the time
                    Time.objects.create(Port = p,TimeIn=start_date,TimeOut=end_date,Duration=duration)
                #response sent back to the boards
                return HttpResponse("New kiosk made")
    else:
        return HttpResponse("No data")

    return HttpResponse(status=200)

#filter the dates provided
def filter_dates(times,GET):
    est = timezone('US/Eastern')
    #set default start and end dates
    start_date = datetime.datetime.now(est)
    start_date = start_date.replace(year=2016)
    end_date = datetime.datetime.now(est)
    start_date = start_date.replace(tzinfo=None)
    end_date = end_date.replace(tzinfo =None)
    #last is when you press the past buttons ie past hour
    last = GET.get("date",None)
    if last:
        #minus the now by the apprioate amount
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
    #if custom start and end date are specified use that instead
    start = GET.get('start',None)
    if start != None and start !='' and start !='undefined' :
        #parser parse a bunch of datetime formats
        start_date = parser.parse(start)
    end = GET.get('end',None)
    if end != None and end!='' and end !='undefined' :
        end_date = parser.parse(end)
    return times.filter(TimeIn__range=(start_date,end_date))

#reset the kiosk by deleting all the times for that kiosk
def resetKiosk(request,pk):
    if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
        kiosk = Kiosk.objects.get(pk = pk)
        ports = Port.objects.filter(Kiosk = kiosk)
        times = Time.objects.filter(Port__in = ports)
        times.delete()
        return HttpResponseRedirect(reverse('analytics:kiosk',args = (pk,)))
    else:
        return HttpResponseRedirect(reverse('analytics:home'))

#django portion of the kiosk view
@ensure_csrf_cookie
def kiosk_view(request,pk):
    if request.user.is_authenticated:
        kiosk = get_object_or_404(Kiosk, ID=pk)
        client = False
        partner = False
        #filter permissions 
        if request.user.groups.filter(name='Partner').exists():
            partner = PartnerToKiosk.objects.get(Partner__User = request.user, Kiosk= kiosk)
            perm = 'partner'
        elif request.user.groups.filter(name='Client').exists():
            client  = request.user == kiosk.Client.User
            perm = 'client'
        elif request.user.groups.filter(name='Admin').exists():
            perm='admin'
        else:
            return HttpResponseRedirect(reverse('analytics:home'))

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



#autocomplete for clients
class ClientAutoComplete(autocomplete.Select2QuerySetView):
    #this allows you to create new clients within the autocomplete textbox
    def post(self,request):
        print('User',request)
        if request.user.is_authenticated:
            #check user permissions
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
#autocomplete for location
class LocationAutoComplete(autocomplete.Select2QuerySetView):
    #allows you to create a new location with just the name
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
#autocomplete for kiosks
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

