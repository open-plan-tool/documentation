.. _age_ins-label:

age_installed
^^^^^^^^^^^^^

:Definition: The number of years the asset has already been in operation.
:Type: numeric
:Unit: Year
:Example: 10
:Restrictions: Natural number
:Default: None

This parameter is used within the following categories: :ref:`conversion`, :ref:`production`


.. _crate-label:

c-rate
^^^^^^

:Definition: C-rate is the rate at which the storage can charge or discharge relative to the nominal capacity of the storage. A c-rate of 1 implies that the battery can discharge or charge completely in a single timestep.
:Type: numeric
:Unit: Factor
:Example: *storage capacity*: NaN, *input power*: 1, *output power*: 1
:Restrictions: Real number between 0 and 1. Only the columns "input power" and "output power" require a value, in column "storage capacity" c_rate should be set to NaN.
:Default: None

This parameter is used within the following categories: :ref:`storage_csv`


.. _country-label:

country
^^^^^^^

:Definition: Name of the country where the project is being deployed
:Type: str
:Unit: None
:Example: Norway
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _currency-label:

currency
^^^^^^^^

:Definition: The currency of the country where the project is implemented.
:Type: str
:Unit: None
:Example: EUR
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`economic_data`


.. _developmentcosts-label:

development_costs
^^^^^^^^^^^^^^^^^

:Definition: A fixed cost to implement the asset, eg. planning costs which do not depend on the (optimized) asset capacity.
:Type: numeric
:Unit: currency
:Example: 10000
:Restrictions: Positive real number
:Default: None

This parameter is used within the following categories: :ref:`conversion`, :ref:`storage_csv`, :ref:`production`, :ref:`fixcost`


.. _discountfactor-label:

discount_factor
^^^^^^^^^^^^^^^

:Definition: Discount factor is the factor which accounts for the depreciation in the value of money in the future, compared to the current value of the same money. The common method is to calculate the weighted average cost of capital (WACC) and use it as the discount rate.
:Type: numeric
:Unit: Factor
:Example: 0.06
:Restrictions: Between 0 and 1
:Default: None

This parameter is used within the following categories: :ref:`economic_data`


.. _dispatchprice-label:

dispatch_price
^^^^^^^^^^^^^^

:Definition: Variable cost associated with a flow through/from the asset (eg. Euro/kWh).
:Type: numeric
:Unit: currency/kWh
:Example: 0.64
:Restrictions: In "storage_xx.csv" only the columns "input power" and "output power" require a value, in column "storage capacity" dispatch_price should be set to NaN.
:Default: None

This parameter is used within the following categories: :ref:`conversion`, :ref:`production`, :ref:`storage_csv`, :ref:`fixcost`


.. _efficiency-label:

efficiency
^^^^^^^^^^

:Definition: Ratio of energy output/energy input. The battery efficiency is the ratio of the energy taken out from the battery, to the energy put into the battery. It means that it is not possible to retrieve as much energy as provided to the battery due to the discharge losses. The efficiency of the "input power" and "ouput power" columns should be set equal to the charge and dischage efficiencies respectively, while the "storage capacity" efficiency should be equal to the storage's efficiency/ability to hold charge over time (`= 1 - self-discharge/decay`), which is usually in the range of 0.95 to 1 for electrical storages.
:Type: numeric
:Unit: Factor
:Example: 0.95
:Restrictions: Between 0 and 1
:Default: None

This parameter is used within the following categories: :ref:`conversion`, :ref:`storage_csv`


.. _emissionfactor-label:

emission_factor
^^^^^^^^^^^^^^^

:Definition: Emissions per unit dispatch of an asset.
:Type: numeric
:Unit: kgCO2eq/asset unit
:Example: 14.4
:Restrictions: Positive real number
:Default: None

This parameter is used within the following categories: :ref:`providers`, :ref:`production`


.. _energyprice-label:

energy_price
^^^^^^^^^^^^

:Definition: Price of energy carrier sourced from the utility grid.
:Type: numeric
:Unit: currency/energy carrier unit
:Example: 0.1
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`providers`


.. _energyvector-label:

energyVector
^^^^^^^^^^^^

:Definition: Energy vector/commodity. Convention: For an energy conversion asset define energyVector of the output. For a sink define based on inflow. For a source define based on output flow. For a storage, define based on stored energy carrier.
:Type: str
:Unit: None
:Example: Electricity
:Restrictions: One of “Electricity”, “Gas”, “Bio-Gas”, “Diesel”, “Heat”, “H2”
:Default: None

This parameter is used within the following categories: :ref:`busses`, :ref:`consumption`, :ref:`production`, :ref:`storage`, :ref:`providers`, :ref:`conversion`


.. _evaluatedperiod-label:

evaluated_period
^^^^^^^^^^^^^^^^

