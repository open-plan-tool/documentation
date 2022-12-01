:Name:,:Unit:,:Default:,:Category:,:Restrictions:,:Definition:
Demand profile,,,Technical,,The energy demand time serie with timestep (if different energy types are considered different profiles must be given)
Energy timeseries,kWh,,Technical,between 0 and 1 (normalized with maximum),"Specific timeseries of energy sources from a primary-secondary transformation (e.g. PV, Wind)"
Source power mix,Percentage,,Technical,,Percentage of each source of power (inclusive % from Grid)
Lower bound renewable energy share ,Percentage,None,Technical,,A constraint that specifies the lower bound on the share of renewable energies in the optimized output energy mix
CO2 upper limit,T of CO2,None,Environmental,,A constraint that specifies an upper bound on the CO2 emissions
Energy sources capacities,kW,None,Technical,,Energy sources with their capacity open for optimization 
Storage units,kW,None,Technical,,Energy storage units with their capacity and technology
Existing energy source infrastructure,kW,None,Technical,,Existing energy infrastructure not up for optimization (with given capacities)
Existing energy storage infrastructure,kW,None,Technical,,Existing storage infrastructure not up for optimization (with given capacities)
GPS coordinates,,None,GIS,,"GPS coordinate of the location, to retrieve the weather conditions in case of missing timeseries. Could be a point, a set of points, or a polygon"
Grid parameters (v2.0 of the tool),,None,Technical,,"Grid parameters such as:  power, voltage, frequence, line length, line impedance, transformers, topology"
Degree of Autonomy (DA),factor,None,Constraint,between 0 and 1,Degree of Autonomy or self sufficiency wished (capability of the system to sustain a certain part of the load)
Temporal resolution of simulation,,,Time,,Time step of the simulation. The user should be aware that a higher resolution require more data and can lead to longer simulation times (might be already in the provided timeseries)
Optimization goal,,None,Simulation,,"The quantities which govern the optimization (CO2, costs, renewable maximization in energy mix, degree of autonomy, multi-objectives)"
Maximum investment budget,EUR,None,Financial,,Upper bound on the investment budget
Current price of CO2 emission certificates,EUR,,Financial,,Current price of CO2 emission certificates
Future price estimates for CO2 emission certificates,EUR,,Financial,,Timeseries of future price  for CO2 emission certificates (values from the EU-ETS and DE-ETS)
Interest rate,EUR,Value provided,Financial,,A guess of what the  interest rate will be in during the project lifetime. Could be provided as constant or timeseries.
Costs of replacement,EUR,Value provided for each accepted asset type,Financial,,Costs of replacement/improvement of the current system components/assets
Grid stability fee,EUR,Value provided,Financial,,Fee/payment for contribution to grid stability
Spatial resolution,,,GIS,,Define the wished spatial resolution (it is wished that it can range from building up to districts)
New power plant available space,,,GIS,,Available space for new power plants (for PV installation for example)
Consumer requirements,,,GIS/Technical,,consumer requirements such as a specific localisation and wished minimal load profile (e.g. in an industry park)
Existing grid structure (v2.0 of the tool),,,GIS/Technical,,GPS coordinates of current grid structure (lines and hubs)
Future grid structure (v2.0 of the tool),,,GIS/Technical,,GPS coordinates of future grid structure (lines and hubs)
Security of supply,,,Technical,, e.g. existence of back-up system
Balancing ratio for anciliary services,,,Technical,,Balancing ratio for ancilliary services (need a more precise definition as PF could not re-figure out what this means)
Number of future extra users,,,Technical,,Number of future extra user in energy cell
Load types,,,Technical,,Designation of flexible and non-flexible loads in the load profile
Costs of asset use,EUR,Value provided,Financial,,The price of a liter of diesel or a kWh from the grid
Project lifetime,Time,,Simulation,,The lifetime of the project (simulation time)
