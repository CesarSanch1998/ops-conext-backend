from utils.snmp_funtion import SNMP_Master
import os
from dotenv import load_dotenv
from utils.definitions import olt_devices,snmp_oid,PORT
from utils.ssh import ssh
from utils.request import db_request
from utils.definitions import endpoints
from utils.spid import calculate_spid
from fastapi import HTTPException
import time
from devices.Router import install_Router
load_dotenv()

# Access environment variables
COMUNNITY = os.getenv("SNMP_READ")

def search_autofind(name,contract,olt,sn,device_type,assigned_public_ip,plan_name,isbridge):
    response = SNMP_Master("next",COMUNNITY,olt_devices[str(olt)],snmp_oid["autofind_sn"],PORT,"sn")
    for list in response:
        print(f"{list['sn']}  is not {sn}")
        if list['sn'].upper() == sn.upper():
            
            response = activate(olt_devices[str(olt)],list['f/s/p'],list['sn'],device_type,plan_name,name,contract,list['f/s/p_oid'],isbridge,olt)
            return response

    return response
def activate(ip,fsp,sn,device_type,plan_name,name,contract,port_oid,isbridge,olt_id):
    separate = fsp.split("/")
    vlan=""
    srv_prof =""
    line_prof=""
    ont_id = ""
    f = separate[0]
    s = separate[1]
    p = separate[2]
    SN = sn.upper()
    
    plans = db_request(endpoints["get_plans"], {})
    # print(plans["data"])
    for value in plans['data']:
        if value['plan_name'] == plan_name:
            vlan = value['vlan']
            srv_prof = value['srv_profile']
            line_prof = value['line_profile']
            gem_port = value['gem_port']
            plan_idx = value['plan_idx']
    
    (comm, command, quit_ssh) = ssh(ip, True)
    command(f"interface gpon {f}/{s}")
    command(f'ont add {p} sn-auth {SN} omci ont-lineprofile-id {line_prof} ont-srvprofile-id {srv_prof} desc "{name +" "+ contract }" ')
    #Verificar en que index se instalo en la olt
    response = SNMP_Master("next",COMUNNITY,ip,snmp_oid["serial"],PORT,"sn",port_oid)
    # print(response)
    for list in response:
        if list['sn'] == sn:
            ont_id = list['ont_id']
            break
    # print(str(list['equip_id'],16)," este es el  equip id")
    
    command(f"ont optical-alarm-profile {p} {ont_id} profile-name ALARMAS_OPTICAS")
    command(f"ont alarm-policy {p} {ont_id} policy-name FAULT_ALARMS")
    # command(f'quit')

    equipement_id= SNMP_Master("get",COMUNNITY,ip,snmp_oid["equipment_id_register"],PORT,"equi_id",port_oid,f"{ont_id}")
    if equipement_id == "1126":#Los BDCM tienen 1126 y los demas el modelo
        time.sleep(17)
        # print(equipement_id)
    else:
        install_Router(command,f,s,p,ont_id,ip,PORT,port_oid,vlan,gem_port,plan_idx)
        # time.sleep(12)
        # print(equipement_id)
    
    #-------------------------------------------------------------------
        # Agregar validacion automatica de potencia y temperatura
    rx_ont = SNMP_Master("get",COMUNNITY,ip,snmp_oid["rx_ont"],PORT,"pw_ont",port_oid,ont_id)
    rx_olt= SNMP_Master("get",COMUNNITY,ip,snmp_oid["rx_olt"],PORT,"pw_olt",port_oid,ont_id)
    # temp_ont = SNMP_Master("next",COMUNNITY,ip,snmp_oid["serial"],PORT,"sn",port_oid)
    # print(rx_olt)
    # print(rx_ont)
    if rx_ont  <= -26.50 and rx_olt <= -31.50:

        ##----------------------------------
        #agregar comandos para quitar los datos del equipo si no se puede seguir la instalacion
        command(f'interface gpon {f} {s}')
        command(f'ont delete {p} {ont_id}')
        return HTTPException(status_code=202, detail={f"Equipo no instalado ont:{rx_ont}  y olt:{rx_olt}"})
    
    if isbridge == True:
        command(f'ont port native-vlan {p} {ont_id} eth 1 vlan {vlan}')

    #-----------------------------------------------------------------
    spid = calculate_spid(s,p,ont_id)
    
    # print(equipement_id)
    # time.sleep(10)
    if equipement_id == "1126":#Los BDCM tienen 1126 y los demas el modelo
        time.sleep(0.5)
        command(f"ont ipconfig {p} {ont_id} ip-index 1 dhcp vlan {vlan} priority 0")
        time.sleep(0.5)
        command(f"ont ipconfig {p} {ont_id} ip-index 2 dhcp vlan {vlan} priority 5")
    else:
        command(f'ont ipconfig {p} {ont_id} ip-index 2 dhcp vlan {vlan}')

    command(f'ont internet-config {p} {ont_id} ip-index 2')
    command(f'ont policy-route-config {p} {ont_id} profile-id 2')
    command(f'quit')
    command(f'service-port {spid["I"]} vlan {vlan} gpon {f}/{s}/{p} ont {ont_id} gemport {gem_port} multi-service user-vlan {vlan} tag-transform transparent inbound traffic-table index {plan_idx} outbound traffic-table index {plan_idx}')
    command(f'interface gpon {f}/{s}')
    if equipement_id == "1126": #BDCM
        time.sleep(0.5)
        command(f"ont wan-config {p} {ont_id} ip-index 1 profile-id 0")
        time.sleep(0.5)
        command(f"ont wan-config {p} {ont_id} ip-index 2 profile-id 0")
        command(f"ont fec {p} {ont_id} use-profile-config")
    else:
        command(f'ont wan-config {p} {ont_id} ip-index 2 profile-id 0')
        command(f'ont port route {p} {ont_id} eth 1-4 enable')

    db_request(endpoints["add_client"], 
        {
	"API_KEY":"pykboz-metcew-fihVe2K2.p##/5We$tt!&",
	"data":
	{
        "contract": contract,
        "frame": int(f),
        "slot": int(s),
        "port":int(p),
        "onu_id":int(ont_id),
        "olt": int(olt_id),
        "fsp": f"{f}/{s}/{p}",
        "fspi": f"{f}/{s}/{p}/{ont_id}",
        "name_1": name,
        "name_2": "",
        "status": "online",
        "state": "active",
        "sn": sn.upper(),
        "device": "ninguno",
        "plan_name": plan_name,
        "spid": int(spid["I"])
	}
}
    )
    return HTTPException(status_code=202, detail=
                  {
        "f/s/p/id":f"{f}/{s}/{p}/{ont_id}",
        "nombre":{name},
        "serial":{sn.upper()},
        "vlan":{vlan},
        "spid":{spid["I"]},
        "Equi_id":equipement_id,
        "status":"OK"
            })
    # return {
    #     "f/s/p/id":f"{f}/{s}/{p}/{ont_id}",
    #     "nombre":{name},
    #     "serial":{sn},
    #     "vlan":{vlan},
    #     "spid":{spid["I"]},
    #     "Equi_id":equipement_id,
    #     "status":"OK"
    #         }
# def search_more_data():
#     response = SNMP_Master("next",COMUNNITY,olt_devices[str(olt)],snmp_oid["autofind_sn"],PORT,"sn")
