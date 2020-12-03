delete from projects_assettype where 1=1;
delete from projects_valuetype where 1=1;


insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('dso','Electricity', 'energy_provider', 'source', '[name,energy_price,feedin_tariff,peak_demand_pricing,peak_demand_pricing_period,renewable_share]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('demand','Electricity', 'energy_consumption', 'sink', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap,input_timeseries]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('transformer_station_in','Electricity', 'energy_conversion', 'transformer', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap,efficiency]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('transformer_station_out','Electricity', 'energy_conversion', 'transformer', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap,efficiency]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('storage_charge_controller_in','Electricity', 'energy_conversion', 'transformer', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap,efficiency]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('storage_charge_controller_out','Electricity', 'energy_conversion', 'transformer', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap,efficiency]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('solar_inverter','Electricity', 'energy_conversion', 'transformer', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap,efficiency]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('pv_plant','Electricity', 'energy_production', 'source', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap, renewable_asset, input_timeseries]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('wind_plant','Electricity', 'energy_production', 'source', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap, renewable_asset, input_timeseries]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('charging_power','Electricity', 'energy_storage', 'storage', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap,crate,efficiency]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('discharging_power','Electricity', 'energy_storage', 'storage', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap,crate,efficiency]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('capacity','Electricity', 'energy_storage', 'storage', '[name,age_installed,installed_capacity,capex_fix,capex_var,opex_fix,opex_var,lifetime,optimize_cap,efficiency,soc_initial,soc_max,soc_min]' );
insert into projects_assettype(asset_type, energy_vector, asset_category, mvs_type, asset_fields) values
('ess','Electricity', 'energy_storage', 'storage', '[name, optimize_cap]' );

insert into projects_valuetype( unit, type) values ('year', 'duration' );
insert into projects_valuetype( unit, type) values ('', 'annuity_factor' );
insert into projects_valuetype( unit, type) values ('factor', 'discount' );
insert into projects_valuetype( unit, type) values ('factor', 'tax' );
insert into projects_valuetype( unit, type) values ('', 'crf' );
insert into projects_valuetype( unit, type) values ('factor of total capacity (kWh)', 'crate' );
insert into projects_valuetype( unit, type) values ('year', 'age_installed' );
insert into projects_valuetype( unit, type) values ('None or factor', 'soc_initial' );
insert into projects_valuetype( unit, type) values ('factor', 'soc_max' );
insert into projects_valuetype( unit, type) values ('factor', 'soc_min' );
insert into projects_valuetype( unit, type) values ('currency', 'capex_fix' );
insert into projects_valuetype( unit, type) values ('currency/unit/year', 'opex_var' );
insert into projects_valuetype( unit, type) values ('factor', 'efficiency' );
insert into projects_valuetype( unit, type) values ('unit', 'installed_capacity' );
insert into projects_valuetype( unit, type) values ('year', 'lifetime' );
insert into projects_valuetype( unit, type) values ('kW', 'maximum_capacity' );
insert into projects_valuetype( unit, type) values ('currency/kWh', 'energy_price' );
insert into projects_valuetype( unit, type) values ('currency/kWh', 'feedin_tariff' );
insert into projects_valuetype( unit, type) values ('bool', 'optimize_cap' );
insert into projects_valuetype( unit, type) values ('currency/kW', 'peak_demand_pricing' );
insert into projects_valuetype( unit, type) values ('times per year (1,2,3,4,6,12)', 'peak_demand_pricing_period' );
insert into projects_valuetype( unit, type) values ('factor', 'renewable_share' );
insert into projects_valuetype( unit, type) values ('currency/unit', 'capex_var' );
insert into projects_valuetype( unit, type) values ('currency/year', 'opex_fix' );
insert into projects_valuetype( unit, type) values ('currency/year', 'specific_costs_om' );
insert into projects_valuetype( unit, type) values ('kWh', 'input_timeseries' );
insert into projects_valuetype( unit, type) values ('days', 'evaluated_period' );
insert into projects_valuetype( unit, type) values ('bool', 'renewable_asset,' );