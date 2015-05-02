import requests
import time
import os
import json
import shlex, subprocess
import glob
import random

CURL = """
curl 'https://demeter.utc.fr/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show' -H 'Host: demeter.utc.fr' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://demeter.utc.fr/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show' -H 'Cookie: portal30=9.0.3+en-us+us+AMERICA+15064640CDA92344E050A8C00A8D3B15+18539210C841B117F3C609A35BBAA279792E4E897CF1C43C183A15A21256ED65939607741C2E28141BE1B6AA65BE93B90EBA5647A611F652575E6EDB3020B5D843734349FFA211B63D1DB160D129511094881CB2BFB329B5; SSO_ID=v1.2~1~D25D9CCCD3A927D5790AEB6CC1E8F68FE04DD3D796FA1ABB29AD2836FD35148199CB47C03A03060C956D84CA024C0876901443F7E152942796B93EE1344CA7F476E000A2DD7FB0A62ED582380AD342C79DEE4E3E1B788E1816766083A839FB94B25FD4515F282721B6CAA4FE4BFCC55F90B57122D7B22838C2E18BD966BE8E80E14479F6D0F51557CB6F49C86D926245B882765C84A179A7D2C7F3DC0D558FB4FCEFFC5623C04768DB0F94B73D08181F979DCFBA7B35944D314D6430A67682FBFBE1585FDBBE08B5DBD184030D8771175878DCB682219ED911CD7C972159F721E2AC3A6D12B7D978; OSSO_USER_CTX=v1.0~72C5C51A8AA9C1EC024B7C88632CE938E37E28C8659D5D309E8BB82D7E6F33F8194B19BC6D9977DEC6EB82EACA1A0EAAA4CF115F6E2248CF2BC954BBC3421135EBDBAAB031178D964E8C5B592CF78322CDA6052422C57862F1A3A76CB06160EBD2D1A102DE6FF124' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --data 'p_arg_names=p_action&p_arg_values=3&p_arg_names=p_niveau_stage&p_arg_values=%25&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values=201403&p_arg_names=p_periode_fin&p_arg_values=201403&p_arg_names=p_rech_periode&p_arg_values=semestre&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values={num}&p_arg_names=p_scroll&p_arg_values=0'
"""

def get_dones():
    l = set()
    for filename in glob.glob('STAGES/*'):
        l.add(filename)
    return l

nums = list(open('data/nums_to_do'))
nums = [int(n.strip()) for n in nums]
random.shuffle(nums)

dones = get_dones()
for i, num in enumerate(nums):
    if num in dones:
        print(num, 'already done')
        continue
    print(num,':', len(dones),'/',len(nums))
    out = subprocess.Popen(CURL.format(num=num), shell=True, stdout=subprocess.PIPE).stdout.read()
    html = out.decode(encoding='iso-8859-15')
    if '<INPUT TYPE="hidden" NAME="p_arg_names" VALUE="p_action">' not in html:
        print('session expired')
        break
    with open("STAGES/{num}".format(num=num),'wb') as f:
        f.write(out)
    print("out len",len(out))
    dones = get_dones()