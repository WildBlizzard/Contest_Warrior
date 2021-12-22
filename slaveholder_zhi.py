# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import os
import sys
import json
sys.dont_write_bytecode = True
from Datong.peon_zhi import Peons


holder = 'holder_zhi.json'
with open(holder, 'r', encoding='utf8') as cs:
    configs = json.load(cs)

labels = os.path.join(configs['Data'], 'Labels')
images = os.path.join(configs['Data'], 'Images')
sub_sce = configs['Scene']
main_sce = configs['Scene_Main']
service_eng = configs['Host&Port']
file_name = configs['Excel_Name']
limit_client_session = configs['Limit_Num'] # 0 是不限制, Windows 下建议 <= 6, Linx 下可根据性能适当提高, 实测 NVIDIA A10 可开至 300

p = Peons(labels, images, sub_sce, main_sce, service_eng, file_name, limit_client_session)
p.work_work()