:Definition: The number of days simulated with the energy system model.
:Type: numeric
:Unit: Day
:Example: 365
:Restrictions: Natural number
:Default: None

This parameter is used within the following categories: :ref:`simulation_settings`


.. _feedintariff-label:

feedin_tariff
^^^^^^^^^^^^^

:Definition: Price received for feeding electricity into the grid.
:Type: numeric
:Unit: currency/kWh
:Example: 0.7
:Restrictions: Real number between 0 and 1
:Default: None

This parameter is used within the following categories: :ref:`providers`


.. _filename-label:

file_name
^^^^^^^^^

:Definition: Name of a csv file containing the input generation or demand timeseries.
:Type: str
:Unit: None
:Example: demand_harbor.csv
:Restrictions: This file must be placed in a folder named “time_series” inside your input folder.
:Default: None

This parameter is used within the following categories: :ref:`consumption`, :ref:`production`, :ref:`storage`


.. _fixed_thermal_losses_absolute-label:

fixed_thermal_losses_absolute
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Thermal losses of storage independent of state of charge and independent of nominal storage capacity between two consecutive timesteps.
:Type: numeric
:Unit: factor
:Example: 0.0003
:Restrictions: Between 0 and 1
:Default: 0

This parameter is used within the following categories: :ref:`storage_csv`


.. _fixed_thermal_losses_relative-label:

fixed_thermal_losses_relative
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Thermal losses of storage independent of state of charge between two consecutive timesteps relative to nominal storage capacity.
:Type: numeric
:Unit: factor
:Example: 0.0016
:Restrictions: Between 0 and 1
:Default: 0

This parameter is used within the following categories: :ref:`storage_csv`


.. _inflowdirection-label:

inflow_direction
^^^^^^^^^^^^^^^^

:Definition: The label of the bus/component from which the energyVector is arriving into the asset.
:Type: str
:Unit: None
:Example: Electricity
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`consumption`, :ref:`conversion`, :ref:`providers`, :ref:`storage`


.. _installedcap-label:

installedCap
^^^^^^^^^^^^

:Definition: The already existing installed capacity in-place. If the project lasts longer than its remaining lifetime, its replacement costs will be taken into account.
:Type: numeric
:Unit: kWp
:Example: 50
:Restrictions: Each component in the “energy production” category must have a value.
:Default: None

This parameter is used within the following categories: :ref:`conversion`, :ref:`production`, :ref:`storage_csv`


.. _labl-label:

label
^^^^^

:Definition: Name of the asset for display purposes
:Type: str
:Unit: None
:Example: pv_plant_01
:Restrictions: Input the names in a computer friendly format, preferably with underscores instead of spaces, and avoiding special characters
:Default: None

This parameter is used within the following categories: :ref:`fixcost`


.. _latitude-label:

latitude
^^^^^^^^

:Definition: Latitude coordinate of the project's geographical location.
:Type: numeric
:Unit: None
:Example: 45.641603
:Restrictions: Should follow geographical convention
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _lifetime-label:

lifetime
^^^^^^^^

:Definition: Number of operational years of the asset until it has to be replaced.
:Type: numeric
:Unit: Year
:Example: 30
:Restrictions: Natural number
:Default: None

This parameter is used within the following categories: :ref:`conversion`, :ref:`production`, :ref:`storage_csv`, :ref:`fixcost`


.. _longitude-label:

longitude
^^^^^^^^^

:Definition: Longitude coordinate of the project's geographical location.
:Type: numeric
:Unit: None
:Example: 10.95787
:Restrictions: Should follow geographical convention
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _maxemissions-label:

maximum_emissions
^^^^^^^^^^^^^^^^^

:Definition: The maximum amount of total emissions in the optimized energy system.
:Type: numeric
:Unit: kgCO2eq/a
:Example: 100000
:Restrictions: Acceptable values are either a positive real number or None
:Default: None

This parameter is used within the following categories: :ref:`constraints`


.. _maxcap-label:

maximumCap
^^^^^^^^^^

:Definition: The maximum total capacity of an asset that can be installed at the project site. This includes the installed and the also the maximum additional capacity possible. An example would be that a roof can only carry 50 kWp PV (maximumCap), whereas the installed capacity is already 10 kWp. The optimization would only be allowed to add 40 kWp PV at maximum.
:Type: numeric
:Unit: kWp
:Example: 1050
:Restrictions: Acceptable values are either a positive real number or None
:Default: None

This parameter is used within the following categories: :ref:`production`


.. _minda-label:

minimal_degree_of_autonomy
^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: The minimal degree of autonomy that needs to be met by the optimization.
:Type: numeric
:Unit: factor
:Example: 0.3
:Restrictions: Between 0 and 1
:Default: None

This parameter is used within the following categories: :ref:`constraints`


.. _minrenshare-label:

