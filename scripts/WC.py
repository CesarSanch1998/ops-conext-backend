# Resync script for smartolt by chrome extension  
from utils.request import db_request_smartolt
from utils.snmp_funtion import SNMP_Master
from utils.definitions import olt_devices,snmp_oid,PORT
from utils.ssh import ssh

onu_data = {}
def wanconfig_getdata_smartolt(onu_unique_id):
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
    onu_data['onu_type_name'] = onu_details['onu_type_name']
    # print(onu_data['f/s/p'])
    if onu_data['onu_mode'] == "Bridging":
        response = wc_data_bridge(onu_data)
    elif onu_data['onu_mode'] == "Routing":
        if onu_data['onu_type_name'] == 'ONU-type-eth-4-pots-2-catv-0':
            return 'BDCM'
        else:
            response = wc_data_router(onu_data)
            return response
        # response = resync_undo_data_router(onu_data)
    return response

def wc_data_bridge(data):
    (comm, command, quit_ssh) = ssh(olt_devices[data['olt_name']], True)
    # Wan Config bridge
    command(f"interface gpon {data['onu_frame']}/{data['onu_slot']}")
    command(f"ont wan-config {data['onu_port']} {data['onu_id']} ip-index 1 profile-id 0")
    return f"Client Wan Config Asigned {data['onu_name']} Successfully"

def wc_data_router(data):
    (comm, command, quit_ssh) = ssh(olt_devices[data['olt_name']], True)
    # Wan Config ONT Router
    command(f"interface gpon {data['onu_frame']}/{data['onu_slot']}")
    command(f"ont wan-config {data['onu_port']} {data['onu_id']} ip-index 1 profile-id 0")
    return f"Client Wan Config Asigned {data['onu_name']} Successfully"