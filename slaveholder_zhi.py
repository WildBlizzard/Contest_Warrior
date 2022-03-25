# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import os
import sys
import json
import time
sys.dont_write_bytecode = True
from Datong.peon_zhi import Peons


print('-------------------------------------------------------')
print('\n-- Author: zhiq')
print('-- This is Contest Warrior v1.2')
print('-- Watch the project in my github:\n\0\0\0"https://github.com/WildBlizzard/Contest_Warrior"\n')
print('-- 请将标注文件与图片分别放在数据文件夹(默认“data”)下的“Labels”与“Images”中')
print('-- 默认数据文件夹名为"data"，其目录下应存在“Labels”与“Images”(这两个名字不可变)')
print('-- 如存在配置文件“holder_zhi.json”则会询问是否跳过输入项，默认跳过\n')
print('-------------------------------------------------------\n')

current_dir_path = os.getcwd()
is_config = os.path.exists(os.path.join(current_dir_path, 'holder_zhi.json'))
chose_config = input('检测到配置文件存在，是否跳过手动输入？(回车默认跳过，输入任意字符开始手动输入): ')
print()

if is_config and not chose_config:
    holder = 'holder_zhi.json'
    with open(holder, 'r', encoding='utf8') as cs: configs = json.load(cs)

    labels = os.path.join(configs['Data'], 'Labels')
    images = os.path.join(configs['Data'], 'Images')
    sub_sce = configs['Scene']
    main_sce = configs['Scene_Main']
    service_eng = configs['Host&Port']
    file_name = configs['Excel_Name']
    limit_client_session = configs['Limit_Num'] # 0 是不限制, Windows 下建议 <= 6, Linx 下可根据性能适当提高, 实测 NVIDIA A10 可开至 300
else:
    default_data = os.path.join(current_dir_path, 'data')
    default_labs, default_imgs = os.path.join(default_data, 'Labels'), os.path.join(default_data, 'Images')
    inp_data = input('1. 请输入数据文件夹名(回车即默认“data”): ')
    labels = default_labs if not inp_data else os.path.join(current_dir_path, inp_data, 'Labels')
    images = default_imgs if not inp_data else os.path.join(current_dir_path, inp_data, 'Images')

    file_name, limit_client_session = input('2. 请输入产出Excel文件名(回车即默认“my_score”): '), 3
    file_name = 'my_score' if not file_name else file_name

    main_sce = input('3. (必选项)请输入主场景名称(如“ticket”): ')
    while not main_sce: main_sce = input('必须输入主场景名称(如“ticket”、“bill”): ')
    sub_sce = input('4. (必选项)请输入细分场景名称(如“invoice_taxi”): ')
    while not sub_sce: sub_sce = input('必须输入细分场景名称(如“invoice_taxi”等): ')
    service_eng = input('5. (必选项)请输入OCR服务地址(务必保证当前机器与之相互连通): ')
    while not service_eng: service_eng = input('必须输入OCR服务地址(如“http://188.88.88.88:8506/”): ')
    print()


p = Peons(labels, images, sub_sce, main_sce, service_eng, file_name, limit_client_session)
p.work_work()

print('5秒后关闭本程序......')
time.sleep(5)