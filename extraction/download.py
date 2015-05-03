import requests
import time
import os
import json
import shlex, subprocess
import glob
import random

CURL = """
curl 'https://demeter.utc.fr/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show' -H 'Host: demeter.utc.fr' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://demeter.utc.fr/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show' -H 'Cookie: portal30=9.0.3+en-us+us+AMERICA+153125AC431F919BE050A8C00A8D7611+3F051AF381E72954EA04F6F04D29E9FEAEE4E05E50114CB9EBCB273EA1984C436F4C9324B2BEEB319C15973AC584CEAC6A05F12E32B3A9CD103A3A5FF6208DA5B8F7806193E3A4824160C937F9D85E94337D320370BB8BC3; SSO_ID=v1.2~1~BA8D9687786B634725449BC851C63286E76C6F7EF463CCF725819C8E9C15938888619A6A2A938FE4F207BCCBD080A16E5DFF633B572E2E7B8EB059641A158F4FEE24228C28FBD687262567968F6AE0446CF23C8C25F3E1FB3F3F3994D5F162504D88974A7FC5B1BE56BEB405EB322873434D5BBA942C9C01E7337704016641F0AF6E0BE772B15E47CB059D43CA3908348A4036E4F6266A8DB42C390FD167AD1A341D95F338053B05CA8504061544E59253A1E52DC8656D88492A9C8EE5370E172AC54C3F45032809473B67F075EC2F6E581A3EC09D6D2234F7B4D13FBB72D9E0F68BA962AF0006AD90411CEFB8F2A1FB; OSSO_USER_CTX=v1.0~582F74C54244FFF7204235FE9CDB1396D878F7613A3DA6593A7883C0B3E8BD0D03DAA85B064A273B4FA98750D16EF2FF53C8D3C3097E67128E2515ED8A66B8D114F192A849D36A842CA2A8FC1F301C555C9A115B745A3DCE551EE79C9E256701B93A0C0B9CE14C07' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --data 'p_arg_names=p_action&p_arg_values=3&p_arg_names=p_niveau_stage&p_arg_values=%25&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values=201403&p_arg_names=p_periode_fin&p_arg_values=201403&p_arg_names=p_rech_periode&p_arg_values=semestre&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values={num}&p_arg_names=p_scroll&p_arg_values=0'
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