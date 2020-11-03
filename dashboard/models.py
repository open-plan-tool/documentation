from django.db import models
from django.conf import settings
# from projects.models import Simulation
from django.contrib.auth.models import AbstractUser

#
# class AssetResults(models.Model):
#     costs_total = models.FloatField(null=False, blank=False),
#     costs_om_total = models.FloatField(null=False, blank=False),
#     costs_investment_over_lifetime = models.FloatField(null=False, blank=False),
#     costs_upfront_in_year_zero = models.FloatField(null=False, blank=False),
#     costs_dispatch = models.FloatField(null=False, blank=False),
#     costs_cost_om = models.FloatField(null=False, blank=False),
#     annuity_total = models.FloatField(null=False, blank=False),
#     annuity_om = models.FloatField(null=False, blank=False),
#     levelized_cost_of_energy_of_asset = models.FloatField(null=False, blank=False),
#
#     unit = models.FloatField(null=False, blank=False),
#     installedCap = models.FloatField(null=False, blank=False),
#     optimizedAddCap = models.FloatField(null=False, blank=False),
#     total_flow = models.FloatField(null=False, blank=False),
#     annual_total_flow = models.FloatField(null=False, blank=False),
#     peak_flow = models.FloatField(null=False, blank=False),
#     average_flow = models.FloatField(null=False, blank=False),
#
#     flow_data = models.TextField(null=True)  # models.BinaryField(default=b'\x08')  # timeseries
#     simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, null=False)

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
    ('source', 'source'),
    ('sink', 'sink'),
    ('transformer', 'transformer'),
    ('storage', 'storage'),
)

ASSET_CATEGORY = [
    ('', 'Choose...'),
    ('energy_provider', 'energy_provider'),
    ('energy_production', 'energy_production'),
    ('energy_conversion', 'energy_conversion'),
    ('energy_storage', 'energy_storage'),
    ('energy_consumption', 'energy_consumption'),
]

SIMULATION_STATUS = (
    ('Failed', 'Failed'),
    ('Completed', 'Completed'),
    ('Running', 'Running'),
    ('Cancelled', 'Cancelled'),
)


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30)


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Scenario(models.Model):
    name = models.CharField(max_length=60)
    start_date = models.DateField()
    time_step = models.IntegerField()
    capex_fix = models.FloatField()
    capex_var = models.FloatField()
    opex_fix = models.FloatField()
    opex_var = models.FloatField()
    evaluated_period = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    pos_x = models.FloatField(default=0.0)
    pos_y = models.FloatField(default=0.0)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=False, blank=False)
    parent_asset = models.ForeignKey(to='Asset', on_delete=models.CASCADE, null=True, blank=True)
    age_installed = models.FloatField(null=True, blank=False)
    installed_capacity = models.FloatField(null=True, blank=False)
    capex_fix = models.FloatField(null=True, blank=False)  # development_costs
    capex_var = models.FloatField(null=True, blank=False)  # specific_costs
    opex_fix = models.FloatField(null=True, blank=False)  # specific_costs_om
    opex_var = models.FloatField(null=True, blank=False)  # dispatch_price
    lifetime = models.IntegerField(null=True, blank=False)
    asset_type = models.CharField(max_length=30, choices=ASSET_TYPE, null=False, unique=True)
    asset_category = models.CharField(max_length=30, choices=ASSET_CATEGORY)
    energy_vector = models.CharField(max_length=20, choices=ENERGY_VECTOR)
    mvs_type = models.CharField(max_length=20, choices=MVS_TYPE)


class Simulation(models.Model):
    start_date = models.DateTimeField(auto_now_add=True, null=False)
    end_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=SIMULATION_STATUS, null=False)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=False)
    results = models.BinaryField(null=True, max_length=30e6)


class AssetResults(models.Model):
    asset_id = models.FloatField(null=False, blank=False)


