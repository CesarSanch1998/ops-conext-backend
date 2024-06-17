from config.db import session,conn
from models.model_db import client_db
from models.plans import plans_db
from utils.definitions import bridges,router,bdcm,snmp_oid,map_ports,state_types
from utils.ssh import ssh
from utils.definitions import olt_devices
from devices.Router import reinstall_router
from devices.Bridge import reinstall_bridge
from devices.BDCM import reinstall_BDCM
from dotenv import load_dotenv
from utils.snmp_funtion import SNMP_Master
import os
import json
import datetime

clients_to_init_modify={}

from utils.spid import calculate_spid
import time
def reinstall_client():
    (comm, command, quit_ssh) = ssh(olt_devices[str(olt)], True)
    try:
        for users in data:
            returned = session.query(plans_db).filter(plans_db.plan_name == users.plan_name_new).first()
            if returned == None:
                return "Plan no existe en la DB"
            else:
                for clave, valor in map_ports.items():
                        if valor == f"{users.frame}/{users.slot}/{users.port}":
                            state_client = SNMP_Master("get",COMUNNITY, olt_devices[str(olt)], snmp_oid['state'],161,"state",fsp_inicial=clave,ont_id=users.onu_id)
                
                if users.device in bridges:
                    clients_to_init_modify.update({})
                    clients_to_init_modify.update({
                        "contract": users.contract,
                        "frame": users.frame,
                        "slot": users.slot,
                        "port":users.port,
                        "onu_id":users.onu_id,
                        "name_1": users.name_1,
                        "name_2": users.name_2,
                        "sn": users.sn,
                        "state":state_types[state_client],
                        "plan_name_old": users.plan_name_old,
                        "plan_name_new": returned.plan_name,
                        "plan_idx":returned.plan_idx,
                        "srv_profile":returned.srv_profile,
                        "vlan":returned.vlan,
                        "line_profile":returned.line_profile,
                        "gem_port":returned.gem_port,
                })
                    # print(clients_to_init_modify)
                    reinstall_bridge(command,clients_to_init_modify)
                    # print(f"{returned.plan_name} {returned.plan_idx} {returned.srv_profile} {returned.vlan} {returned.line_profile} {returned.gem_port}")
                elif users.device in router:
                    #ROUTER---------------------------
                    clients_to_init_modify.update({})
                    clients_to_init_modify.update({
                        "contract": users.contract,
                        "frame": users.frame,
                        "slot": users.slot,
                        "port":users.port,
                        "onu_id":users.onu_id,
                        "name_1": users.name_1,
                        "name_2": users.name_2,
                        "sn": users.sn,
                        "state":state_types[state_client],
                        "plan_name_old": users.plan_name_old,
                        "plan_name_new": returned.plan_name,
                        "plan_idx":returned.plan_idx,
                        "srv_profile":returned.srv_profile,
                        "vlan":returned.vlan,
                        "line_profile":returned.line_profile,
                        "gem_port":returned.gem_port,
                })
                    reinstall_router(command,olt_devices[str(olt)],clients_to_init_modify)
                    # print(clients_to_init_modify)
                    # print(f"{returned.plan_name} {returned.plan_idx} {returned.srv_profile} {returned.vlan} {returned.line_profile} {returned.gem_port}")
                elif users.device in bdcm:
                    
                    for clave, valor in map_ports.items():
                        
                        if valor == f"{users.frame}/{users.slot}/{users.port}":
                            modelo_snmp = SNMP_Master("get",COMUNNITY, olt_devices[str(olt)], snmp_oid['equipment_id_register'],161,"equi_id",fsp_inicial=clave,ont_id=users.onu_id)
                            print(modelo_snmp)
                    
                    #BDCM---------------------------
                    clients_to_init_modify.update({})
                    clients_to_init_modify.update({
                        "contract": users.contract,
                        "frame": users.frame,
                        "slot": users.slot,
                        "port":users.port,
                        "onu_id":users.onu_id,
                        "name_1": users.name_1,
                        "name_2": users.name_2,
                        "sn": users.sn,
                        "state":state_types[state_client],
                        "plan_name_old": users.plan_name_old,
                        "plan_name_new": returned.plan_name,
                        "plan_idx":returned.plan_idx,
                        "srv_profile":returned.srv_profile,
                        "vlan":returned.vlan,
                        "line_profile":returned.line_profile,
                        "gem_port":returned.gem_port,
                })
                    #Despues de saber si lo detecta como ONU-type-eth-4-pots-2-catv-0  lo verificamos con snmp para saber el equipo
                    if modelo_snmp == '1126':
                        reinstall_BDCM(command,clients_to_init_modify)
                    elif modelo_snmp in router:
                        reinstall_router(command,olt_devices[str(olt)],clients_to_init_modify)
                    elif modelo_snmp in router:
                        reinstall_bridge(command,clients_to_init_modify)
                    elif modelo_snmp == '':
                        print("EL EQUIPO ESTA APAGADO SE INSTALARA CONFIG PERSONALIZADA!!")
                        reinstall_router(command,olt_devices[str(olt)],clients_to_init_modify)
                        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d")
                        with open(f"cliente_omitido-{fecha_hora}.json", "a") as archivo_json:
                            json.dump(clients_to_init_modify, archivo_json, indent=4)

    # print(data)
    except Exception as e:
        session.rollback()
        raise e  # o maneja la excepción de otra manera (registra el error, devuelve un mensaje, etc.)
    finally:
        session.close()
        conn.close()
        
    
    return data



