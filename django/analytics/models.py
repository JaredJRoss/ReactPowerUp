from django.db import models

#All Classes

#Partners own Kiosks which they rent to clients
class Partner(models.Model):
    def __str__(self):
        return self.PartnerName

    PartnerName = models.CharField(name = "PartnerName",max_length = 150)

#Keep Track of clients who are using kiosks
class Client(models.Model):
    def __str__(self):
        return self.ClientName

    ClientName = models.CharField(name = "ClientName", max_length=150,unique=True)
    Logo = models.FileField(upload_to='logo',blank=True,null=True)

#Catergories for type of clients for search purposes
class Catergories(models.Model):
    def __str__(self):
        return self.Type

    Type = models.CharField(name = "Type", max_length = 100,unique=True)

#The location that the kiosk is at
class Location(models.Model):
    def __str__(self):
        return self.LocationName

    LocationName = models.CharField(name = "LocationName",max_length = 150,unique=True)
    Address = models.CharField(name="Address", max_length=150)

#The actual powerboard
class Kiosk(models.Model):
    def __str__(self):
        return "Kiosk:"+str(self.ID) + " with client "+self.Client.ClientName+" at location "+self.Location.LocationName

    ID = models.IntegerField(verbose_name="ID", primary_key=True)
    Location = models.ForeignKey(Location,blank=True,null=True, related_name='KioskToLocation' ,on_delete=models.CASCADE)
    Client = models.ForeignKey(Client,related_name='KioskToClient' ,on_delete=models.CASCADE)
    CreatedOn= models.DateTimeField()
class KioskHistory:
    ID = models.IntegerField(verbose_name="ID", primary_key=True)
    Location = models.ForeignKey(Location,blank=True,null=True, related_name='KioskToLocation' ,on_delete=models.CASCADE)
    Client = models.ForeignKey(Client,related_name='KioskToClient' ,on_delete=models.CASCADE)
    CreatedOn= models.DateTimeField()
    DeactivatedOn = models.DateTimeField()
    #Port number on the board for charging need to identify with port number and kiosk
#has own primary key to make relational easier
class Port(models.Model):
    def __str__(self):
        return "Kiosk:"+str(self.Kiosk.ID) + " Port:" +str(self.Port)+" Type: "+self.Type
    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Product.
        """
        return reverse('port-detail', args=[str(self.id)])

    Type_Of_Charger = (
        ('IPhone', 'IPhone'),
        ('Android', 'Android'),
        ('USB-C', 'USB-C'),
        ('Other','Other')
    )
    Port = models.IntegerField(verbose_name="Port", primary_key=True)
    Kiosk = models.ForeignKey(Kiosk,related_name='KioskToPort',on_delete=models.CASCADE)
    Type = models.CharField(verbose_name = "Type", max_length=20, choices=Type_Of_Charger, default ='Other')

#Keep track of times for each port
class Time(models.Model):
    def __str__(self):
        return 'Kiosk:'+str(self.Port.Kiosk.ID)+' Port:'+str(self.Port.Port) + " Time In:" +self.TimeIn.strftime("%Y-%m-%d %H:%M:%S") \
        + " Time Out:" +self.TimeOut.strftime("%Y-%m-%d %H:%M:%S")

    Port = models.ForeignKey(Port,related_name='PortToTime',on_delete=models.CASCADE)
    TimeIn = models.DateTimeField(verbose_name = "TimeIn")
    TimeOut = models.DateTimeField(verbose_name = "TimeOut")

#Relational Tables

#Match partners with client
class PartnerToClient(models.Model):
    def __str__(self):
        return "Partner:"+self.Partner.PartnerName + " has Client "+self.Client.ClientName
    Partner = models.ForeignKey(Partner ,on_delete=models.CASCADE)
    Client = models.ForeignKey(Client ,on_delete=models.CASCADE)

class PartnerToKiosk(models.Model):
    def __str__(self):
        return "Partner:"+self.Partner.PartnerName + " has Kiosk "+str(self.Kiosk.ID)
    Partner = models.ForeignKey(Partner ,on_delete=models.CASCADE)
    Kiosk = models.ForeignKey(Kiosk ,on_delete=models.CASCADE)

class ClientToType(models.Model):
    def __str__(self):
        return "Client:"+self.Client.ClientName + " has type "+self.Type.Type
    Type = models.ForeignKey(Catergories ,on_delete=models.CASCADE)
    Client = models.ForeignKey(Client ,on_delete=models.CASCADE)
