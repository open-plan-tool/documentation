from django.shortcuts import get_object_or_404
from projects.models import Bus, AssetType, Scenario, ConnectionLink, Asset
import json
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


# region sent db nodes to js
def load_scenario_topology_from_db(scen_id):
    bus_nodes_list = db_bus_nodes_to_list(scen_id)
    asset_nodes_list = db_asset_nodes_to_list(scen_id)
    connection_links_list = db_connection_links_to_list(scen_id)
    return {"busses": bus_nodes_list, "assets": asset_nodes_list, "links": connection_links_list}


def db_bus_nodes_to_list(scen_id):
    all_db_busses = Bus.objects.filter(scenario_id=scen_id)
    bus_nodes_list = list()
    for db_bus in all_db_busses:
        db_bus_dict = {"name": "bus", "data": {"name": db_bus.name, "bustype": db_bus.type, "databaseId": db_bus.id,
                                               "parent_asset_id": db_bus.parent_asset_id if db_bus.parent_asset_id else ""},
                       "pos_x": db_bus.pos_x, "pos_y": db_bus.pos_y, "input_ports": db_bus.input_ports,
                       "output_ports": db_bus.output_ports}
        # "input_ports": db_bus.input_ports, "output_ports": db_bus.output_ports}
        bus_nodes_list.append(db_bus_dict)
    return bus_nodes_list


def db_asset_nodes_to_list(scen_id):
    all_db_assets = Asset.objects.filter(scenario_id=scen_id)
    asset_nodes_list = list()
    for db_asset in all_db_assets:
        data = dict()
        db_asset_to_dict = json.loads(json.dumps(db_asset.__dict__, default=lambda o: o.__dict__))
        ignored_keys = ["scenario_id", "pos_x", "pos_y", "asset_type_id"]
        for key, val in db_asset_to_dict.items():
            if not (key.startswith('_') or (key in ignored_keys) or val is None):
                if key == "id":
                    data["databaseId"] = val
                else:
                    data[key] = val

        asset_type_obj = get_object_or_404(AssetType, pk=db_asset.asset_type_id)
        db_asset_dict = {"name": asset_type_obj.asset_type, "pos_x": db_asset.pos_x, "pos_y": db_asset.pos_y,
                         "data": data}
        asset_nodes_list.append(db_asset_dict)
    return asset_nodes_list


def db_connection_links_to_list(scen_id):
    all_db_connection_links = ConnectionLink.objects.filter(scenario_id=scen_id)
    connections_list = list()
    for db_connection in all_db_connection_links:
        db_connection_dict = {"bus_id": db_connection.bus_id, "asset_id": db_connection.asset_id,
                              "flow_direction": db_connection.flow_direction,
                              "bus_connection_port": db_connection.bus_connection_port}
        connections_list.append(db_connection_dict)
    return connections_list


# endregion db_nodes_to_js


def update_deleted_objects_from_database(scenario_id, topo_node_list):
    # Delete Database Scenario Related Objects which are not in the topology before inserting or updating data.
    all_scenario_asset_ids = Asset.objects.filter(scenario_id=scenario_id).values_list('id', flat=True)
    all_scenario_busses_ids = Bus.objects.filter(scenario_id=scenario_id).values_list('id', flat=True)
    topology_asset_ids = list()
    topology_busses_ids = list()
    for node in topo_node_list:
        if node.name != 'bus' and node.db_obj_id:
            topology_asset_ids.append(node.db_obj_id)
        elif node.name == 'bus' and node.db_obj_id:
            topology_busses_ids.append(node.db_obj_id)

    for asset_id in all_scenario_asset_ids:
        if asset_id not in topology_asset_ids:
            # print("Asset {} not in topology. Gonna delete!!".format(asset_id))
            Asset.objects.filter(id=asset_id).delete()

    for bus_id in all_scenario_busses_ids:
        if bus_id not in topology_busses_ids:
            # print("Bus {} not in topology. Gonna delete!!".format(bus_id))
            Bus.objects.filter(id=bus_id).delete()


# region Scenario Duplicate
def duplicate_scenario_objects(obj_list, scenario):
    # FIXME: During Scenario Duplication ESS assets need special care, /
    #  regarding the parent_asset_id
    mapping_dict = dict()
    for obj in obj_list:
        old_id = obj.id
        obj.id = None
        obj.scenario = scenario
        obj.save()
        mapping_dict[old_id] = obj.id
    return mapping_dict


def duplicate_scenario_connections(connections_list, scenario, asset_map, bus_map):
    for connection in connections_list:
        old_asset_id = connection.asset_id
        old_bus_id = connection.bus_id
        connection.id = None
        connection.asset_id = asset_map[old_asset_id]
        connection.bus_id = bus_map[old_bus_id]
        connection.scenario = scenario
        connection.save()
# endregion


