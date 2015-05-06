import requests
import time
import os
import json
import shlex, subprocess
import glob
import random

CURL = """
curl 'https://demeter.utc.fr/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show' -H 'Host: demeter.utc.fr' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://demeter.utc.fr/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show' -H 'Cookie: portal30=9.0.3+en-us+us+AMERICA+156BDDF999329717E050A8C00A8D21E1+BCD90DA6C8398BE852AC5A869F5593E420E0F545D49306293C2229CB40022D6B2F7A3E2FCFC00547DB2F627C75B26475C983775A8D62E38993BBBDAF8E15ED67DBD19C0FB92393854471376A312262A36C6345C4895E105F; SSO_ID=v1.2~1~9354DA6A47134596986C4CDAEC226A3FC551DAA79DD5A4C2BCE804ABFD1D821A587DFFE6A88858166723E93F46BD873D7DEF4A9568BBC31C22F96B8B545200C352178957E678A0986AC6B58AFA2C15046069D13C72CB0DAF2A6A9264E95335036E09403A299FF823BAD3035CEC087962FDD084EA658CFA553BC9F83078E72E4694336188390397AD6B73AC9589D1ACB25545883F2EA9189C18B23812A253A3DEF3788FC00A3E4DE92488405ABD5AA820F15D179A85D19CC43127FBD4EAECBFA7C9615C37DDC91CB72D5E9797140A9CE3DFE0BF66EBCD1E47189DA1DA4C2EBDAC94A808AC3D14C8BFC9D30FFB3BD98B8E; OSSO_USER_CTX=v1.0~F8486FCA64F7AC05CA3B54D100947505292AF9B851991F76DED93304FED82F1C1AAA16D67D393B26C3E45683AFC0070B3119FE65144A23D493530C8252A6E811A96944E7865E45E46BF48CFEEF315E59F71852D492DE87EF866E41AE613808ECC6761E5D224A7F80' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --data 'p_arg_names=p_action&p_arg_values=3&p_arg_names=p_niveau_stage&p_arg_values=%25&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values=201403&p_arg_names=p_periode_fin&p_arg_values=201403&p_arg_names=p_rech_periode&p_arg_values=semestre&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values={num}&p_arg_names=p_scroll&p_arg_values=0'
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