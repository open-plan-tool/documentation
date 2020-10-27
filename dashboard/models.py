from django.db import models

from projects.models import Simulation


class AssetResults(models.Model):
    costs_total = models.FloatField(null=False, blank=False),
    costs_om_total = models.FloatField(null=False, blank=False),
    costs_investment_over_lifetime = models.FloatField(null=False, blank=False),
    costs_upfront_in_year_zero = models.FloatField(null=False, blank=False),
    costs_dispatch = models.FloatField(null=False, blank=False),
    costs_cost_om = models.FloatField(null=False, blank=False),
    annuity_total = models.FloatField(null=False, blank=False),
    annuity_om = models.FloatField(null=False, blank=False),
    levelized_cost_of_energy_of_asset = models.FloatField(null=False, blank=False),

    unit = models.FloatField(null=False, blank=False),
    installedCap = models.FloatField(null=False, blank=False),
    optimizedAddCap = models.FloatField(null=False, blank=False),
    total_flow = models.FloatField(null=False, blank=False),
    annual_total_flow = models.FloatField(null=False, blank=False),
    peak_flow = models.FloatField(null=False, blank=False),
    average_flow = models.FloatField(null=False, blank=False),

    flow_data = models.TextField(null=True)  # models.BinaryField(default=b'\x08')  # timeseries
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, null=False)