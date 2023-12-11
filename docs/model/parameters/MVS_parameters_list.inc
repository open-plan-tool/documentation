.. _age_ins-label:

age_installed
^^^^^^^^^^^^^

:Definition_Short: Number of years the asset has already been in operation
:Definition_Long: If the project lasts longer than its remaining lifetime, the replacement costs of the asset will be taken into account.
:Type: numeric
:Unit: a
:Example: 10
:Restrictions: Natural number
:Default: 0

This parameter is used within the following categories: :ref:`conversion:production`


.. _crate-label:

c-rate
^^^^^^

:Definition_Short: Maximum permissable power at which the storage can be charged or discharged relative to the nominal capacity of the storage
:Definition_Long: The C rate indicates the reciprocal of the time for which a battery of the specified capacity can be charged or discharged with the maximum charge or discharge current. A C-rate of 1 implies that the battery can be fully charged or discharged completely in a single timestep. A C-rate of 0.5 implies that the battery needs at least 2 timesteps to be fully charged or discharged.
:Type: numeric
:Unit: Factor
:Example: 1
:Restrictions: Real number between 0 and 1
:Default: 1

This parameter is used within the following categories: :ref:`storage_csv`


.. _country-label:

country
^^^^^^^

:Definition_Short: Name of the country where the project is being deployed
:Type: str
:Unit: None
:Example: Norway
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _currency-label:

currency
^^^^^^^^

:Definition_Short: The currency of the country where the project is implemented
:Type: str
:Unit: None
:Example: EUR
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`economic_data`


.. _developmentcosts-label:

development_costs
^^^^^^^^^^^^^^^^^

:Definition_Short: Planning and development costs
:Definition_Long: This could be planning and development costs which do not depend on the (optimized) capacities of the assets.
:Type: numeric
:Unit: €
:Example: 10000
:Restrictions: Positive real number
:Default: 0

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`storage_csv`


.. _discountfactor-label:

discount_factor
^^^^^^^^^^^^^^^

:Definition_Short: The factor which accounts for the depreciation in the value of money in the future compared to the current value of the same money
:Definition_Long: The common method is to calculate the weighted average cost of capital (WACC) and use it as the discount rate.
:Type: numeric
:Unit: Factor
:Example: 0.06
:Restrictions: Real number
:Default: 0.05

This parameter is used within the following categories: :ref:`economic_data`


.. _dispatchprice-label:

dispatch_price
^^^^^^^^^^^^^^

:Definition_Short: Costs associated with a flow through/from the asset (OPEX_var or fuel costs)
:Definition_Long: This could be fuel costs for fuel sources like biogas or oil or operational costs for thermal power plants which only occur when operating the plant.
:Type: numeric
:Unit: €/kWh
:Example: 0.01
:Restrictions: None
:Default: 0.01

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`storage_csv`


.. _efficiency-label:

efficiency
^^^^^^^^^^

:Definition_Short: Ratio of energy output to energy input
:Definition_Long: The battery efficiency is the ratio of the energy taken out from the battery to the energy put into the battery.
:Type: numeric
:Unit: Factor
:Example: 0.95
:Restrictions: Positive real number
:Default: 0.8

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`storage_csv`


.. _emissionfactor-label:

emission_factor
^^^^^^^^^^^^^^^

:Definition_Short: Emissions per unit dispatch of an asset
:Type: numeric
:Unit: kgCO2eq/asset unit
:Example: 14.4
:Restrictions: Positive real number
:Default: 0.4

This parameter is used within the following categories: :ref:`providers`


See also: :ref:`production`


.. _energyprice-label:

energy_price
^^^^^^^^^^^^

:Definition_Short: Price of the energy carrier sourced from the utility grid
:Definition_Long: Can be also a timeseries
:Type: numeric
:Unit: €/kWh
:Example: 0.3
:Restrictions: None
:Default: 0.3

This parameter is used within the following categories: :ref:`providers`


.. _energyvector-label:

energyVector
^^^^^^^^^^^^

