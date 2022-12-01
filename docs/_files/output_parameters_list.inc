.. _costs_for_co2_emission:

Costs for CO2 emission
^^^^^^^^^^^^^^^^^^^^^^

:Definition: Calculated costs for CO2 emission certificates (current and future) from inputs
:Unit: EUR
:Default: None
:Category: Financial
:Restrictions: nan

----

.. _lcoe:

LCOE
^^^^

:Definition: Levelized costs of energy
:Unit: EUR
:Default: None
:Category: Financial
:Restrictions: 0 or above

----

.. _emissions_co2eq:

Emissions CO2eq
^^^^^^^^^^^^^^^

:Definition: Emissions of CO2eq  (gCO2eq/kWh, TCO2eq emitted)
:Unit: T of CO2eq
:Default: None
:Category: Environmental
:Restrictions: 0 or above

----

.. _relative_emissions_co2eq:

Relative emissions CO2eq
^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Emissions of CO2eq relative to another scenario (% reduced emissions compared to another scenario. E.g: BAU)
:Unit: Percentage
:Default: None
:Category: Environmental
:Restrictions: 0 or above

----

.. _investment_needed:

Investment needed
^^^^^^^^^^^^^^^^^

:Definition: Total investment needed
:Unit: EUR
:Default: None
:Category: Financial
:Restrictions: 0 or above

----

.. _degree_of_sector-coupling:

Degree of sector-coupling
^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: A synergy index of the energy system expressed via the DOA defined in a publication of RLI
:Unit: factor
:Default: None
:Category: KPI
:Restrictions: between 0 and 1

----

.. _degree_of_autonomy_(da):

Degree of Autonomy (DA)
^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Degree of Autonomy or self sufficiency obtained, typically a number between 0 and 1
:Unit: factor
:Default: None
:Category: KPI
:Restrictions: between 0 and 1

----

.. _transformation_pathway:

Transformation pathway
^^^^^^^^^^^^^^^^^^^^^^

:Definition: Enable the user to carry out this analysis on how to get from current situation to future situation from the other outputs. The pathway itself shall not be output by the simulation as it depends on policies and human political decisions as well
:Unit: None
:Default: nan
:Category: Report
:Restrictions: nan

----

.. _scenarios_comparisons:

Scenarios comparisons
^^^^^^^^^^^^^^^^^^^^^

:Definition: Comparison of different energy systems  and energy mixs (like RLI stemp-mv tool). Could compare energy savings, costs savings, CO2 savings
:Unit: None
:Default: nan
:Category: Report
:Restrictions: nan

----

.. _energy_mix:

Energy mix
^^^^^^^^^^

:Definition: Percentage of each asset for each energy type.
:Unit: Percentage
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _renewable_energy_share:

Renewable energy share
^^^^^^^^^^^^^^^^^^^^^^

:Definition: The share of renewable energy produced in the output energy mix
:Unit: Percentage
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _wasted_energy:

Wasted energy
^^^^^^^^^^^^^

:Definition: Energy which could not be stored, or was lost in Joule effect (heating), i.e. losses in heat boilers
:Unit: kW
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _installed__capacity:

Installed  capacity
^^^^^^^^^^^^^^^^^^^

:Definition: The minimal capacity that needs to be installed in order to meet peak demand
:Unit: kW
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _installed_power:

Installed power
^^^^^^^^^^^^^^^

:Definition: The aggregated power that needs to be produced in order to meet demand
:Unit: kWh
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _calculate_network_requirements_or_expansion_possibilities:

Calculate network requirements or expansion possibilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Calculate network requirements or expansion possibilities
:Unit: None
:Default: nan
:Category: Report
:Restrictions: nan

----

.. _grid_equipment_requirements:

Grid equipment requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Number of new transformers (v2.0 of the tool)
:Unit: nan
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _grid_cable_requirements:

Grid cable requirements
^^^^^^^^^^^^^^^^^^^^^^^

:Definition: length and size of new cables required (v2.0 of the tool)
:Unit: km
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _available_generation_technologies:

Available generation technologies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: List of existing technologies which could fulfill the capacity without exceeding the costs
:Unit: None
:Default: nan
:Category: Report
:Restrictions: nan

----

.. _required_storage:

Required storage
^^^^^^^^^^^^^^^^

:Definition: Required size to sustain peak demands for each storage technology (only if storage is part of input)
:Unit: kW
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _connection_points:

Connection points
^^^^^^^^^^^^^^^^^

:Definition: Transfer interfaces with existing supply structures (gas/electricity/water/wastewater)
:Unit: None
:Default: nan
:Category: Report
:Restrictions: nan

----

.. _amortisation_period_of_system_improvements:

Amortisation period of system improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: How many months/years should one wait to get back the money invested in the components/assets
:Unit: Time
:Default: None
:Category: Financial
:Restrictions: 0 or above

----

.. _list_of_support_programmes:

List of support programmes
^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: List of support programmes (government, NGO, World Bank) which criteria are fulfilled by the output energy system
:Unit: None
:Default: nan
:Category: Report
:Restrictions: nan