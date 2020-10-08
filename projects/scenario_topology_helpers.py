from django.shortcuts import get_object_or_404
from projects.models import Bus, AssetType, Scenario, ConnectionLink, Asset
import json


def load_scenario_topology_from_db(scen_id):
    bus_nodes_list = db_bus_nodes_to_list(scen_id)
    asset_nodes_list = db_asset_nodes_to_list(scen_id)
    connection_links_list = db_connection_links_to_list(scen_id)
    return {"busses": bus_nodes_list, "assets": asset_nodes_list, "links": connection_links_list}


def db_bus_nodes_to_list(scen_id):
    all_db_busses = Bus.objects.filter(scenario_id=scen_id)
    bus_nodes_list = list()
    for db_bus in all_db_busses:
        db_bus_dict = {"name": "bus", "data": {"name": db_bus.name, "bustype": db_bus.type, "databaseId": db_bus.id},
                       "pos_x": db_bus.pos_x, "pos_y": db_bus.pos_y}
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
                              "flow_direction": db_connection.flow_direction}
        connections_list.append(db_connection_dict)
    return connections_list


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


def duplicate_scenario_objects(obj_list, scenario):
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


class NodeObject:
    def __init__(self, node_data=None):
        self.obj_id = node_data['id']
        self.name = node_data['name']
        self.data = node_data['data']
        self.pos_x = node_data['pos_x']
        self.pos_y = node_data['pos_y']
        self.db_obj_id = (node_data['data']['databaseId'] if 'databaseId' in node_data['data'] else None)
        self.node_obj_type = ('bus' if self.name == 'bus' else 'asset')
        self.inputs = node_data['inputs']
        self.outputs = list()

        for key1 in node_data['outputs'].keys():
            for key2 in node_data['outputs'][key1]:
                self.outputs = [connected_node['node'] for connected_node in node_data['outputs'][key1][key2]]

    def create_or_update_asset(self, scen_id):
        asset = get_object_or_404(Asset, pk=self.db_obj_id) if self.db_obj_id else Asset()
        for name, value in self.data.items():
            # print(name, value)
            if name == 'optimize_cap':
                value = True if value == 'on' else False
            setattr(asset, name, value)

        setattr(asset, 'pos_x', self.pos_x)
        setattr(asset, 'pos_y', self.pos_y)
        asset.scenario = get_object_or_404(Scenario, pk=scen_id)
        asset.asset_type = get_object_or_404(AssetType, asset_type=self.name)
        asset.save()
        if self.db_obj_id is None:
            self.db_obj_id = asset.id

    def create_or_update_bus(self, scen_id):
        bus = get_object_or_404(Bus, pk=self.db_obj_id) if self.db_obj_id else Bus()
        setattr(bus, 'name', self.data['name'])
        setattr(bus, 'type', self.data['bustype'])
        setattr(bus, 'pos_x', self.pos_x)
        setattr(bus, 'pos_y', self.pos_y)
        bus.scenario = get_object_or_404(Scenario, pk=scen_id)
        bus.save()
        if self.db_obj_id is None:
            self.db_obj_id = bus.id


def create_node_interconnection_links(node_obj, map_dict, scen_id):
    for output_connection in node_obj.outputs:
        connection = ConnectionLink()
        output_node = map_dict[int(output_connection)]

        if node_obj.name == 'bus' and output_node['node_type'] != 'bus':
            setattr(connection, 'bus', get_object_or_404(Bus, pk=node_obj.db_obj_id))
            setattr(connection, 'asset', get_object_or_404(Asset, pk=output_node['db_obj_id']))
            setattr(connection, 'flow_direction', 'B2A')
            setattr(connection, 'scenario', get_object_or_404(Scenario, pk=scen_id))
        elif node_obj.name != 'bus' and output_node['node_type'] == 'bus':
            setattr(connection, 'asset', get_object_or_404(Asset, pk=node_obj.db_obj_id))
            setattr(connection, 'bus', get_object_or_404(Bus, pk=output_node['db_obj_id']))
            setattr(connection, 'flow_direction', 'A2B')
            setattr(connection, 'scenario', get_object_or_404(Scenario, pk=scen_id))
        connection.save()


# Helper method to clean dict data from None values
def del_none(d: dict):
    # Copy dict in order to modify
    rez = d.copy()
    # Iterate over dict
    for key, value in d.items():
        # If null or empty delete key from dict
        if value is None or value == '':
            del rez[key]
        # Else if nested dict call method again on dict
        elif isinstance(value, dict):
            rez[key] = del_none(value)
        # Else if nested list call method again on contents
        elif isinstance(value, list):
            if not value:
                del rez[key]
            # Remove empty list entries
            for entry in value:
                value[value.index(entry)] = del_none(entry)
    return rez
