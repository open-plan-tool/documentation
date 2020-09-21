from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from django.db import models

COUNTRY = (
    ('', 'Choose...'),
    ('Norway', 'Norway'),
    ('Finland', 'Finland'),
    ('Germany', 'Germany'),
    ('Italy', 'Italy'),
)

CURRENCY = (
    ('', 'Choose...'),
    ('EUR', 'EUR'),
    ('NOK', 'NOK'),
    ('USD', 'USD'),
    ('GBP', 'GBP'),
)


ENERGY_VECTOR = (
    ('', 'Choose...'),
    ('electricity', 'electricity'),
    ('heat', 'heat'),
    ('gas', 'gas'),
    ('h2', 'h2'),
    ('mobility', 'mobility'),
)

MVS_TYPE = (
    ('', 'Choose...'),
    ('source', 'electricity'),
    ('sink', 'heat'),
    ('transformer', 'gas'),
    ('storage', 'h2'),
)

ASSET_CATEGORY = (
    ('', 'Choose...'),
    ('energy_provider', 'energy_provider'),
    ('energy_production', 'energy_production'),
    ('energy_conversion', 'energy_conversion'),
    ('energy_storage', 'energy_storage'),
    ('energy_consumption', 'energy_consumption'),
)

VALUE_TYPE = (
    ('', 'Choose...'),
    ('name', 'name'),
    ('age_installed', 'age_installed'),
    ('installed_capacity', 'installed_capacity'),
    ('capex_fix', 'capex_fix'),
    ('capex_var', 'capex_var'),
    ('opex_fix', 'opex_fix'),
    ('opex_var', 'opex_var'),
    ('lifetime', 'lifetime'),
    ('optimize_cap', 'optimize_cap'),
    ('historical_generation_data', 'historical_generation_data'),
    ('crate', 'crate'),
    ('efficiency', 'efficiency'),
    ('self_discharge', 'self_discharge'),
    ('soc_initial', 'soc_initial'),
    ('soc_max', 'soc_max'),
    ('soc_min', 'soc_min'),
    ('dispatchable', 'dispatchable'),
)

ASSET_TYPE = (
    ('', 'Choose...'),
    ('dso', 'dso'),
    ('electricity_excess', 'electricity_excess'),
    ('dso_feedin', 'dso_feedin'),
    ('demand', 'demand'),
    ('transformer_station_in', 'transformer_station_in'),
    ('transformer_station_out', 'transformer_station_out'),
    ('storage_charge_controller_in', 'storage_charge_controller_in'),
    ('storage_charge_controller_out', 'storage_charge_controller_out'),
    ('solar_inverter', 'solar_inverter'),
    ('dso_consumption', 'dso_consumption'),
    ('pv_plant', 'pv_plant'),
    ('wind_plant', 'wind_plant'),
    ('charging_power', 'charging_power'),
    ('discharging_power', 'discharging_power'),
    ('capacity', 'capacity'),
)



class EconomicData(models.Model):
    duration = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY)
    discount = models.FloatField()
    tax = models.FloatField()


class Project(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=120)
    description = models.TextField()
    country = models.CharField(max_length=20, choices=COUNTRY)
    latitude = models.FloatField()
    longitude = models.FloatField()
    economic_data = models.OneToOneField(EconomicData, on_delete=models.SET_NULL, null=True, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=60)
    body = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Scenario(models.Model):
    name = models.CharField(max_length=60)
    start_date = models.DateField()
    period = models.IntegerField()
    time_step = models.IntegerField()
    capex_fix = models.FloatField()
    capex_var = models.FloatField()
    opex_fix = models.FloatField()
    opex_var = models.FloatField()
    lifetime = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ElectricityAsset(models.Model):
    name = models.CharField(max_length=60)
    age_installed = models.FloatField()
    installed_capacity = models.FloatField()
    capex_fix = models.FloatField()
    capex_var = models.FloatField()
    opex_fix = models.FloatField()
    opex_var = models.FloatField()
    lifetime = models.IntegerField()
    optimize_cap = models.BooleanField()
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class AssetType(models.Model):
    asset_type = models.CharField(max_length=30, choices=ASSET_TYPE)
    asset_category = models.CharField(max_length=30, choices=ASSET_CATEGORY)
    energy_vector = models.CharField(max_length=20, choices=ENERGY_VECTOR)
    mvs_type = models.CharField(max_length=20, choices=MVS_TYPE)
    asset_fields = models.TextField(null=True)


