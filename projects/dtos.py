import sys

from numpy.core import long
from typing import List
import json

from projects.models import *
from django.db import models


class ProjectDataDto:
    def __init__(self, project_id: str, project_name: str, scenario_id: str, scenario_name: str, country: str,
                 latitude: float, longitude: float):
        self.project_id = project_id
        self.project_name = project_name
        self.scenario_id = scenario_id
        self.scenario_name = scenario_name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude


class ValueTypeDto:
    def __init__(self, unit: str, value: float):
        self.unit = unit
        self.value = value


class EconomicDataDto:
    def __init__(self, currency: str, project_duration: ValueTypeDto, annuity_factor: ValueTypeDto,
                 discount_factor: ValueTypeDto, tax: ValueTypeDto, crf: ValueTypeDto):
        self.currency = currency
        self.project_duration = project_duration
        self.annuity_factor = annuity_factor
        self.discount_factor = discount_factor
        self.tax = tax
        self.crf = crf


class SimulationSettingsDto:
    def __init__(self, start_date: long, end_date: long, periods: int, evaluated_period: ValueTypeDto):
        self.start_date = start_date
        self.end_date = end_date
        self.periods = periods
        self.evaluated_period = evaluated_period


class TimeseriesDataDto:
    def __init__(self, unit: str, data: List[List[float]]):
        self.unit = unit
        self.data = data


class AssetDto:
    def __init__(self, asset_type: str, label: str, type_oemof: str, energy_vector: str, input_bus_name: str,
                 output_bus_name: str, dispatchable: bool, age_installed: ValueTypeDto, c_rate: ValueTypeDto,
                 soc_initial: ValueTypeDto,
                 soc_max: ValueTypeDto, soc_min: ValueTypeDto, development_costs: ValueTypeDto,
                 dispatch_price: ValueTypeDto, efficiency: ValueTypeDto,
                 installed_capacity: ValueTypeDto, lifetime: ValueTypeDto, maximum_capacity: ValueTypeDto,
                 energy_price: ValueTypeDto, feedin_tariff: ValueTypeDto, optimize_capacity: ValueTypeDto,
                 peak_demand_pricing: ValueTypeDto, peak_demand_pricing_period: ValueTypeDto,
                 renewable_share: ValueTypeDto, specific_costs: ValueTypeDto, specific_costs_om: ValueTypeDto,
                 input_timeseries: TimeseriesDataDto):
        self.asset_type = asset_type
        self.label = label
        self.type_oemof = type_oemof
        self.energy_vector = energy_vector
        self.input_bus_name = input_bus_name
        self.output_bus_name = output_bus_name
        self.dispatchable = dispatchable
        self.age_installed = age_installed
        self.c_rate = c_rate
        self.soc_initial = soc_initial
        self.soc_max = soc_max
        self.soc_min = soc_min
        self.development_costs = development_costs
        self.dispatch_price = dispatch_price
        self.efficiency = efficiency
        self.installed_capacity = installed_capacity
        self.lifetime = lifetime
        self.maximum_capacity = maximum_capacity
        self.energy_price = energy_price
        self.feedin_tariff = feedin_tariff
        self.optimize_capacity = optimize_capacity
        self.peak_demand_pricing = peak_demand_pricing
        self.peak_demand_pricing_period = peak_demand_pricing_period
        self.renewable_share = renewable_share
        self.specific_costs = specific_costs
        self.specific_costs_om = specific_costs_om
        self.input_timeseries = input_timeseries


class MVSRequestDto:
    def __init__(self, project_data: ProjectDataDto, economic_data: EconomicDataDto,
                 simulation_settings: SimulationSettingsDto, energy_providers: List[AssetDto],
                 energy_consumption: List[AssetDto], energy_conversion: List[AssetDto],
                 energy_production: List[AssetDto], energy_storage: List[AssetDto]):
        self.project_data = project_data
        self.economic_data = economic_data
        self.simulation_settings = simulation_settings
        self.energy_providers = energy_providers
        self.energy_consumption = energy_consumption
        self.energy_conversion = energy_conversion
        self.energy_production = energy_production
        self.energy_storage = energy_storage


