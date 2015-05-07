import requests
import time
import os
import json
import shlex, subprocess
import glob
import random

CURL = """
curl 'https://demeter.utc.fr/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show' -H 'Host: demeter.utc.fr' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://demeter.utc.fr/pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show' -H 'Cookie: portal30=9.0.3+en-us+us+AMERICA+157F98D79AA5F995E050A8C00A8D7C3A+B667755FDE656955F383FBBBE45A280C8785F8E2408652F3DDF099F41AA02A75FAB75729B20AEBD79AF0B52A61410720630F36CC64356DD2F7C02DCF11298DDD4F8F1ABBF3BF77BAEA00AB276BF9B87CD9FF2540585025D9; SSO_ID=v1.2~1~66DA32DA285898D7636E0C1F31AC0E15DDAEACC991A45F27FFF77794E0E1D9C60408387AA9A6B73D732AC5E71EAC8FFBF19EEB2C5981C65356D7259E04A7D174BA79F5B7DA29B8130E1BB1CE2B52F160283DC99EEBDA89E15AB563513A24F6ECF13D267EA16753BD9DE1B991E699310E1A02E02E33F24BEEDB41F6A359997191890A135546546EE85D9D1F4B5627AEAB91BC42BC7CF6F4DFF91E3551FF0C3D040C8BA42290FD0BB5998FA2500A33B5175EF3C4B2AB3908F00837E64FFEA0CD9F539270CBC482911899C1B1CD033ABE80F76151CA9939DDA02D75687F3A8966FC5DC968C08F65BAC2; OSSO_USER_CTX=v1.0~6D7AEC1A9CB90BF124F883EF26A41814759EE9A7583349C06CF645E17D1D2314FA9AD958ED9096703C167145AA376DA854FE7871FE217982EB448EE0DA8C73D2C1AC596F3201ECDDE8CB087171E1F0D7BB4884380DB87BFBC50288553BFA0467F3AB474F85979339' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --data 'p_arg_names=p_action&p_arg_values=3&p_arg_names=p_niveau_stage&p_arg_values=%25&p_arg_names=p_spec&p_arg_values=%25&p_arg_names=p_option&p_arg_values=%25&p_arg_names=p_mot&p_arg_values=%25&p_arg_names=p_periode_debut&p_arg_values=201403&p_arg_names=p_periode_fin&p_arg_values=201403&p_arg_names=p_rech_periode&p_arg_values=semestre&p_arg_names=p_pays&p_arg_values=%25&p_arg_names=p_nom_commune&p_arg_values=&p_arg_names=p_region&p_arg_values=%25&p_arg_names=p_dept&p_arg_values=%25&p_arg_names=p_domaine&p_arg_values=%25&p_arg_names=p_ape&p_arg_values=%25&p_arg_names=p_no_etu&p_arg_values=N&p_arg_names=p_with_etu&p_arg_values=O&p_arg_names=p_prop_id&p_arg_values={num}&p_arg_names=p_scroll&p_arg_values=0'
"""

def get_dones():
    l = set()
    for filename in glob.glob('STAGES/*'):
        l.add(int(filename.split('/')[1].strip()))
    return l

nums = set(list(open('data/nums_to_do')))
nums = [int(n.strip()) for n in nums]
random.shuffle(nums)

dones = get_dones()
for i, num in enumerate(nums):
    if num in dones:
        continue
    print(num,':', len(dones),'/',len(nums))
    out = subprocess.Popen(CURL.format(num=num), shell=True, stdout=subprocess.PIPE).stdout.read()
    html = out.decode(encoding='iso-8859-15')
    if '<INPUT TYPE="hidden" NAME="p_arg_names" VALUE="p_action">' not in html:
        print('session expired')
        break
    with open("STAGES/{num}".format(num=num),'wb') as f:
        f.write(out)
    print("out",num)
    dones = get_dones()