:Definition_Short: Energy commodity
:Definition_Long: Convention: For an energy conversion asset define the commodity of the output. For a sink define the commodity based on the input flow. For a source define the commodity based on the output flow. For a storage, define the commodity based on the stored energy carrier.
:Type: str
:Unit: None
:Example: Electricity
:Restrictions: One of “Electricity”, “Gas”, “Bio-Gas”, “Diesel”, “Heat”, “H2”
:Default: Electricity

This parameter is used within the following categories: :ref:`busses`


See also: :ref:`consumption`


.. _evaluatedperiod-label:

evaluated_period
^^^^^^^^^^^^^^^^

:Definition_Short: The number of days for which the simulation is to be run
:Type: numeric
:Unit: None
:Example: 365
:Restrictions: Natural number
:Default: 365

This parameter is used within the following categories: :ref:`simulation_settings`


.. _feedincap-label:

feedin_cap
^^^^^^^^^^

:Definition_Short: Maximum capacity for feeding electricity into the grid
:Type: numeric
:Unit: :unit:
:Example: 1000
:Restrictions: Acceptable values are either a positive real number or None
:Default: None

This parameter is used within the following categories: :ref:`providers`


.. _feedintariff-label:

feedin_tariff
^^^^^^^^^^^^^

:Definition_Short: Price received for feeding electricity into the grid
:Definition_Long: Can be also a timeseries
:Type: numeric
:Unit: €/kWh
:Example: 0.1
:Restrictions: None
:Default: 0.1

This parameter is used within the following categories: :ref:`providers`


.. _filename-label:

file_name
^^^^^^^^^

:Definition_Short: Name of the csv file containing the input generation or demand timeseries
:Type: str
:Unit: None
:Example: demand_harbor.csv
:Restrictions: This file must be placed in a folder named “time_series” inside your input folder.
:Default: None

This parameter is used within the following categories: :ref:`consumption`


See also: :ref:`production`


.. _fixed_thermal_losses_absolute-label:

fixed_thermal_losses_absolute
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition_Short: Thermal losses of the storage independent of the state of charge and independent of nominal storage capacity between two consecutive timesteps
:Type: numeric
:Unit: factor
:Example: 0.0003
:Restrictions: Between 0 and 1
:Default: 0

This parameter is used within the following categories: :ref:`storage_csv`


.. _fixed_thermal_losses_relative-label:

fixed_thermal_losses_relative
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition_Short: Thermal losses of storage independent of state of charge between two consecutive timesteps relative to nominal storage capacity
:Type: numeric
:Unit: factor
:Example: 0.0016
:Restrictions: Between 0 and 1
:Default: 0

This parameter is used within the following categories: :ref:`storage_csv`


.. _inflowdirection-label:

inflow_direction
^^^^^^^^^^^^^^^^

:Definition_Short: Label of the bus/component from which the energyVector is arriving into the asset
:Type: str
:Unit: None
:Example: Electricity
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`consumption`


See also: :ref:`conversion`


.. _installedcap-label:

installedCap
^^^^^^^^^^^^

:Definition_Short: Already existing installed capacity
:Definition_Long: If the project lasts longer than its remaining lifetime, the replacement costs of the asset will be taken into account.
:Type: numeric
:Unit: :unit:
:Example: 50
:Restrictions: None
:Default: 0

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`production`


.. _labl-label:

label
^^^^^

:Definition_Short: Name of the asset
:Type: str
:Unit: None
:Example: pv_plant_01
:Restrictions: Input the names in a computer friendly format, preferably with underscores instead of spaces, and avoiding special characters
:Default: None

This parameter is used within the following categories: :ref:`fixcost`


.. _latitude-label:

latitude
^^^^^^^^

:Definition_Short: Latitude coordinate of the project's geographical location
:Type: numeric
:Unit: None
:Example: 45.641603
:Restrictions: Should follow geographical convention
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _lifetime-label:

lifetime
^^^^^^^^