minimal_renewable_factor
^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: The minimum share of energy supplied by renewable generation in the optimized energy system. Insert the value 0 to deactivate this constraint.
:Type: numeric
:Unit: factor
:Example: 0.7
:Restrictions: Between 0 and 1
:Default: None

This parameter is used within the following categories: :ref:`constraints`


.. _nzeconstraint-label:

net_zero_energy
^^^^^^^^^^^^^^^

:Definition: Specifies whether optimization needs to result into a net zero energy system (True) or not (False).
:Type: boolean
:Unit: None
:Example: True
:Restrictions: Acceptable values are either True or False.
:Default: False

This parameter is used within the following categories: :ref:`constraints`


.. _optimizecap-label:

optimizeCap
^^^^^^^^^^^

:Definition: Allow the user to perform capacity optimization for an asset.
:Type: boolean
:Unit: None
:Example: True
:Restrictions: Permissible values are either True or False
:Default: None

This parameter is used within the following categories: :ref:`conversion`, :ref:`production`, :ref:`providers`, :ref:`storage`


.. _outflowdirec-label:

outflow_direction
^^^^^^^^^^^^^^^^^

:Definition: The label of bus/component towards which the energyVector is leaving from the asset.
:Type: str
:Unit: None
:Example: PV plant (mono)
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`consumption`, :ref:`conversion`, :ref:`providers`, :ref:`storage`


.. _outputlpfile-label:

output_lp_file
^^^^^^^^^^^^^^

:Definition: Enable the generation of a file with the linear equation system describing the simulation, ie., with the objective function and all the constraints. This lp file enables the user look at the underlying equations of the optimization.
:Type: boolean
:Unit: None
:Example: False
:Restrictions: Acceptable values are either True or False
:Default: None

This parameter is used within the following categories: :ref:`simulation_settings`


.. _peakdemand-label:

peak_demand_pricing
^^^^^^^^^^^^^^^^^^^

:Definition: Price to be paid additionally for energy-consumption based on the peak demand of a given period.
:Type: numeric
:Unit: currency/kW
:Example: 60
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`providers`


See also: :ref:`peakdemandperiod-label`


.. _peakdemandperiod-label:

peak_demand_pricing_period
^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition: Number of reference periods in one year for the peak demand pricing.
:Type: numeric
:Unit: times per year (1,2,3,4,6,12)
:Example: 2
:Restrictions: Only one of the following are acceptable values: 1 (yearly), 2, 3 ,4, 6, 12 (monthly)
:Default: None

This parameter is used within the following categories: :ref:`providers`


See also: :ref:`peakdemand-label`


.. _projectduration-label:

project_duration
^^^^^^^^^^^^^^^^

:Definition: The number of years the project is intended to be operational. The project duration also sets the installation time of the assets used in the simulation. After the project ends these assets are 'sold' and the refund is charged against the initial investment costs.
:Type: numeric
:Unit: Years
:Example: 30
:Restrictions: Natural number
:Default: None

This parameter is used within the following categories: :ref:`economic_data`


.. _projectid-label:

project_id
^^^^^^^^^^

:Definition: Users can assign a project ID as per their preference.
:Type: str
:Unit: None
:Example: 1
:Restrictions: Cannot be the same as an already existing project
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _projectname-label:

project_name
^^^^^^^^^^^^

:Definition: Users can assign a project name as per their preference.
:Type: str
:Unit: None
:Example: Borg Havn
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _renshare-label:

renewable_share
^^^^^^^^^^^^^^^

:Definition: The share of renewables in the generation mix of the energy supplied by the DSO (utility).
:Type: numeric
:Unit: Factor
:Example: 0.1
:Restrictions: Real number between 0 and 1
:Default: None

This parameter is used within the following categories: :ref:`providers`


.. _renewableasset-label:

renewableAsset
^^^^^^^^^^^^^^

:Definition: Allow the user to tag as asset as renewable.
:Type: boolean
:Unit: None
:Example: True
:Restrictions: Acceptable values are either True or False
:Default: None

This parameter is used within the following categories: :ref:`production`


.. _scenariodescription-label:

scenario_description
^^^^^^^^^^^^^^^^^^^^

:Definition: Brief description of the scenario being simulated.
:Type: str
:Unit: None
:Example: This scenario simulates a sector-coupled energy system
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _scenarioid-label:

scenario_id
^^^^^^^^^^^

:Definition: Users can assign a scenario id as per their preference.
:Type: str
:Unit: None
:Example: 1
:Restrictions: Cannot be the same as an already existing scenario within the project
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _scenarioname-label:

scenario_name
^^^^^^^^^^^^^

:Definition: Users can assign a scenario name as per their preference.
:Type: str
:Unit: None
:Example: Warehouse 14
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _socin-label:

soc_initial
^^^^^^^^^^^

