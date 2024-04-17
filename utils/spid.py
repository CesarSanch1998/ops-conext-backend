def calculate_spid(s,p,onu_id):
    SPID = (
        12288 * (int(s) - 1)
        + 771 * int(p)
        + 3 * int(onu_id)
    )
    return {"I": SPID, "P": SPID + 1, "V": SPID + 2}


value = calculate_spid(12,6,0)['I']
print(value)