:Definition_Short: Number of operational years of the asset until it has to be replaced
:Type: numeric
:Unit: a
:Example: 20
:Restrictions: Natural number
:Default: 20

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`storage_csv`


.. _longitude-label:

longitude
^^^^^^^^^

:Definition_Short: Longitude coordinate of the project's geographical location
:Type: numeric
:Unit: None
:Example: 10.95787
:Restrictions: Should follow geographical convention
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _maxemissions-label:

maximum_emissions
^^^^^^^^^^^^^^^^^

:Definition_Short: Maximum amount of total emissions which are allowed in the optimized energy system
:Type: numeric
:Unit: kgCO2eq/a
:Example: 100000
:Restrictions: Acceptable values are either a positive real number or None.
:Default: None

This parameter is used within the following categories: :ref:`constraints`


.. _maxcap-label:

maximumCap
^^^^^^^^^^

:Definition_Short: Maximum total capacity of an asset that can be installed at the project site
:Definition_Long: This includes the already existing installed and additional capacity possible. An example would be that a roof can only carry 50 kW PV (maximum capacity), whereas the installed capacity is already 10 kW. The optimization would only be allowed to add 40 kW PV at maximum.
:Type: numeric
:Unit: :unit:
:Example: 1000
:Restrictions: Acceptable values are either a positive real number or None.
:Default: None

This parameter is used within the following categories: :ref:`production`, :ref:`storage`


.. _minda-label:

minimal_degree_of_autonomy
^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition_Short: Minimum degree of autonomy that needs to be met by the optimization
:Definition_Long: This constraint defines a lower bound on the <a href='https://open-plan-documentation.readthedocs.io/en/latest/model/simulation_outputs.html#degree-of-autonomy'>degree of autonomy</a> of the energy system. Note that constraint is applied to the the whole, sector-coupled energy system, but not to specific sectors individually.
:Type: numeric
:Unit: factor
:Example: 0.6
:Restrictions: Real number between 0 and 1
:Default: 0.6

This parameter is used within the following categories: :ref:`constraints`


.. _minrenshare-label:

minimal_renewable_factor
^^^^^^^^^^^^^^^^^^^^^^^^

:Definition_Short: Minimum share of energy supplied by renewable generation that needs to be met by the optimization
:Definition_Long: This constraint defines a lower bound on the <a href='https://open-plan-documentation.readthedocs.io/en/latest/model/simulation_outputs.html#renewable-factor'>renewable share</a> of the system, which takes into account both local generation as well as the renewable share of energy providers. Note that constraint is applied to the renewable share of the whole, sector-coupled energy system, but not to specific sectors individually.
:Type: numeric
:Unit: factor
:Example: 0.8
:Restrictions: Real number between 0 and 1
:Default: 0.8

This parameter is used within the following categories: :ref:`constraints`


.. _nzeconstraint-label:

net_zero_energy
^^^^^^^^^^^^^^^

:Definition_Short: Specifies whether optimization needs to result into a net zero energy system (True) or not (False)
:Type: boolean
:Unit: None
:Example: True
:Restrictions: Acceptable values are either Yes or No.
:Default: False

This parameter is used within the following categories: :ref:`constraints`


.. _optimizecap-label:

optimizeCap
^^^^^^^^^^^

:Definition_Short: Choose if capacity optimization should be performed for this asset.
:Type: boolean
:Unit: None
:Example: True
:Restrictions: Acceptable values are either Yes or No.
:Default: False

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`storage`


.. _outflowdirec-label:

outflow_direction
^^^^^^^^^^^^^^^^^

:Definition_Short: Label of bus/component towards which the energyVector is leaving from the asset
:Type: str
:Unit: None
:Example: PV plant (mono)
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`consumption`


See also: :ref:`conversion`


.. _outputlpfile-label:

output_lp_file
^^^^^^^^^^^^^^

