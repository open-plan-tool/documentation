.. _demand_profile:

Demand profile
^^^^^^^^^^^^^^

:Definition: The energy demand time serie with timestep (if different energy types are considered different profiles must be given)
:Unit: nan
:Default: nan
:Category: Technical
:Restrictions: nan

----

.. _energy_timeseries:

Energy timeseries
^^^^^^^^^^^^^^^^^

:Definition: Specific timeseries of energy sources from a primary-secondary transformation (e.g. PV, Wind)
:Unit: kWh
:Default: nan
:Category: Technical
:Restrictions: between 0 and 1 (normalized with maximum)

----

.. _source_power_mix:

Source power mix
^^^^^^^^^^^^^^^^

:Definition: Percentage of each source of power (inclusive % from Grid)
:Unit: Percentage
:Default: nan
:Category: Technical
:Restrictions: nan

----

.. _lower_bound_renewable_energy_share_:

Lower bound renewable energy share 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: A constraint that specifies the lower bound on the share of renewable energies in the optimized output energy mix
:Unit: Percentage
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _co2_upper_limit:

CO2 upper limit
^^^^^^^^^^^^^^^

:Definition: A constraint that specifies an upper bound on the CO2 emissions
:Unit: T of CO2
:Default: None
:Category: Environmental
:Restrictions: nan

----

.. _energy_sources_capacities:

Energy sources capacities
^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Energy sources with their capacity open for optimization 
:Unit: kW
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _storage_units:

Storage units
^^^^^^^^^^^^^

:Definition: Energy storage units with their capacity and technology
:Unit: kW
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _existing_energy_source_infrastructure:

Existing energy source infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Existing energy infrastructure not up for optimization (with given capacities)
:Unit: kW
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _existing_energy_storage_infrastructure:

Existing energy storage infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Existing storage infrastructure not up for optimization (with given capacities)
:Unit: kW
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _gps_coordinates:

GPS coordinates
^^^^^^^^^^^^^^^

:Definition: GPS coordinate of the location, to retrieve the weather conditions in case of missing timeseries. Could be a point, a set of points, or a polygon
:Unit: nan
:Default: None
:Category: GIS
:Restrictions: nan

----

.. _grid_parameters_(v2.0_of_the_tool):

Grid parameters (v2.0 of the tool)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Grid parameters such as:  power, voltage, frequence, line length, line impedance, transformers, topology
:Unit: nan
:Default: None
:Category: Technical
:Restrictions: nan

----

.. _degree_of_autonomy_(da):

Degree of Autonomy (DA)
^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Degree of Autonomy or self sufficiency wished (capability of the system to sustain a certain part of the load)
:Unit: factor
:Default: None
:Category: Constraint
:Restrictions: between 0 and 1

----

.. _ it's always a matter of data:

Temporal resolution of simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Time step of the simulation. The user should be aware that a higher resolution require more data and can lead to longer simulation times (might be already in the provided timeseries)
:Unit: nan
:Default: nan
:Category: Time
:Restrictions: nan

----

.. _optimization_goal:

Optimization goal
^^^^^^^^^^^^^^^^^

:Definition: The quantities which govern the optimization (CO2, costs, renewable maximization in energy mix, degree of autonomy, multi-objectives)
:Unit: nan
:Default: None
:Category: Simulation
:Restrictions: nan

----

.. _maximum_investment_budget:

Maximum investment budget
^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Upper bound on the investment budget
:Unit: EUR
:Default: None
:Category: Financial
:Restrictions: nan

----

.. _current_price_of_co2_emission_certificates:

Current price of CO2 emission certificates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Current price of CO2 emission certificates
:Unit: EUR
:Default: nan
:Category: Financial
:Restrictions: nan

----

.. _future_price_estimates_for_co2_emission_certificates:

Future price estimates for CO2 emission certificates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Timeseries of future price  for CO2 emission certificates (values from the EU-ETS and DE-ETS)
:Unit: EUR
:Default: nan
:Category: Financial
:Restrictions: nan

----

.. _interest_rate:

Interest rate
^^^^^^^^^^^^^

:Definition: A guess of what the  interest rate will be in during the project lifetime. Could be provided as constant or timeseries.
:Unit: EUR
:Default: Value provided
:Category: Financial
:Restrictions: nan

----

.. _costs_of_replacement:

Costs of replacement
^^^^^^^^^^^^^^^^^^^^

:Definition: Costs of replacement/improvement of the current system components/assets
:Unit: EUR
:Default: Value provided for each accepted asset type
:Category: Financial
:Restrictions: nan

----

.. _grid_stability_fee:

Grid stability fee
^^^^^^^^^^^^^^^^^^

:Definition: Fee/payment for contribution to grid stability
:Unit: EUR
:Default: Value provided
:Category: Financial
:Restrictions: nan

----

.. _ it's always a matter of data :

Spatial resolution
^^^^^^^^^^^^^^^^^^

:Definition: Define the wished spatial resolution (it is wished that it can range from building up to districts)
:Unit: nan
:Default: nan
:Category: GIS
:Restrictions: nan

----

.. _new_power_plant_available_space:

New power plant available space
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Available space for new power plants (for PV installation for example)
:Unit: nan
:Default: nan
:Category: GIS
:Restrictions: nan

----

.. _consumer_requirements:

Consumer requirements
^^^^^^^^^^^^^^^^^^^^^

:Definition: consumer requirements such as a specific localisation and wished minimal load profile (e.g. in an industry park)
:Unit: nan
:Default: nan
:Category: GIS/Technical
:Restrictions: nan

----

.. _existing_grid_structure_(v2.0_of_the_tool):

Existing grid structure (v2.0 of the tool)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: GPS coordinates of current grid structure (lines and hubs)
:Unit: nan
:Default: nan
:Category: GIS/Technical
:Restrictions: nan

----

.. _future_grid_structure_(v2.0_of_the_tool):

Future grid structure (v2.0 of the tool)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: GPS coordinates of future grid structure (lines and hubs)
:Unit: nan
:Default: nan
:Category: GIS/Technical
:Restrictions: nan

----

.. _security_of_supply:

Security of supply
^^^^^^^^^^^^^^^^^^

:Definition:  e.g. existence of back-up system
:Unit: nan
:Default: nan
:Category: Technical
:Restrictions: nan

----

.. _balancing_ratio_for_anciliary_services:

Balancing ratio for anciliary services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Balancing ratio for ancilliary services (need a more precise definition as PF could not re-figure out what this means)
:Unit: nan
:Default: nan
:Category: Technical
:Restrictions: nan

----

.. _number_of_future_extra_users:

Number of future extra users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Number of future extra user in energy cell
:Unit: nan
:Default: nan
:Category: Technical
:Restrictions: nan

----

.. _load_types:

Load types
^^^^^^^^^^

:Definition: Designation of flexible and non-flexible loads in the load profile
:Unit: nan
:Default: nan
:Category: Technical
:Restrictions: nan

----

.. _costs_of_asset_use:

Costs of asset use
^^^^^^^^^^^^^^^^^^

:Definition: The price of a liter of diesel or a kWh from the grid
:Unit: EUR
:Default: Value provided
:Category: Financial
:Restrictions: nan

----

.. _project_lifetime:

Project lifetime
^^^^^^^^^^^^^^^^

:Definition: The lifetime of the project (simulation time)
:Unit: Time
:Default: nan
:Category: Simulation
:Restrictions: nan