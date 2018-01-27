from django.contrib import admin

# Register your models here.
from analytics.models import *
from analytics.forms import *


admin.site.register(Partner)
admin.site.register(Client)
admin.site.register(Catergories)
admin.site.register(Location)
admin.site.register(Kiosk)
admin.site.register(Port)
admin.site.register(Time)
admin.site.register(PartnerToClient)
admin.site.register(PartnerToKiosk)
admin.site.register(ClientToType)
