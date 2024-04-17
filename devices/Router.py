# from utils.ssh import ssh
import time
from utils.snmp_funtion import SNMP_Master
from utils.definitions import olt_devices,snmp_oid,PORT
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from utils.spid import calculate_spid
load_dotenv()

# Access environment variables
COMUNNITY = os.getenv("SNMP_READ")

def install_Router(command,f,s,p,ont_id,ip,PORT,port_oid,vlan,gem_port,plan_idx):
    # (comm, command, quit_ssh) = ssh(ip, True)
    time.sleep(12)
    # Agregar validacion automatica de potencia y temperatura
    rx_ont = SNMP_Master("get",COMUNNITY,ip,snmp_oid["rx_ont"],PORT,"pw_ont",port_oid,ont_id)
    rx_olt= SNMP_Master("get",COMUNNITY,ip,snmp_oid["rx_olt"],PORT,"pw_olt",port_oid,ont_id)

    if rx_ont  <= -26.50 and rx_olt <= -31.50:

        ##----------------------------------
        #agregar comandos para quitar los datos del equipo si no se puede seguir la instalacion
        command(f'interface gpon {f} {s}')
        command(f'ont delete {p} {ont_id}')
        return HTTPException(status_code=202, detail={f"Equipo no instalado ont:{rx_ont}  y olt:{rx_olt}"})
    
    spid = calculate_spid(s,p,ont_id)

    command(f'ont ipconfig {p} {ont_id} ip-index 2 dhcp vlan {vlan}')
    command(f'ont internet-config {p} {ont_id} ip-index 2')
    command(f'ont policy-route-config {p} {ont_id} profile-id 2')
    command(f'quit')
    command(f'service-port {spid["I"]} vlan {vlan} gpon {f}/{s}/{p} ont {ont_id} gemport {gem_port} multi-service user-vlan {vlan} tag-transform transparent inbound traffic-table index {plan_idx} outbound traffic-table index {plan_idx}')
    command(f'interface gpon {f}/{s}')
    command(f'ont wan-config {p} {ont_id} ip-index 2 profile-id 0')
    command(f'ont port route {p} {ont_id} eth 1-4 enable')
    