# Function to serialize scenario topology models to JSON
def convert_to_dto(scenario: Scenario):
    # Retrieve models
    # scenario = Scenario.objects.get(pk=scenarioId)
    project = Project.objects.get(scenario=scenario)
    economic_data = EconomicData.objects.get(project=project)
    asset_list = Asset.objects.filter(scenario=scenario)
    bus_list = Bus.objects.filter(scenario=scenario)

    # Create  dto objects

    project_data_dto = ProjectDataDto(project.id,
                                      project.name,
                                      scenario.id,
                                      scenario.name,
                                      project.country,
                                      project.latitude,
                                      project.longitude)

    economic_data_dto = EconomicDataDto(economic_data.currency,
                                        to_value_type(economic_data, 'duration'),
                                        None,  # TODO: Add missing fields to DB
                                        to_value_type(economic_data, 'discount'),
                                        to_value_type(economic_data, 'tax'),
                                        None)

    # map_to_dto(economic_data, economic_data_dto)

    # Initialize asset lists depending on asset category
    energy_providers = []
    energy_production = []
    energy_consumption = []
    energy_storage = []
    energy_conversion = []

    # Iterate over assets
    for asset in asset_list:

        # Find all connections to asset
        connection_list = ConnectionLink.objects.filter(asset=asset)

        input_connection = ConnectionLink.objects.filter(asset=asset, flow_direction='B2A').first()
        output_connection = ConnectionLink.objects.filter(asset=asset, flow_direction='A2B').first()

        input_bus_name = input_connection.bus if input_connection is not None else None
        output_bus_name = output_connection.bus if output_connection is not None else None

        asset_dto = AssetDto(asset.asset_type.asset_category,
                             asset.name,
                             asset.asset_type.mvs_type,
                             asset.asset_type.energy_vector,
                             input_bus_name,
                             output_bus_name,
                             asset.dispatchable,
                             to_value_type(asset, 'age_installed'),
                             to_value_type(asset, 'crate'),
                             to_value_type(asset, 'soc_initial'),
                             to_value_type(asset, 'soc_max'),
                             to_value_type(asset, 'soc_min'),
                             to_value_type(asset, 'capex_fix'),
                             to_value_type(asset, 'opex_var'),
                             to_value_type(asset, 'efficiency'),
                             to_value_type(asset, 'installed_capacity'),
                             to_value_type(asset, 'lifetime'),
                             None,  # TODO: Add missing fields to DB
                             None,
                             None,
                             to_value_type(asset, 'optimize_cap'),
                             None,
                             None,
                             None,
                             to_value_type(asset, 'capex_var'),
                             to_value_type(asset, 'opex_fix'),
                             to_timeseries_data(asset, 'input_timeseries'), )

        # map_to_dto(asset, asset_dto)

        # Get category of asset and append to appropriate category
        if asset.asset_type.asset_category == 'energy_providers':
            energy_providers.append(asset_dto)
        elif asset.asset_type.asset_category == 'energy_production':
            energy_production.append(asset_dto)
        elif asset.asset_type.asset_category == 'energy_consumption':
            energy_consumption.append(asset_dto)
        elif asset.asset_type.asset_category == 'energy_storage':
            energy_storage.append(asset_dto)
        elif asset.asset_type.asset_category == 'energy_conversion':
            energy_conversion.append(asset_dto)

    mvs_request_dto = MVSRequestDto(project_data_dto, economic_data_dto, None, energy_providers, energy_consumption,
                                    energy_conversion, energy_production, energy_storage)

    return mvs_request_dto


def map_to_dto(model_obj, dto_obj):
    # Iterate over model attributes
    for f in model_obj._meta.get_fields():
        # For dto attributes that are user defined
        if hasattr(dto_obj, f.name):
            if ValueType.objects.all().filter(type=f.name).exists():
                setattr(dto_obj, f.name, to_value_type(model_obj, f.name))
            # For all other attributes
            else:
                setattr(dto_obj, f.name, getattr(model_obj, f.name))


def to_value_type(model_obj, field_name):
    unit = ValueType.objects.get(type=field_name).unit
    value = getattr(model_obj, field_name)
    return ValueTypeDto(unit, value)


def to_timeseries_data(model_obj, field_name):
    unit = ValueType.objects.get(type=field_name).unit
    value_list = json.loads(getattr(model_obj, field_name)) if getattr(model_obj, field_name) is not None else None
    return TimeseriesDataDto(unit, value_list)
