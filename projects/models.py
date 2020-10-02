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

FLOW_DIRECTION = (
    ('B2A', 'Bus_to_Asset'),
    ('A2B', 'Asset_to_Bus'),
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
    ('input_timeseries', 'input_timeseries'),
    ('crate', 'crate'),
    ('efficiency', 'efficiency'),
    ('self_discharge', 'self_discharge'),
    ('soc_initial', 'soc_initial'),
    ('soc_max', 'soc_max'),
    ('soc_min', 'soc_min'),
    ('dispatchable', 'dispatchable'),
    ('maximum_capacity', 'maximum_capacity'),
    ('energy_price', 'energy_price'),
    ('feedin_tariff', 'feedin_tariff'),
    ('peak_demand', 'peak_demand'),
    ('peak_demand_pricing_period', 'peak_demand_pricing_period'),
    ('renewable_share', 'renewable_share'),
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

BUS_TYPE = (
    ('bus_electricity', 'bus_electricity'),
    ('bus_heat', 'bus_heat'),
    ('bus_gas', 'bus_gas'),
)


class EconomicData(models.Model):
    duration = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY)
    discount = models.FloatField()
    annuity_factor = models.FloatField()
    tax = models.FloatField()
    crf = models.FloatField()


class Project(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=120)
    description = models.TextField()
    country = models.CharField(max_length=20, choices=COUNTRY)
    latitude = models.FloatField()
    longitude = models.FloatField()
    economic_data = models.OneToOneField(EconomicData, on_delete=models.SET_NULL, null=True)
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


class AssetType(models.Model):
    asset_type = models.CharField(max_length=30, choices=ASSET_TYPE, null=False, unique=True)
    asset_category = models.CharField(max_length=30, choices=ASSET_CATEGORY)
    energy_vector = models.CharField(max_length=20, choices=ENERGY_VECTOR)
    mvs_type = models.CharField(max_length=20, choices=MVS_TYPE)
    asset_fields = models.TextField(null=True)


class TopologyNode(models.Model):
    name = models.CharField(max_length=60)
    pos_x = models.FloatField(default=0.0)
    pos_y = models.FloatField(default=0.0)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ValueType(models.Model):
    type = models.CharField(max_length=30, null=False, unique=True)
    unit = models.CharField(max_length=30, null=True)


class Asset(TopologyNode):
    age_installed = models.FloatField(null=False)
    installed_capacity = models.FloatField(null=False,)
    capex_fix = models.FloatField(null=False,)  # development_costs
    capex_var = models.FloatField(null=False,)  # specific_costs
    opex_fix = models.FloatField(null=False,)  # specific_costs_om
    opex_var = models.FloatField(null=False,)  # dispatch_price
    lifetime = models.IntegerField(null=False,)
    optimize_cap = models.BooleanField(null=False, default=False)
    input_timeseries = models.TextField(null=True)
    crate = models.FloatField(null=True)
    efficiency = models.FloatField(null=True)
    self_discharge = models.FloatField(null=True)
    soc_initial = models.FloatField(null=True)
    soc_max = models.FloatField(null=True)
    soc_min = models.FloatField(null=True)
    dispatchable = models.BooleanField(null=True, default=False)
    maximum_capacity = models.FloatField(null=True)
    energy_price = models.FloatField(null=True)
    feedin_tariff = models.FloatField(null=True)
    peak_demand_pricing = models.FloatField(null=True)
    peak_demand_pricing_period = models.FloatField(null=True)
    renewable_share = models.FloatField(null=True)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, null=True)


class Bus(TopologyNode):
    type = models.CharField(max_length=20, choices=BUS_TYPE)


class ConnectionLink(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=False)
    flow_direction = models.CharField(max_length=15, choices=FLOW_DIRECTION, null=False)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=False)
