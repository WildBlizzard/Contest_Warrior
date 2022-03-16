# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import os
import sys
import time
import json
import asyncio
import aiohttp
sys.dont_write_bytecode = True
from .compare_zhi import Maker
from .compare_zhi import Collector
from .diy_demo_znj_zhi import Diy
from collections import OrderedDict
from .tools.right_Hand_zhi import RightHand


class Peons:

    def __init__(self, labels, images, sub_sce, main_sce, service_eng, excel_name, lt_cs=3, to_cs=600) -> None:
        self.labels = labels
        self.images = images
        self.sub_sce = sub_sce
        self.main_sce = main_sce
        self.service_eng = service_eng
        self.excel_name = excel_name
        self.lico = aiohttp.TCPConnector(limit=lt_cs)
        self.tter = aiohttp.ClientTimeout(total=to_cs)

    def work_man_two(self, the_basket_up):
        if the_basket_up['keys'] == 'None':
            print('Please check the error label.')
            return None
        elif not the_basket_up['keys']:
            print('Please check the data folder, it seems like empty.')
            return None
        m = Maker(the_basket_up, self.excel_name)
        m.make_excel()

    async def work_man_one(self, basket, lab_cont, ida_cont, img_name, session): # diy here
        # ------------ diy area ------------------
        # c = Collector(lab_cont, ida_cont, self.sub_sce,
        #             self.main_sce, self.service_eng, img_name)
        # res = await c.processing_room(session)
        d = Diy(lab_cont, ida_cont, self.sub_sce,
                    self.main_sce, self.service_eng, img_name)
        res = await d.processing_room(session)
        # ------------ diy area ------------------
        try: apple_c, key_c = res[0], res[1]
        except TypeError:
            apple_c, key_c = {'None': 'None'}, 'None'
        basket['apples'].append(apple_c)
        basket['keys'] = key_c

    def deal_empty(self, the_basket_up, empty_list):
        apples_b, banana_h = the_basket_up['apples'], OrderedDict()
        for empty_f in empty_list: # 获取空标注的图片
            name_empty = os.path.split(empty_f)[-1] # image name
            banana_h['文件名/准确率'] = name_empty
            for k_apple in apples_b[0].keys():
                if k_apple == '文件名/准确率': continue
                banana_h[k_apple] = 'None'
            apples_b.append(banana_h)

    def is_ok(self, img_path, label_path, epts_up):
        img_ok = os.path.exists(img_path)
        lab_ok = os.path.exists(label_path)
        with open(label_path, encoding='utf8') as lab_file:
            lab_inside = json.load(lab_file)
        if not lab_inside: epts_up.append(img_path)
        if img_ok and lab_ok and lab_inside: return 1

    async def work_leader(self):
        async with aiohttp.ClientSession(connector=self.lico, timeout=self.tter) as session:
            tasks, epts, the_basket = [], [], {'apples': [], 'keys': None}
            for img_path in RightHand.through_full_path(self.images):
                img_name = os.path.split(img_path)[-1]
                lab_name = img_name.split('.')[0] + '.json'
                label_path = os.path.join(self.labels, lab_name)
                if self.is_ok(img_path, label_path, epts):
                    with open(label_path, 'r', encoding='utf8') as lda: lab_cont = lda.read()
                    with open(img_path, 'rb') as ida: ida_cont = ida.read()
                    tasks.append(self.work_man_one(the_basket, lab_cont, ida_cont, img_name, session))
            await asyncio.gather(*tasks)
            if epts: self.deal_empty(the_basket, epts) # 处理空标注数据
            self.work_man_two(the_basket)

    def work_work(self):
        print('----------------- Start the process -----------------\n')
        start = time.perf_counter()
        try:
            # asyncio.run(self.work_leader())
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.work_leader())
        except aiohttp.ClientConnectionError :
            print('Network Error or lower tne "limit_client_session"')
        stop = time.perf_counter() - start
        final_show = RightHand.electronic_clock(stop)
        hour, minute, second = final_show[0], final_show[1], final_show[2]
        print('\nTotal time:「 %02d : %02d : %02d 」' % (hour, minute, second))
        print('---------------- Process is completed ---------------')