class NodeObject:
    def __init__(self, node_data=None):
        self.obj_id = node_data['id']
        self.name = node_data['name']
        self.data = node_data['data']
        self.pos_x = node_data['pos_x']
        self.pos_y = node_data['pos_y']
        self.db_obj_id = (node_data['data']['databaseId'] if 'databaseId' in node_data['data'] else None)
        self.group_id = (node_data['data']['parent_asset_id'] if 'parent_asset_id' in node_data['data'] else None)
        self.node_obj_type = ('bus' if self.name == 'bus' else 'asset')
        self.inputs = NodeObject.refactor_connections(node_data['inputs'])
        self.outputs = NodeObject.refactor_connections(node_data['outputs'])

    @staticmethod
    def refactor_connections(input_or_output_data):
        connection_dict = dict()
        for key in input_or_output_data.keys():
            temp = [connected_node['node'] for connected_node in input_or_output_data[key]['connections']]
            connection_dict[key] = temp
        return connection_dict

    def create_or_update_asset(self, scen_id):
        asset = get_object_or_404(Asset, pk=self.db_obj_id) if self.db_obj_id else Asset()

        try:
            for name, value in self.data.items():
                if name != "parent_asset_id":
                    setattr(asset, name, value)

            setattr(asset, 'pos_x', self.pos_x)
            setattr(asset, 'pos_y', self.pos_y)
            asset.scenario = get_object_or_404(Scenario, pk=scen_id)
            asset.asset_type = get_object_or_404(AssetType, asset_type=self.name)

            # List of fields that are not required included for the particular asset type
            excluded_fields = [prop for prop in asset.fields if prop not in asset.asset_type.asset_fields]

            asset.full_clean(exclude=excluded_fields)

        except (KeyError, ValidationError) as error:
            return {"success": False,
                    "specific_obj_type": self.name,
                    "obj_name": self.data['name'],
                    "full_error": str(error)
                    }
        else:
            asset.save()
            if self.db_obj_id is None:
                self.db_obj_id = asset.id
            return {"success": True, "obj_type": "asset"}

    def create_or_update_bus(self, scen_id):
        bus = get_object_or_404(Bus, pk=self.db_obj_id) if self.db_obj_id else Bus()

        try:
            setattr(bus, 'name', self.data['name'])
            setattr(bus, 'type', self.data['bustype'])
            setattr(bus, 'pos_x', self.pos_x)
            setattr(bus, 'pos_y', self.pos_y)
            setattr(bus, 'input_ports', len(self.inputs))
            setattr(bus, 'output_ports', len(self.outputs))
            bus.scenario = get_object_or_404(Scenario, pk=scen_id)

            bus.full_clean()
        except (KeyError, ValidationError) as error:
            return {"success": False,
                    "specific_obj_type": self.name,
                    "obj_name": self.data['name'],
                    "full_error": str(error)
                    }
        else:
            bus.save()
            if self.db_obj_id is None:
                self.db_obj_id = bus.id
            return {"success": True, "obj_type": "bus"}

    def assign_asset_to_proper_group(self, node_to_db_mapping):
        try:
            if self.node_obj_type == "asset":
                asset = get_object_or_404(Asset, pk=self.db_obj_id)
                asset.parent_asset_id = node_to_db_mapping[self.group_id]["db_obj_id"] if self.group_id else None
                asset.save()
            else:  # i.e. "bus"
                bus = get_object_or_404(Bus, pk=self.db_obj_id)
                bus.parent_asset_id = node_to_db_mapping[self.group_id]["db_obj_id"] if self.group_id else None
                bus.save()
        except KeyError:
            return {"success": False, "obj_type": self.node_obj_type}
        except ValidationError:
            return {"success": False, "obj_type": self.node_obj_type}
        else:
            return {"success": True, "obj_type": self.node_obj_type}


def create_node_interconnection_links(node_obj, map_dict, scen_id):
    for port_key, connections_list in node_obj.outputs.items():
        for output_connection in connections_list:
            connection = ConnectionLink()
            output_node = map_dict[int(output_connection)]

            if node_obj.name == 'bus' and output_node['node_type'] != 'bus':
                setattr(connection, 'bus', get_object_or_404(Bus, pk=node_obj.db_obj_id))
                setattr(connection, 'asset', get_object_or_404(Asset, pk=output_node['db_obj_id']))
                setattr(connection, 'flow_direction', 'B2A')
                setattr(connection, 'bus_connection_port', port_key)
                setattr(connection, 'scenario', get_object_or_404(Scenario, pk=scen_id))
            elif node_obj.name != 'bus' and output_node['node_type'] == 'bus':
                setattr(connection, 'asset', get_object_or_404(Asset, pk=node_obj.db_obj_id))
                setattr(connection, 'bus', get_object_or_404(Bus, pk=output_node['db_obj_id']))
                setattr(connection, 'flow_direction', 'A2B')

                for node_port_key, con_links_list in output_node['input_connections'].items():
                    for index, input_connection in enumerate(con_links_list):
                        if node_obj.obj_id == int(input_connection):
                            print(output_node['input_connections'][node_port_key][index])
                            setattr(connection, 'bus_connection_port', node_port_key)
                            map_dict[int(output_connection)]['input_connections'][node_port_key][
                                index] = '0'  # hacky solution
                            break
                    else:
                        continue
                    break
                setattr(connection, 'scenario', get_object_or_404(Scenario, pk=scen_id))
            connection.save()


def create_ESS_objects(all_ess_assets_node_list, scen_id):
    ess_obj_list = list()

    charging_power_asset_id = AssetType.objects.get(asset_type="charging_power")
    discharging_power_asset_id = AssetType.objects.get(asset_type="discharging_power")
    capacity_asset_id = AssetType.objects.get(asset_type="capacity")

    scenario_connection_links = ConnectionLink.objects.filter(scenario_id=scen_id)
    cap_scenario_connection_links = scenario_connection_links.filter(asset__asset_type=capacity_asset_id)
    charge_scenario_connection_links = scenario_connection_links.filter(asset__asset_type=charging_power_asset_id)
    discharge_scenario_connection_links = scenario_connection_links.filter(asset__asset_type=discharging_power_asset_id)

    for asset in all_ess_assets_node_list:
        if asset.name == 'capacity':
            # check if there is a connection link to a bus
            pass


# Helper method to clean dict data from empty values
def remove_empty_elements(d):
    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}