:Definition: The level of charge (as a factor of the actual capacity) in the storage in the zeroth time-step.
:Type: numeric
:Unit: None or factor
:Example: :code:`storage capacity`: None, :code:`input power`: NaN, :code:`output power`: NaN
:Restrictions: Acceptable values are either None or the factor. Only the column :code:`storage capacity` requires a value, in column :code:`input power` and :code:`output power` :code:`soc_initial` should be set to NaN. The :code:`soc_initial` has to be within the [0,1] interval.
:Default: None

This parameter is used within the following categories: :ref:`storage_csv`


.. _socmax-label:

soc_max
^^^^^^^

:Definition: The maximum permissible level of charge in the battery (generally, it is when the battery is filled to its nominal capacity), represented by the value 1.0. Users can  also specify a certain value as a factor of the actual capacity.
:Type: numeric
:Unit: Factor
:Example: :code:`storage capacity`: 1, :code:`input power`: NaN, :code:`output power`: NaN
:Restrictions: Only the column :code:`storage capacity` requires a value, in column :code:`input power` and :code:`output power` :code:`soc_max` should be set to NaN. The :code:`soc_max` has to be in the [0,1] interval.
:Default: None

This parameter is used within the following categories: :ref:`storage_csv`


.. _socmin-label:

soc_min
^^^^^^^

:Definition: The minimum permissible level of charge in the battery as a factor of the nominal capacity of the battery.
:Type: numeric
:Unit: Factor
:Example: :code:`storage capacity`:0.2, :code:`input power`: NaN, :code:`output power`: NaN
:Restrictions: Only the column :code:`storage capacity` requires a value, in column :code:`input power` and :code:`output power` :code:`soc_min` should be set to NaN. The soc_min has to be in the [0,1] interval.
:Default: None

This parameter is used within the following categories: :ref:`storage_csv`


.. _specificcosts-label:

specific_costs
^^^^^^^^^^^^^^

:Definition: Actual CAPEX of an asset, i.e., specific investment costs
:Type: numeric
:Unit: currency/unit
:Example: 4000
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`conversion`, :ref:`production`, :ref:`storage_csv`, :ref:`fixcost`


.. _specificomcosts-label:

specific_costs_om
^^^^^^^^^^^^^^^^^

:Definition: Actual OPEX of an asset, i.e., specific operational and maintenance costs.
:Type: numeric
:Unit: currency/unit/year
:Example: 120
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`conversion`, :ref:`production`, :ref:`storage_csv`, :ref:`fixcost`


.. _startdate-label:

start_date
^^^^^^^^^^

:Definition: The data and time on which the simulation starts at the first step.
:Type: str
:Unit: None
:Example: 2018-01-01 00:00:00
:Restrictions: Acceptable format is YYYY-MM-DD HH:MM:SS
:Default: None

This parameter is used within the following categories: :ref:`simulation_settings`


.. _storagefilename-label:

storage_filename
^^^^^^^^^^^^^^^^

:Definition: Name of a csv file containing the properties of a storage component
:Type: str
:Unit: None
:Example: storage_01.csv
:Restrictions: Follows the convention of 'storage_xx.csv' where 'xx' is a number. This file must be placed in a folder named “csv_elements” inside your input folder.
:Default: None

This parameter is used within the following categories: :ref:`storage`


.. _tax-label:

tax
^^^

:Definition: Tax factor.
:Type: numeric
:Unit: Factor
:Example: 0
:Restrictions: Between 0 and 1
:Default: None

This parameter is used within the following categories: :ref:`economic_data`


.. _timestep-label:

timestep
^^^^^^^^

:Definition: Length of the time-steps.
:Type: numeric
:Unit: Minutes
:Example: 60
:Restrictions: Can only be 60 at the moment
:Default: None

This parameter is used within the following categories: :ref:`simulation_settings`


.. _typeoemof-label:

type_oemof
^^^^^^^^^^

:Definition: Input the type of OEMOF component. For example, a PV plant would be a source, a solar inverter would be a transformer, etc.  The `type_oemof` will later on be determined through the EPA.
:Type: str
:Unit: None
:Example: sink
:Restrictions: *sink* or *source* or one of the other component classes of OEMOF.
:Default: None

This parameter is used within the following categories: :ref:`consumption`, :ref:`conversion`, :ref:`production`, :ref:`providers`, :ref:`storage`


.. _unit-label:

unit
^^^^

:Definition: Unit associated with the capacity of the component.
:Type: str
:Unit: nan
:Example: Storage could have units like kW or kWh, transformer station could have kVA, and so on.
:Restrictions: Appropriate scientific unit
:Default: None

This parameter is used within the following categories: :ref:`consumption`, :ref:`conversion`, :ref:`production`, :ref:`providers`, :ref:`storage_csv`