class Asset(models.Model):
    name = models.CharField(max_length=60)
    age_installed = models.FloatField()
    installed_capacity = models.FloatField()
    capex_fix = models.FloatField()
    capex_var = models.FloatField()
    opex_fix = models.FloatField()
    opex_var = models.FloatField()
    lifetime = models.IntegerField()
    optimize_cap = models.BooleanField()
    historical_generation_data = models.TextField(null=True)
    crate = models.FloatField(null=True)
    efficiency = models.FloatField(null=True)
    self_discharge = models.FloatField(null=True)
    soc_initial = models.FloatField(null=True)
    soc_max = models.FloatField(null=True)
    soc_min = models.FloatField(null=True)
    dispatchable = models.BooleanField(null=True, default=False)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, null=True)

'''
class EnergyConsumption(models.Model):
    name = models.CharField(max_length=60)
    historical_consumption_data = models.TextField()
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EnergyProduction(models.Model):
    name = models.CharField(max_length=60)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EnergyConversion(models.Model):
    name = models.CharField(max_length=60)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EnergyStorage(models.Model):
    name = models.CharField(max_length=60)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
'''


class PVPlant(ElectricityAsset):
    historical_generation_data = models.TextField()
    #asset_type = models.ForeignKey(EnergyProduction, on_delete=models.CASCADE)

    def __str__(self):
        return "PV Plant"


class PVInverter(ElectricityAsset):
    efficiency = models.FloatField()
    #asset_type = models.ForeignKey(EnergyProduction, on_delete=models.CASCADE)

    def __str__(self):
        return "PV Inverter"

class WindPlant(ElectricityAsset):

    def __str__(self):
        return "Wind Plant"
    #asset_type = models.ForeignKey(EnergyProduction, on_delete=models.CASCADE)


class ESS(ElectricityAsset):

    def __str__(self):
        return "Energy Storage System (ESS)"
    #asset_type = models.ForeignKey(EnergyProduction, on_delete=models.CASCADE)


class ChargingPower(ElectricityAsset):
    crate = models.FloatField()
    efficiency = models.FloatField()
    self_discharge = models.FloatField()
    ess = models.OneToOneField(ESS, on_delete=models.CASCADE, primary_key=True,)


class Capacity(ElectricityAsset):
    efficiency = models.FloatField()
    soc_initial = models.FloatField()
    soc_max = models.FloatField()
    soc_min = models.FloatField()
    ess = models.OneToOneField(ESS, on_delete=models.CASCADE, primary_key=True,)


class DischargingPower(ElectricityAsset):
    crate = models.FloatField()
    efficiency = models.FloatField()
    ess = models.OneToOneField(ESS, on_delete=models.CASCADE, primary_key=True,)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)


class ChargeController(ElectricityAsset):
    efficiency = models.FloatField()
    ess = models.OneToOneField(ESS, on_delete=models.CASCADE, primary_key=True,)
    start_date = models.DateTimeField()
    period = models.IntegerField()
    time_step = models.IntegerField()

    def __str__(self):
        return self.name

#
# class Author(models.Model):
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('author_detail', args=[str(self.id)])
#
#
# class Project(models.Model):
#     name = models.CharField(max_length=255)
#     details = models.TextField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now_add=True)
#     electricity = models.BooleanField(default=False)
#     heat = models.BooleanField(default=False)
#     gas = models.BooleanField(default=False)
#     h2 = models.BooleanField(default=False)
#     ev = models.BooleanField(default=False)
#     author = models.ForeignKey(
#         Author,
#         on_delete=models.CASCADE,
#         related_name='location',
#     )
#     location = models.ForeignKey(
#         Location,
#         on_delete=models.CASCADE,
#         related_name='location',
#     )
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('project_detail', args=[str(self.id)])
