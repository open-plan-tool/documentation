.. _constraints:

constraints.csv
^^^^^^^^^^^^^^^

The file `constraints.csv` includes the following parameter(s):

* :ref:`maxemissions-label`
* :ref:`minda-label`
* :ref:`minrenshare-label`
* :ref:`nzeconstraint-label`


.. _economic_data:

economic_data.csv
^^^^^^^^^^^^^^^^^

The file `economic_data.csv` includes all economic data that the simulation will use. This includes the following parameters:

* :ref:`currency-label`
* :ref:`discountfactor-label`
* :ref:`projectduration-label`
* :ref:`tax-label`


.. _busses:

energyBusses.csv
^^^^^^^^^^^^^^^^

The file `energyBusses.csv` defines all busses required to build the energy system. It includes following parameters:

* :ref:`energyvector-label`


.. _consumption:

energyConsumption.csv
^^^^^^^^^^^^^^^^^^^^^

The file `energyConsumption.csv` defines all energy demands that should be included in the energy system. It includes the following parameters:

* :ref:`energyvector-label`
* :ref:`filename-label`
* :ref:`inflowdirection-label`
* :ref:`outflowdirec-label`
* :ref:`typeoemof-label`
* :ref:`unit-label`


.. _conversion:

energyConversion.csv
^^^^^^^^^^^^^^^^^^^^

The file `energyConversion.csv` defines the assets that convert one energy carrier into another one, eg. inverters or generators. Following parameters define them:

* :ref:`age_ins-label`
* :ref:`developmentcosts-label`
* :ref:`dispatchprice-label`
* :ref:`efficiency-label`
* :ref:`energyvector-label`
* :ref:`inflowdirection-label`
* :ref:`installedcap-label`
* :ref:`lifetime-label`
* :ref:`optimizecap-label`
* :ref:`outflowdirec-label`
* :ref:`specificcosts-label`
* :ref:`specificomcosts-label`
* :ref:`typeoemof-label`
* :ref:`unit-label`


.. _production:

energyProduction.csv
^^^^^^^^^^^^^^^^^^^^

The file `energyProduction.csv` defines the assets that serve as energy sources, eg. fuel sources or PV plants. They include the following parameters:

* :ref:`age_ins-label`
* :ref:`developmentcosts-label`
* :ref:`dispatchprice-label`
* :ref:`emissionfactor-label`
* :ref:`energyvector-label`
* :ref:`filename-label`
* :ref:`installedcap-label`
* :ref:`lifetime-label`
* :ref:`maxcap-label`
* :ref:`optimizecap-label`
* :ref:`renewableasset-label`
* :ref:`specificcosts-label`
* :ref:`specificomcosts-label`
* :ref:`typeoemof-label`
* :ref:`unit-label`


.. _providers:

energyProviders.csv
^^^^^^^^^^^^^^^^^^^

The file `energyProviders.csv` defines the energy providers of the energy system. They include the following parameters:

* :ref:`emissionfactor-label`
* :ref:`energyprice-label`
* :ref:`energyvector-label`
* :ref:`feedintariff-label`
* :ref:`inflowdirection-label`
* :ref:`optimizecap-label`
* :ref:`outflowdirec-label`
* :ref:`peakdemand-label`
* :ref:`peakdemandperiod-label`
* :ref:`renshare-label`
* :ref:`typeoemof-label`
* :ref:`unit-label`


.. _storage:

energyStorage.csv
^^^^^^^^^^^^^^^^^

The file `energyStorage.csv` defines the storage assets included in the energy system. It does not hold all needed parameters, but requires `storage_xx.csv` to be defined as well. The file `energyStorage.csv` includes the following parameters:

* :ref:`energyvector-label`
* :ref:`filename-label`
* :ref:`inflowdirection-label`
* :ref:`optimizecap-label`
* :ref:`outflowdirec-label`
* :ref:`storagefilename-label`
* :ref:`typeoemof-label`


.. _fixcost:

fixcost.csv
^^^^^^^^^^^

The parameters must be filled for all three columns/components namely: *distribution_grid*, *engineering* and *operation*.
The file `fixcost.csv` includes the following parameters:

* :ref:`developmentcosts-label`
* :ref:`dispatchprice-label`
* :ref:`labl-label`
* :ref:`lifetime-label`
* :ref:`specificcosts-label`
* :ref:`specificomcosts-label`


.. _project_data:

project_data.csv
^^^^^^^^^^^^^^^^

The file `project_data.csv` includes the following parameters:

* :ref:`country-label`
* :ref:`latitude-label`
* :ref:`longitude-label`
* :ref:`projectid-label`
* :ref:`projectname-label`
* :ref:`scenariodescription-label`
* :ref:`scenarioid-label`
* :ref:`scenarioname-label`


.. _simulation_settings:

simulation_settings.csv
^^^^^^^^^^^^^^^^^^^^^^^

The file `simulation_settings.csv` includes the following parameters:

* :ref:`evaluatedperiod-label`
* :ref:`outputlpfile-label`
* :ref:`startdate-label`
* :ref:`timestep-label`


.. _storage_csv:

storage_*.csv
^^^^^^^^^^^^^

The `*` in the storage filename is the number identifying the storage. It depends on the number of storage components (such as batteries, etc.) present in the system. For e.g., there should be two storage files named storage_01.csv and storage_02.csv if the system contains two storage components.The file `storage_xx.csv` contains the following parameters:

* :ref:`crate-label`
* :ref:`developmentcosts-label`
* :ref:`dispatchprice-label`
* :ref:`efficiency-label`
* :ref:`fixed_thermal_losses_absolute-label`
* :ref:`fixed_thermal_losses_relative-label`
* :ref:`installedcap-label`
* :ref:`lifetime-label`
* :ref:`socin-label`
* :ref:`socmax-label`
* :ref:`socmin-label`
* :ref:`specificcosts-label`
* :ref:`specificomcosts-label`
* :ref:`unit-label`

