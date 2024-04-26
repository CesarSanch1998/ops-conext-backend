# Resync script for smartolt by chrome extension  
from utils.request import db_request_smartolt
from utils.definitions import olt_devices,snmp_oid,PORT
from utils.ssh import ssh

onu_data = {}
def resync_getdata_smartolt(onu_unique_id):
    data = db_request_smartolt('get_onu_smartolt',onu_unique_id)
    onu_details = data['onu_details']
    onu_service_ports = onu_details.get("service_ports", [])

    for port in onu_service_ports:
        onu_data['service_port'] = port["service_port"]
        onu_data['vlan'] = port["vlan"]
        onu_data['upload_speed'] = port["upload_speed"]
        onu_data['download_speed'] = port["download_speed"]
    onu_data['onu_sn'] = onu_details['sn']
    onu_data['onu_mode'] = onu_details['mode']
    onu_data['onu_frame'] = '0'
    onu_data['onu_type'] = onu_details['onu_type_name']
    onu_data['onu_slot'] = onu_details['board']
    onu_data['onu_port'] = onu_details['port']
    onu_data['onu_id'] = onu_details['onu']
    onu_data['f/s/p'] = f"{onu_data['onu_frame']}/{onu_data['onu_slot']}/{onu_data['onu_port']}"
    onu_data['onu_name'] = onu_details['name']
    onu_data['olt_name'] = onu_details['olt_name'][-1:]
    # print(onu_data['f/s/p'])
    if onu_data['onu_mode'] == "Bridging":
        response = resync_undo_data_bridge(onu_data)
    elif onu_data['onu_mode'] == "Routing":
        response = resync_undo_data_router(onu_data)
    return data

def resync_undo_data_bridge(data):
    (comm, command, quit_ssh) = ssh(olt_devices[data['olt_name']], True)
    # Undo ONT bridge
    command(f"undo service-port {data['service_port']} vlan {data['vlan']} gpon {data['f/s/p']} ont {data['onu_id']} gemport 11 multi-service user-vlan {data['vlan']} tag-transform transparent inbound traffic-table index 111 outbound traffic-table index 111")
    command(f"interface gpon {data['onu_frame']}/{data['onu_slot']}")
    command(f"undo ont internet-config {data['onu_port']} {data['onu_id']}")
    command(f"undo ont wan-config {data['onu_port']} {data['onu_id']} ip-index 2")
    command(f"undo ont ipconfig {data['onu_port']} {data['onu_id']} ip-index 2")
    command(f"undo ont policy-route-config {data['onu_port']} {data['onu_id']} profile-id 2")

    # Reactivate ONT bridge
    command(f"ont ipconfig {data['onu_port']} {data['onu_id']} ip-index 2")
    command(f"ont wan-config {data['onu_port']} {data['onu_id']} ip-index 2 profile-id 0")
    command(f"ont internet-config {data['onu_port']} {data['onu_id']} ip-index 2")
    command(f"ont policy-route-config {data['onu_port']} {data['onu_id']} profile-id 2")
    command(f"quit")
    command(f"service-port {data['service_port']} vlan {data['vlan']} gpon {data['f/s/p']} ont {data['onu_id']} gemport 11 multi-service user-vlan {data['vlan']} tag-transform transparent inbound traffic-table index 111 outbound traffic-table index 111")
    return f"Client Resync {data['onu_name']} Successfully"
def resync_undo_data_router(data):
    (comm, command, quit_ssh) = ssh(olt_devices[data['olt_name']], True)
    # Undo ONT bridge
    command(f"undo service-port {data['service_port']} vlan {data['vlan']} gpon {data['f/s/p']} ont {data['onu_id']} gemport 11 multi-service user-vlan {data['vlan']} tag-transform transparent inbound traffic-table index 111 outbound traffic-table index 111")
    command(f"interface gpon {data['onu_frame']}/{data['onu_slot']}")
    command(f"undo ont internet-config {data['onu_port']} {data['onu_id']}")
    command(f"undo ont wan-config {data['onu_port']} {data['onu_id']} ip-index 2")
    command(f"undo ont ipconfig {data['onu_port']} {data['onu_id']} ip-index 2")
    command(f"undo ont policy-route-config {data['onu_port']} {data['onu_id']} profile-id 2")

    # Reactivate ONT bridge
    command(f"ont ipconfig {data['onu_port']} {data['onu_id']} ip-index 2")
    command(f"ont wan-config {data['onu_port']} {data['onu_id']} ip-index 2 profile-id 0")
    command(f"ont internet-config {data['onu_port']} {data['onu_id']} ip-index 2")
    command(f"ont policy-route-config {data['onu_port']} {data['onu_id']} profile-id 2")
    command(f"quit")
    command(f"service-port {data['service_port']} vlan {data['vlan']} gpon {data['f/s/p']} ont {data['onu_id']} gemport 11 multi-service user-vlan {data['vlan']} tag-transform transparent inbound traffic-table index 111 outbound traffic-table index 111")