from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Project)
admin.site.register(EconomicData)
admin.site.register(Comment)
admin.site.register(Scenario)
#admin.site.register(EnergyConsumption)
#admin.site.register(EnergyProduction)
#admin.site.register(EnergyConversion)
admin.site.register(PVPlant)
admin.site.register(PVInverter)
admin.site.register(WindPlant)
admin.site.register(ESS)
admin.site.register(ChargingPower)
admin.site.register(Capacity)
admin.site.register(DischargingPower)
admin.site.register(ChargeController)