:Definition_Short: Enables the output of the linear programming (lp) file with the linear equation system describing the optimization problem
:Definition_Long: The lp file contains the objective function and all constraints. It enables the user to look at the underlying equations of the optimization.
:Type: boolean
:Unit: None
:Example: False
:Restrictions: Acceptable values are either True or False
:Default: False

This parameter is used within the following categories: :ref:`simulation_settings`


.. _peakdemand-label:

peak_demand_pricing
^^^^^^^^^^^^^^^^^^^

:Definition_Short: Grid fee to be paid based on the peak demand of a given period
:Type: numeric
:Unit: €/kW
:Example: 60
:Restrictions: None
:Default: 0

This parameter is used within the following categories: :ref:`providers`


See also: :ref:`peakdemandperiod-label`


.. _peakdemandperiod-label:

peak_demand_pricing_period
^^^^^^^^^^^^^^^^^^^^^^^^^^

:Definition_Short: Number of reference periods in one year for the peak demand pricing
:Type: numeric
:Unit: times per year
:Example: 2
:Restrictions: Only one of the following are acceptable values: 1 (yearly), 2, 3 ,4, 6, 12 (monthly)
:Default: 1

This parameter is used within the following categories: :ref:`providers`


See also: :ref:`peakdemand-label`


.. _projectduration-label:

project_duration
^^^^^^^^^^^^^^^^

:Definition_Short: The number of years the project is intended to be operational
:Definition_Long: The project duration also sets the installation time of the assets used in the simulation. After the project ends these assets are 'sold' and the refund is charged against the initial investment costs.
:Type: numeric
:Unit: a
:Example: 30
:Restrictions: Natural number
:Default: 20

This parameter is used within the following categories: :ref:`economic_data`


.. _projectid-label:

project_id
^^^^^^^^^^

:Definition_Short: Assign a project ID as per your preference.
:Type: str
:Unit: None
:Example: 1
:Restrictions: Cannot be the same as an already existing project ID
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _projectname-label:

project_name
^^^^^^^^^^^^

:Definition_Short: Assign a project name as per your preference.
:Type: str
:Unit: None
:Example: Borg Havn
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _renshare-label:

renewable_share
^^^^^^^^^^^^^^^

:Definition_Short: Share of renewables in the generation mix of the energy supplied by the DSO utility
:Type: numeric
:Unit: Factor
:Example: 0.5
:Restrictions: Real number between 0 and 1
:Default: 0.44

This parameter is used within the following categories: :ref:`providers`


.. _renewableasset-label:

renewableAsset
^^^^^^^^^^^^^^

:Definition_Short: Choose if this asset should be considered as renewable.
:Definition_Long: This parameter is necessary to consider the renewable share constraint correctly.
:Type: boolean
:Unit: None
:Example: True
:Restrictions: Acceptable values are either Yes or No.
:Default: True

This parameter is used within the following categories: :ref:`production`


.. _scenariodescription-label:

scenario_description
^^^^^^^^^^^^^^^^^^^^

:Definition_Short: Brief description of the scenario being simulated
:Type: str
:Unit: None
:Example: This scenario simulates a sector-coupled energy system
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _scenarioid-label:

scenario_id
^^^^^^^^^^^

:Definition_Short: Assign a scenario ID as per your preference.
:Type: str
:Unit: None
:Example: 1
:Restrictions: Cannot be the same as an already existing scenario ID within the project
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _scenarioname-label:

scenario_name
^^^^^^^^^^^^^

:Definition_Short: Assign a scenario name as per your preference.
:Type: str
:Unit: None
:Example: Warehouse 14
:Restrictions: None
:Default: None

This parameter is used within the following categories: :ref:`project_data`


.. _socin-label:

soc_initial
^^^^^^^^^^^

:Definition_Short: State of charge of the storage in the zeroth time step
:Definition_Long: The state of charge is specified as a factor of the nominal capacity.
:Type: numeric
:Unit: None or factor
:Example: nan
:Restrictions: nan
:Default: None

This parameter is used within the following categories: :ref:`storage_csv`


.. _socmax-label:

soc_max
^^^^^^^

