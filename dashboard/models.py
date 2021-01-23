from django.db import models
from projects.models import Simulation

KPI_COSTS_TOOLTIPS = {
    "Replacement_costs_during_project_lifetime": "Costs for replacement of assets which occur over the project lifetime.",
    "annuity_om": "Annuity of the operation, maintenance and dispatch costs of the energy system, ie. Ballpoint number of the annual expenses for system operation.",
    "annuity_total": "Annuity of the net present costs (NPC) of the energy system.", 
    "costs_cost_om": "Costs for fix annual operation and maintenance costs over the whole project lifetime, that do not depend on the assets dispatch but solely on installed capacity.",
    "costs_dispatch": "Dispatch costs over the whole project lifetime including all expenditures that depend on the dispatch of assets, ie. fuel costs, electricity consumption from the external grid, costs for operation and maintainance that depend on the thoughput of an asset.",
    "costs_investment_over_lifetime": "Investment costs over the whole project lifetime, including all replacement costs.",
    "costs_om_total": "Costs for annual operation and maintenance costs as well as dispatch of all assets of the energy system, for the whole project duration.",
    "costs_total": "Net present costs of the system for the whole project duration, includes all operation, maintainance and dispatch costs as well as the investment costs (including replacements).",
    "costs_upfront_in_year_zero": "The costs which will have to be paid upfront when project begin, ie. In year 0.",
    "levelized_cost_of_energy_of_asset": "Cost per kWh thoughput though an asset, based on the assets costs during the project lifetime as well as the total thoughput though the asset in the project lifetime. For generation assets, equivalent to the levelized cost of generation."
}

KPI_SCALAR_UNITS = {
    "Attributed costsElectricity": "€",
    "Degree of autonomy": "fraction",
    "Levelized costs of electricity equivalent": "€/kWh",
    "Levelized costs of electricity equivalentElectricity": "€/kWh",
    "Onsite energy fraction": "fraction",
    "Onsite energy matching": "fraction",
    "Renewable factor": "fraction",
    "Renewable share of local generation": "fraction",
    "Replacement_costs_during_project_lifetime": "€",
    "Specific emissions per electricity equivalent": "kg GHGeq/kWh",
    "Total emissions": "GHGeq/annum",
    "Total internal generation": "kWh/annum",
    "Total internal non-renewable generation": "kWh/annum",
    "Total internal renewable generation": "kWh/annum",
    "Total non-renewable energy use": "kWh/annum",
    "Total renewable energy use": "kWh/annum",
    "Total_demandElectricity": "kWh/annum",
    "Total_demandElectricity_electricity_equivalent": "kWh/annum",
    "Total_demand_electricity_equivalent": "kWh/annum",
    "Total_excessElectricity": "kWh/annum",
    "Total_excessElectricity_electricity_equivalent": "kWh/annum",
    "Total_excess_electricity_equivalent": "kWh/annum",
    "Total_feedinElectricity": "kWh/annum",
    "Total_feedinElectricity_electricity_equivalent": "kWh/annum",
    "Total_feedin_electricity_equivalent": "kWh/annum",
    "annuity_om": "€/annum",
    "annuity_total": "€/annum",
    "costs_cost_om": "€",
    "costs_dispatch": "€",
    "costs_investment_over_lifetime": "€",
    "costs_om_total": "€",
    "costs_total": "€",
    "costs_upfront_in_year_zero": "€"
}


class KPIScalarResults(models.Model):
    scalar_values = models.TextField()  # to store the scalars dict
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)


class KPICostsMatrixResults(models.Model):
    cost_values = models.TextField()  # to store the scalars dict
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)


class AssetsResults(models.Model):
    assets_list = models.TextField()  # to store the assets list
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
