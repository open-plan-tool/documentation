from django.db import models


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
from projects.models import Asset


# class AssetResults(models.Model):
#     asset_id = models.ForeignKey(to='Asset', on_delete=models.CASCADE, null=True)
#     #output_power = models.ForeignKey(to='Asset', on_delete=models.DO_NOTHING, null=True)  # output power, i.e. storage discharging power
#     #input_power = models.ForeignKey(to='Asset', on_delete=models.DO_NOTHING, null=True)  # input power, i.e. storage charging power
#     #storage_capacity = models.ForeignKey(to='Asset', on_delete=models.DO_NOTHING, null=True)  # storage capacity, i.e. storage capacity
#     timeseries = models.BinaryField()
#     # connected_feedin_sink = models.CharField(max_length=20)
#     # connected_consumption_sources = models.CharField(max_length=20)
#     # outflow_direction = models.CharField(max_length=20)
#     # inflow_direction = models.CharField(max_length=20)
#     # output_bus_name = models.CharField(max_length=20)
#     # input_bus_name = models.CharField(max_length=20)
#     # renewable_asset = models.BooleanField()
#     # unit = models.CharField()  # asset unit (e.g. storage - kWh)
#
#     # 'storage capacity', 'unit'
#
#
# class AssetType(models.Model):
#     pass
#
#
# class Scenario(models.Model):
#     pass
#
#
# class Asset(models.Model):
#     asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, null=False, blank=True)
#     scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=False, blank=False)
#     parent_asset = models.ForeignKey(to='Asset', on_delete=models.CASCADE, null=True, blank=True)
#
#
# class Simulation(models.Model):
#     scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=False)
#
#
# class KPIResults(models.Model):
#     simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, null=False)
#     attributed_costsElectricity = models.FloatField()
#     levelized_costs_of_electricity_equivalent = models.FloatField()
#     Levelized_costs_of_electricity_equivalentElectricity = models.FloatField()
#     Renewable_share = models.FloatField()
#     Total_internal_non_renewable_generation = models.FloatField()
#     Total_internal_renewable_generation = models.FloatField()
#     Total_non_renewable_energy_use = models.FloatField()
#     Total_renewable_energy_use = models.FloatField()
#     Total_demandElectricity = models.FloatField()
#     Total_demandElectricity_electricity_equivalent = models.FloatField()
#     Total_demand_electricity_equivalent = models.FloatField()
#     Total_excessElectricity = models.FloatField()
#     Total_excessElectricity_electricity_equivalent = models.FloatField()
#     Total_excess_electricity_equivalent = models.FloatField()
#     annuity_om = models.FloatField()
#     annuity_total = models.FloatField()
#     costs_cost_om = models.FloatField()
#     costs_dispatch = models.FloatField()
#     costs_investment_over_lifetime = models.FloatField()
#     costs_om_total = models.FloatField()
#     costs_total = models.FloatField()
#     costs_upfront_in_year_zero = models.FloatField()