from django.db import models
from projects.models import Simulation


class KPIScalarResults(models.Model):
    scalar_values = models.TextField()  # to store the scalars dict
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)


class KPICostsMatrixResults(models.Model):
    cost_values = models.TextField()  # to store the scalars dict
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)


class AssetsResults(models.Model):
    assets_list = models.TextField()  # to store the assets list
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
