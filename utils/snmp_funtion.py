from pysnmp.hlapi import *
from utils.definitions import map_ports #,state_types
import binascii

from utils.failcheck import fail,check_power, check_sn,check_power_olt,check_equip_id
# from helpers.shows_progress import print_fsp

datos = {}

data = []
OPERATION = {
    "next":nextCmd,
    "get":getCmd,
    "bulk":bulkCmd,
}

# def null_datos():
#     datos.clear()
#     datos = {}
#     # print(datos)

                    
#-------------------REQUEST MASTER --------------------------------------
def SNMP_Master(op,community, host, oid,port,type_request,fsp_inicial="",ont_id=""):
    data.clear()
    iterator = OPERATION[op](
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid+f".{fsp_inicial}.{ont_id}")),
        lexicographicMode=False
    )
    # print(oid+f".{fsp_inicial}.{ont_id}")

    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                fsp = map_ports[varBind[0].prettyPrint().split('.')[-2]]
                ont_id = varBind[0].prettyPrint().split('.')[-1]
                resp = varBind[1].prettyPrint()

                if type_request=="desc":
                    datos[fsp+"-"+ont_id] = {
                            "fsp": fsp,
                            "ont_id": ont_id,
                            "rxont": "",
                            "rxolt": "",
                            "sn":"",
                            "state": "",
                            "name": resp,
                            "contract": resp.split()[-1],
                            "distance": "",
                            "ST":'',
                        } 
                
                # elif type_request=="state":
                #     if resp in state_types:
                #         datos[fsp+"-"+ont_id]['state'] =state_types[resp]
                elif type_request=="sn":
                    # print(f"{fsp} , {ont_id} , {resp}")
                    data.append({"f/s/p":fsp,
                                "ont_id":ont_id,
                                "f/s/p_oid":varBind[0].prettyPrint().split('.')[-2],
                                "sn":check_sn(resp),
                                })

                elif type_request=="pw_ont":
                    rxont = check_power(resp)
                    # print(f"rxont {rxont}")
                    return rxont
                    # datos[fsp+"-"+ont_id]['rxont'] = check_power(resp)
                elif type_request=="pw_olt":
                    # print("olt: ",check_power_olt(resp))
                    rxolt = check_power_olt(resp)
                    # print(f"rxolt {rxolt}")
                    return rxolt
                elif type_request=="equi_id":
                    equip_id_register =  resp
                    return equip_id_register
    return data