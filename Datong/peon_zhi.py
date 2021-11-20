# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import os
import sys
import time
sys.dont_write_bytecode = True
from .compare_zhi import Maker
from .diy_demo_znj_zhi import Diy # diy manually
from .compare_zhi import Collector
from Datong.tools.showTime import electronic_clock
from .tools.getFullPath import through_full_path as tp


class Peons:

    def __init__(self, labels, images, sub_sce, main_sce, service_eng, excel_name) -> None:
        self.labels = labels
        self.images = images
        self.sub_sce = sub_sce
        self.main_sce = main_sce
        self.service_eng = service_eng
        self.excel_name = excel_name

    def work_man_two(self, the_basket_up):
        if the_basket_up['keys'] == 'None':
            print('Please check the error label.')
            return None
        elif not the_basket_up['keys']:
            print('Please check the data folder,\
                    \nit seems like empty.')
            return None
        m = Maker(the_basket_up, self.excel_name)
        m.make_excel()

    def work_man_one(self, basket, lab_cont, ida_cont, img_name): # diy here
        # c = Collector(lab_cont, ida_cont, self.sub_sce,
        #             self.main_sce, self.service_eng, img_name)
        # res = c.processing_room()
        d = Diy(lab_cont, ida_cont, self.sub_sce,
                    self.main_sce, self.service_eng, img_name)
        res = d.processing_room() # diy manually
        try:
            apple_c, key_c = res[0], res[1]
        except TypeError:
            apple_c, key_c = {'None': 'None'}, 'None'
        basket['apples'].append(apple_c)
        basket['keys'] = key_c

    def is_ok(self, img_path, label_path):
        img_ok = os.path.exists(img_path)
        lab_ok = os.path.exists(label_path)
        if img_ok and lab_ok: return 1

    def work_leader(self):
        the_basket = {'apples': [], 'keys': None}
        for img_path in tp(self.images):
            img_name = os.path.split(img_path)[-1]
            lab_name = img_name.split('.')[0] + '.json'
            label_path = os.path.join(self.labels, lab_name)
            if self.is_ok(img_path, label_path):
                with open(label_path, 'r', encoding='utf8') as lda:
                    lab_cont = lda.read()
                with open(img_path, 'rb') as ida: ida_cont = ida.read()
                self.work_man_one(the_basket, lab_cont, ida_cont, img_name)
            else: return 'Nothing'
        self.work_man_two(the_basket)

    def work_work(self):
        print('----------------- Start the process -----------------\n')
        start = time.perf_counter()
        some_thing = self.work_leader()
        if some_thing == 'Nothing':
            print('Input error, stoped the program,\
                    please check the data folder.')
        stop = time.perf_counter() - start
        final_show = electronic_clock(stop)
        hour, minute, second = final_show[0], final_show[1], final_show[2]
        print('\nTotal time:「 %02d : %02d : %02d 」' % (hour, minute, second))
        print('---------------- Process is completed ---------------')


