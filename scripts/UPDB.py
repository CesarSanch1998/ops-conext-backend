# Resync script for smartolt by chrome extension  
from utils.request import db_request_smartolt
from utils.snmp_funtion import SNMP_Master
from utils.definitions import olt_devices,snmp_oid,PORT
from utils.ssh import ssh
from config.db import session
from models.model_db import client_db
from utils.definitions import plan_type
import json
onu_data = {}

def getdata_smartolt(onu_unique_id):
    data = db_request_smartolt('get_onu_smartolt',onu_unique_id)
    onu_details = data['onu_details']
    onu_service_ports = onu_details.get("service_ports", [])

    for port in onu_service_ports:
        onu_data['service_port'] = port["service_port"]
        onu_data['vlan'] = port["vlan"]
        onu_data['upload_speed'] = port["upload_speed"]
        onu_data['download_speed'] = port["download_speed"]
    onu_data['onu_sn'] = "48575443" + onu_details['sn'][4:]
    onu_data['onu_mode'] = onu_details['mode']
    onu_data['onu_frame'] = '0'
    onu_data['onu_type'] = onu_details['onu_type_name']
    onu_data['onu_slot'] = onu_details['board']
    onu_data['onu_port'] = onu_details['port']
    onu_data['onu_id'] = onu_details['onu']
    onu_data['f/s/p'] = f"{onu_data['onu_frame']}/{onu_data['onu_slot']}/{onu_data['onu_port']}"
    onu_data['onu_contract'] = onu_details['name'][-10:]
    onu_data['client_name'] = onu_details['name'][:-10]
    
    if len(onu_data['client_name'].split(' '))  == 1:
        onu_data['client_name_1'] = onu_data['client_name'].split(' ')[0]
        onu_data['client_name_2'] = 'Sin Apellido'
    elif len(onu_data['client_name'].split(' ')) == 2:
        onu_data['client_name_1'] = onu_data['client_name'].split(' ')[0]
        onu_data['client_name_2'] = onu_data['client_name'].split(' ')[1]
    else:
        onu_data['client_name_1'] = onu_data['client_name'].split(' ')[0]
        onu_data['client_name_2'] = onu_data['client_name'].split(' ', 1)[1]


    onu_data['olt_name'] = onu_details['olt_name'][-1:]
    onu_data['onu_type_name'] = onu_details['onu_type_name']
    onu_data['onu_mode'] = onu_details['mode']
    onu_data['onu_state'] = 'active' if onu_details['administrative_status'] == 'Enabled' else 'deactivated'

    response = update_client_db(onu_data)
    # response = onu_data['client_name_2']
    return response

def update_client_db(data):

    request = session.query(client_db).filter(client_db.contract == data['onu_contract']).first()
    if request == None:
        request_add = add_client_db(data)
        return request_add
    else:
        #UPDATE DATA IN POSGRESTSQL DEFINITIOS
        request.frame = data['onu_frame']
        request.slot = data['onu_slot']
        request.port  = data['onu_port']
        request.onu_id = data['onu_id']
        request.olt = data['olt_name']
        request.fsp = data['f/s/p']
        request.fspi = data['f/s/p'] +'/'+ data['onu_id']
        request.name_1 = data['client_name_1']
        request.name_2 = data['client_name_2']
        request.state = data['onu_state']
        request.sn = data['onu_sn']
        request.device = data['onu_type_name']
        request.plan_name = plan_type[data['vlan']]
        request.spid = data['service_port']

        #Mandar valores a guardar
        session.add(request)
        session.commit()
        
        if request > 0:  # Verificar si se actualizó algún registro
            return 'Client update Successfully'
        else:
            # ... (manejar el caso donde no se encontró el registro)
            return 'Client update Successfully'

    

def add_client_db(data):

    client = client_db(contract=data['onu_contract'],
                       frame=data['onu_frame'],
                       slot=data['onu_slot'],
                       port=data['onu_port'],
                       onu_id=data['onu_id'],
                       olt=data['olt_name'],
                       fsp=data['f/s/p'],
                       fspi=data['f/s/p'] +'/'+ data['onu_id'],
                       name_1=data['client_name_1'],
                       name_2=data['client_name_2'],
                       state=data['onu_state'],
                       sn=data['onu_sn'],
                       device=data['onu_type_name'],
                       plan_name = plan_type[data['vlan']],
                       spid = data['service_port'])
    
    
    #Mandar valores a guardar
    session.add(client)
    session.commit()
     
    if client > 0:  # Verificar si se actualizó algún registro
        return 'Client add Successfully'
    else:
        # ... (manejar el caso donde no se encontró el registro)
            return 'Client add Successfully'


def update_all_client_db(data):

    result = session.query(client_db).filter(client_db.contract == data['onu_contract']).update({
                       'frame':data['onu_frame'],
                       'slot':data['onu_slot'],
                       'port':data['onu_port'],
                       'onu_id':data['onu_id'],
                       'olt':data['olt_name'],
                       'fsp':data['f/s/p'],
                       'fspi':data['f/s/p'] +'/'+ data['onu_id'],
                       'name_1':data['client_name_1'],
                       'name_2':data['client_name_2'],
                       'state':data['onu_state'],
                       'sn':data['onu_sn'],
                       'device':data['onu_type_name'],
                       'plan_name': plan_type[data['vlan']],
                       'spid': data['service_port']
    # ... (otros atributos a actualizar)
    })

    session.commit()

    if result > 0:  # Verificar si se actualizó algún registro
        return 'Client Update Successfully'
    else:
        # ... (manejar el caso donde no se encontró el registro)
            return 'Client No Successfully'