from utils.definitions import ERRORS
from utils.definitions import snmp_down_causes

def fail(texto):
    
    if texto not in ERRORS:
        return texto
    else:
        return "-"
    
def check_power(power):
    if power != "2147483647":
        f_power = (float(power)/100)
        return f_power
    else:
        f_power = "0"
        return f_power

def check_power_olt(power):
    if power != "2147483647":
        f_power = (((float(power)) - 10000)/100)
        return f_power
    else:
        f_power = "0"
        return f_power

def check_sn(sn):
    return sn[2:]

def check_equip_id(equip_id):
    return equip_id[2:]

