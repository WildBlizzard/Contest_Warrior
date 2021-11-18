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
file_name = configs['Excel_Name']
sub_sce = configs['Scene']
main_sce = configs['Scene_Main']
service_eng = configs['Host&Port']

p = Peons(labels, images, sub_sce, main_sce, service_eng, file_name)
p.work_work()