def reinstall_router(command,ip,data):
    # (comm, command, quit_ssh) = ssh(ip, True)
    spid = calculate_spid(data['slot'],data['port'],data['onu_id'])
    command(f"undo service-port {spid['I']}")
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(f"ont delete {data['port']} {data['onu_id']}")
    time.sleep(1)
    command(f'ont add {data["port"]} {data["onu_id"]} sn-auth {data["sn"]} omci ont-lineprofile-id {data["line_profile"]} ont-srvprofile-id {data["srv_profile"]} desc "{data["name_1"]+" "+ data["name_2"] +" "+ data["contract"]}"')
    
    if data["state"] != 'active':
        command(f"ont deactivate {data['port']} {data['onu_id']}")
    
    command(f"ont optical-alarm-profile {data['port']} {data['onu_id']} profile-id 3")
    command(f"ont alarm-policy {data['port']} {data['onu_id']} policy-id 1")
    command(f"ont ipconfig {data['port']} {data['onu_id']} ip-index 1 dhcp vlan {data['vlan']} priority 0")
    command(f"ont internet-config {data['port']} {data['onu_id']} ip-index 1")
    command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 0")
    command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 1 profile-id 0")
    command(f"ont fec {data['port']} {data['onu_id']} use-profile-config")
    command(f"ont port route {data['port']} {data['onu_id']} eth 1-8 enable")
    command(f"quit")
    command(f"service-port {spid['I']} vlan {data['vlan']} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['onu_id']} gemport {data['gem_port']} multi-service user-vlan {data['vlan']} tag-transform transparent inbound traffic-table index {data['plan_idx']} outbound traffic-table index {data['plan_idx']}")
    print("\n")
    print(f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']}")
    return f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']} "



def reinstall_bridge(command,data):
    # (comm, command, quit_ssh) = ssh(ip, True)
    spid = calculate_spid(data["slot"],data["port"],data["onu_id"])
    command(f'undo service-port {spid["I"]}')
    command(f'interface gpon {data["frame"]}/{data["slot"]}')
    command(f'ont delete {data["port"]} {data["onu_id"]}')
    time.sleep(1)
    command(f'ont add {data["port"]} {data["onu_id"]} sn-auth {data["sn"]} omci ont-lineprofile-id {data["line_profile"]} ont-srvprofile-id {data["srv_profile"]} desc "{data["name_1"]+" "+ data["name_2"] +" "+ data["contract"]}" ')
    
    if data["state"] != 'active':
        command(f"ont deactivate {data['port']} {data['onu_id']}")
    
    command(f'ont optical-alarm-profile {data["port"]} {data["onu_id"]} profile-id 3')
    command(f'ont alarm-policy {data["port"]} {data["onu_id"]} policy-id 1')
    command(f'ont fec {data["port"]} {data["onu_id"]} use-profile-config')
    command(f'ont port native-vlan {data["port"]} {data["onu_id"]} eth 1 vlan {data["vlan"]} priority 0')
    command(f'ont port native-vlan {data["port"]} {data["onu_id"]} eth 2 vlan {data["vlan"]} priority 0')
    
    command(f'quit')
    command(f'service-port {spid["I"]} vlan {data["vlan"]} gpon {data["frame"]}/{data["slot"]}/{data["port"]} ont {data["onu_id"]} gemport {data["gem_port"]} multi-service user-vlan {data["vlan"]} tag-transform transparent inbound traffic-table index {data["plan_idx"]} outbound traffic-table index {data["plan_idx"]}')
    print("\n")
    print(f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']}")
    return f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']} "

def reinstall_BDCM(command,data):
    # (comm, command, quit_ssh) = ssh(ip, True)
    spid = calculate_spid(data['slot'],data['port'],data['onu_id'])
    command(f"undo service-port {spid['I']}")
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(f"ont delete {data['port']} {data['onu_id']}")
    time.sleep(1)
    command(f'ont add {data["port"]} {data["onu_id"]} sn-auth {data["sn"]} omci ont-lineprofile-id {data["line_profile"]} ont-srvprofile-id {data["srv_profile"]} desc "{data["name_1"]+" "+ data["name_2"] +" "+ data["contract"]}"')

    if data["state"] != 'active':
        command(f"ont deactivate {data['port']} {data['onu_id']}")

    command(f"ont optical-alarm-profile {data['port']} {data['onu_id']} profile-id 3")
    command(f"ont alarm-policy {data['port']} {data['onu_id']} policy-id 1")
    command(f"ont ipconfig {data['port']} {data['onu_id']} ip-index 1 dhcp vlan {data['vlan']} priority 0")
    command(f"ont ipconfig {data['port']} {data['onu_id']} ip-index 2 dhcp vlan {data['vlan']} priority 5")
    command(f"ont internet-config {data['port']} {data['onu_id']} ip-index 1")
    # command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 0")
    command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 1 profile-id 0")
    command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 2 profile-id 0")
    command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 2")
    command(f"ont fec {data['port']} {data['onu_id']} use-profile-config")
    # command(f"ont port route {data['port']} {data['onu_id']} eth 1-8 enable")
    command(f"quit")
    command(f"service-port {spid['I']} vlan {data['vlan']} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['onu_id']} gemport {data['gem_port']} multi-service user-vlan {data['vlan']} tag-transform transparent inbound traffic-table index {data['plan_idx']} outbound traffic-table index {data['plan_idx']}")
    print("\n")
    print(f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']}")
    return f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']} "