:Definition_Short: The maximum permissible level of charge of the storage as a factor of the nominal capacity
:Definition_Long: When the battery is filled to its nominal capacity the state of charge is represented by the value 1.
:Type: numeric
:Unit: Factor
:Example: nan
:Restrictions: Real number between 0 and 1
:Default: 1

This parameter is used within the following categories: :ref:`storage_csv`


.. _socmin-label:

soc_min
^^^^^^^

:Definition_Short: The minimum permissible level of charge of the storage as a factor of the nominal capacity
:Definition_Long: When the battery is fully discharged the state of charge is represented by the value 0.
:Type: numeric
:Unit: Factor
:Example: nan
:Restrictions: Real number between 0 and 1
:Default: 0

This parameter is used within the following categories: :ref:`storage_csv`


.. _specificcosts-label:

specific_costs
^^^^^^^^^^^^^^

:Definition_Short: Specific investment costs of the asset related to the installed capacity (CAPEX)
:Type: numeric
:Unit: €/:unit:
:Example: 1000
:Restrictions: None
:Default: 1000

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`storage_csv`


.. _specificomcosts-label:

specific_costs_om
^^^^^^^^^^^^^^^^^

:Definition_Short: Specific operational and maintenance costs of the asset related to the installed capacity (OPEX_fix)
:Type: numeric
:Unit: €/(:unit:*a)
:Example: 10
:Restrictions: None
:Default: 10

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`storage_csv`


.. _startdate-label:

start_date
^^^^^^^^^^

:Definition_Short: Date and time when the simulation starts with the first step
:Definition_Long: This date will be used for the results graphs as well as the timeseries upload.
:Type: str
:Unit: None
:Example: 2018-01-01 00:00:00
:Restrictions: Acceptable format is YYYY-MM-DD HH:MM:SS
:Default: None

This parameter is used within the following categories: :ref:`simulation_settings`


.. _storagefilename-label:

storage_filename
^^^^^^^^^^^^^^^^

:Definition_Short: Name of a csv file containing the properties of a storage component
:Type: str
:Unit: None
:Example: storage_01.csv
:Restrictions: Follows the convention of 'storage_xx.csv' where 'xx' is a number. This file must be placed in a folder named “csv_elements” inside your input folder.
:Default: None

This parameter is used within the following categories: :ref:`storage`


.. _tax-label:

tax
^^^

:Definition_Short: Tax factor
:Type: numeric
:Unit: Factor
:Example: 0
:Restrictions: Between 0 and 1
:Default: 0

This parameter is used within the following categories: :ref:`economic_data`


.. _timestep-label:

timestep
^^^^^^^^

:Definition_Short: Length of the time steps
:Type: numeric
:Unit: None
:Example: 60
:Restrictions: Can only be 60 minutes at the moment
:Default: 60

This parameter is used within the following categories: :ref:`simulation_settings`


.. _typeoemof-label:

type_oemof
^^^^^^^^^^

:Definition_Short: Input the type of OEMOF component
:Definition_Long: A photovoltaic plant would be a source, a solar inverter would be a transformer, etc. The `type_oemof` will later on be determined through the EPA.
:Type: str
:Unit: None
:Example: sink
:Restrictions: *sink* or *source* or one of the other component classes of OEMOF.
:Default: None

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`storage`


.. _unit-label:

unit
^^^^

:Definition_Short: Unit associated with the capacity of the component
:Type: str
:Unit: nan
:Example: Storage could have units like kW or kWh, transformer station could have kVA, and so on.
:Restrictions: Appropriate scientific unit
:Default: kW

This parameter is used within the following categories: :ref:`conversion`


See also: :ref:`storage_csv`


.. _Beta-label:

beta
^^^^

:Definition_Short: Power loss index for CHPs, usually known as beta coefficient
:Definition_Long: 0.6
:Type: factor
:Unit: beta
:Example: Between 0 and 1
:Restrictions: numeric
:Default: 0

This parameter is used within the following categories: :ref:`conversion`

