# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import re
import os
import sys
import time
import json
import copy
import base64
import random
import asyncio
import aiohttp
import pandas as pd
from math import floor
from requests import post
from typing import Counter
sys.dont_write_bytecode = True
from collections import OrderedDict
from json.decoder import JSONDecodeError


# -------------------------------------------------
data_origin = 'data'
labels_origin = os.path.join(data_origin, 'Labels')
images_origin = os.path.join(data_origin, 'Images')
sub_sce_origin = 'xxxx'
main_sce_origin = 'xxxx'
service_eng_origin = 'http://127.0.0.1:8888/'
file_name_origin = 'my_score'
# -------------------------------------------------


class OCR:

    def __init__(self, server_url, image, main_scene, sub_scene, async_sess=None, vers=None):
        self.server = server_url
        self.img = image
        self.main_sce = main_scene
        self.sub_sce = sub_scene
        self.session = async_sess
        self.vers = vers
        self.sub_predict_url = 'lab/ocr/predict/' + str(self.main_sce)
        self.predict_url = os.path.join(self.server, self.sub_predict_url)

    def data_bs64_encode(self):
        """打开并读取图片，base64加密，ascii解密"""
        # with open(self.img, 'rb') as f:
        #     image_data = base64.b64encode(f.read())
        image_data = base64.b64encode(self.img)
        if self.vers == '105':
            return image_data.decode('ascii').replace('\n', '')
        return image_data.decode()

    def post_request(self):
        """将图片内容与场景名称整个为统一数据"""
        data = {'image': self.data_bs64_encode(), 'scene': self.sub_sce}
        if self.vers == '105':
            return post(self.predict_url, data=data).json()
        data = {'image': self.data_bs64_encode(), 'scene': self.sub_sce, 'parameters': {'vis_flag': False}}
        return post(self.predict_url, json=data).json()

    async def aiohttp_post(self):
        """协程化，异步IO"""
        data = {'image': self.data_bs64_encode(),
                'scene': self.sub_sce, 'parameters': {'vis_flag': False}}
        try:
            async with self.session.post(self.predict_url, json=data, timeout=1200) as resp:
                return await resp.json()
        except Exception: print('aiohttp_post_timeout!')

class RightHand:

    @staticmethod
    def data_arrangement(ori_list, ori_num):
        """
        数据整理
        ori_list: 传入列表
        ori_num: 拆分块基础数量
        return: 传入列表三大件
        """
        one_index = int(len(ori_list) // ori_num)
        three_index = -int(len(ori_list) // ori_num)
        left = ori_list[None:int(one_index)]
        mid = ori_list[int(one_index):int(three_index)]
        right = ori_list[int(three_index):None]
        return left, mid, right

    @staticmethod
    def vegetable_cutter(pre_list, pre_size):
        """
        拆分列表
        pre_list: 传入列表
        pre_size: 期待拆分值
        return: 拆分后的列表
        """
        if pre_size < 1: pre_size = 1
        return [pre_list[i:i+pre_size] for i in range(0, len(pre_list), pre_size)]

    @staticmethod
    def customize_cut_list(da_list, cut_num=3):
        """
        想要的拆分列表
        da_list: 传入列表
        cut_num: 想切成几份，必须大于2
        return: 切好的列表
        """
        if cut_num < 3: cut_num = 3
        in_data = RightHand.data_arrangement(da_list, cut_num)
        if floor(len(in_data[1])/cut_num) == 1 : pass
        else:
            new_r = RightHand.vegetable_cutter(in_data[1], floor(len(in_data[1])/(cut_num - 2)))
            lmr = [in_data[0]]
            for item in new_r: lmr.append(item)
            if len(new_r) != cut_num - 2: in_data[2].extend(lmr.pop())
            lmr.append(in_data[2])
            return lmr
        return in_data

    @staticmethod
    def make_dirs(input_path):
        """
        判断路径是否完整，否则创建对应文件夹，完整路径
        input_path: 输入路径
        return: None
        """
        if not os.path.exists(input_path): os.makedirs(input_path)

    @staticmethod
    def complete_it(open_file_path, save_file_path, index_num, addition=''):
        """
        创建输出路径
        open_file_path: 完整输入路径子路径及文件
        save_file_path: 初始输出路径
        index_num: 初始输入路径长度定位值
        addition: 额外增补路径，默认空
        return: 完整输出路径，子文件夹路径
        """
        # 获取下级目录路径信息，若无则只返回系统分隔符
        end_path = (os.path.split(open_file_path)[0][index_num:]) + os.sep
        # 组合完整输出路径
        final_output = save_file_path + end_path + addition + os.sep
        # 创建输出路径
        RightHand.make_dirs(final_output)
        return final_output, end_path

    @staticmethod
    def through_full_path(origin_path):
        """
        遍历路径，让步产出完整体
        origin_path: 输入路径
        yield: 完整路径
        """
        for root, dirs, files in os.walk(origin_path):
            for name in files: yield os.path.join(root, name)

    @staticmethod
    def get_order_list(input_list, symbol='/', sign_splt='-'):
        """
        获取一个有序的路径列表，文件名需类似此形态：'xxx-1.xxx'，
        input_list: 输入路径（无序）
        symbol: 当前运行系统文件夹分隔符 (已无效，无需输入)
        sign_splt: 以何标识拆分文件名，以区分，默认为 '-'，可变更
        return: 有序路径
        """
        compare_one = [item for item in sorted(RightHand.through_full_path(input_list))]
        compare_two = [int(os.path.split(item)[-1].split('.')[0].split(sign_splt)[-1])
                        for item in sorted(RightHand.through_full_path(input_list))]
        ziplist = zip(compare_one, compare_two)
        return [item[0] for item in sorted([(k, v) for k, v in ziplist], key=lambda x:x[1])]

    @staticmethod
    def get_the_filename(input_path, index_num, extension):
        """
        创建自定义路径末尾文件名及格式
        input_path: 输入路径
        index_num: 路径长度定位值
        extension: 文件扩展名
        return: 想要的文件名
        """
        return '{}.{}'.format(((input_path[index_num:].split(os.sep)[-1]).split('.')[0]), extension)

    @staticmethod
    def random_s():
        """
        获得随机英文加数字组合的字符串
        return: 随机字符串
        """
        str_s = ['' + chr(random.randrange(97, 123)) for i in range(4)]
        str_n = ['' + str(random.randrange(0, 10)) for i in range(3)]
        return ''.join(str_s + str_n)

    @staticmethod
    def out(rule, inp_str):
        """
        正则输出
        rule 正则表达式
        return 筛后字符串
        """
        if not rule: return ''
        regex = re.compile(rule, re.S)
        result_re = regex.findall(inp_str)
        if not result_re: return ''
        elif type(result_re[0]) is str:
            return ''.join(result_re)
        return ','.join(result_re[0])

    @staticmethod
    def calculate_time(func):
        """
        计时装饰器
        """
        def wrapper(*args, **kwargs):
            start_spot = time.perf_counter()
            func(*args, **kwargs)
            final_time = time.perf_counter() - start_spot
            # print('Process "%s" takes %.2f seconds' % (func.__name__, final_time / 60))
            print('It took %.2f seconds' % final_time)

        return wrapper

    @staticmethod
    def electronic_clock(input_seconds):
        """
        电子钟式显示器
        return: 时，分，秒
        """
        pre_minute, second = divmod(input_seconds, 60)
        hour, minute = divmod(pre_minute, 60)
        return hour, minute, second

class Collector:

    def __init__(self, res_l, img_o, sub_o, main_o, server_o, file_name) -> None:
        self.res_l = res_l # Label json result
        self.img_o = img_o # image data
        self.sub_o = sub_o # ocr server sub name
        self.main_o = main_o # ocr server main name
        self.server_o = server_o # ocr server itself
        self.file_name = file_name # image name

    def get_label_res(self): # Label about
        return json.loads(self.res_l) # f.read()

    def mix_useful(self, sts, swh, deal_vals): # Label about
        ready_to_deal = [deal_vals[swh_sgl] for swh_sgl in swh]
        if len(ready_to_deal) != sts:
            print(f'Duplicate label seems strange...\n{ready_to_deal}')
        out_use_val = ''.join(ready_to_deal)
        return out_use_val, ready_to_deal # 2021617, ['2021', '6', '17']

    def del_categroy(self, scate, deal_listb) -> None: # Label about
        for deal_idx in range(len(deal_listb) -1, -1, -1):
            if deal_listb[deal_idx] == scate:
                del deal_listb[deal_idx]

    def del_value(self, del_list, deal_listc) -> None: # Label about
        for deal_idx in range(len(deal_listc) -1, -1, -1):
            if deal_idx in del_list:
                del deal_listc[deal_idx]

    def split_monks_again(self, specll, catss, valss): # Label about
        valss_c = copy.deepcopy(valss)
        reborn_val = []
        should_del_idx = sum([specll_sgl[-1] for specll_sgl in specll], [])
        for item in range(len(valss)):
            if item not in should_del_idx: reborn_val.append(valss[item])
        for sp_sgl1 in specll:
            sp_cate1, sp_times1, sp_where1 = sp_sgl1[0], sp_sgl1[1], sp_sgl1[2]
            # refresh original position of category
            catss.append(sp_cate1)
            # refresh original position of value
            key_vals = self.mix_useful(sp_times1, sp_where1, valss_c)[0]
            reborn_val.append(key_vals)
        return catss, reborn_val

    def deal_special_guy(self, cats, vals, specl): # Label about
        for sp_sgl in specl: # del categroies
            sp_cate = sp_sgl[0]
            self.del_categroy(sp_cate, cats) # delete useless cates
        return self.split_monks_again(specl, cats, vals)

    def split_monks(self, category_list, value_list): # Label about
        frequencies, special_list = Counter(category_list), []
        for ky, ts in frequencies.items():
            if ts > 1:
                sp_wh = [sw for sw in range(len(category_list)) if category_list[sw] == ky]
                special_list.append((ky, ts, sp_wh))
        if special_list:
            sp_guy = self.deal_special_guy(category_list, value_list, special_list)
            category_list, value_list = sp_guy[0], sp_guy[1]
        return dict(zip(category_list, value_list))

    def select_label_res(self): # Label about Final
        label_res = self.get_label_res()
        catt_list = [cates['category'] for cates in label_res]
        vall_list = [values['value'] for values in label_res]
        return self.split_monks(catt_list, vall_list)

    async def get_ocr_res(self, session_3up): # OCR about
        engine_ocr = OCR(self.server_o, self.img_o, self.main_o, self.sub_o, session_3up)
        try:
            # origin_ocr_result = engine_ocr.post_request()
            origin_ocr_result = await engine_ocr.aiohttp_post()
        except TimeoutError: print('Connection aborted, no response.')
        else: return origin_ocr_result

    async def select_ocr_res(self, session_upup): # OCR about Final
        try:
            ocr_res = await self.get_ocr_res(session_upup)
        except JSONDecodeError: print('Expecting value wrong, maybe a mistake.')
        else:
            ocr_res_list = ocr_res['data']['result'][0]['data']
            ename_ocr = [enames['element_name'] for enames in ocr_res_list]
            eval_ocr = []
            for evals in ocr_res_list:
                ocr_yes = evals['element_value']
                if ocr_yes: eval_ocr.append(ocr_yes)
                else: eval_ocr.append('None')
            return dict(zip(ename_ocr, eval_ocr))

    def operator_manual(self, lab_got, ocr_got, key_lab): # Able to Diy
        """
        lab_got: Label value (human did)
        ocr_got: OCR detected value (AI)
        key_lab: which header item input (key of manual)
        """
        # Left label result, Right ocr result
        lab_v, ocr_v = lab_got[key_lab], ocr_got[key_lab]
        lab_m, ocr_m = lab_v, ocr_v
        if lab_m == 'None' and ocr_m == 'None':
            mix_val = 'None'
        elif lab_m == ocr_m:
            mix_val = f'True|>..<|{lab_m}|>..<|{ocr_m}'
        else:
            mix_val = f'False|>..<|{lab_m}|>..<|{ocr_m}'
        return mix_val

    def deal_final_info(self, lgot, ogot, keys_ocr):
        the_apple = OrderedDict()
        the_apple['文件名/准确率'] = self.file_name
        for klab in lgot.keys():
            try:
                mix_val = self.operator_manual(lgot, ogot, klab)
            except KeyError as ke:
                print(f'Label {ke} does not match the remote information, The image is {self.file_name}.')
                return
            the_apple[klab] = mix_val
        return the_apple, keys_ocr

    async def processing_room(self, session_up):
        try: ocrs_got = await self.select_ocr_res(session_up)
        except TypeError: print('ocr return noting...')
        else:
            labs_got = self.select_label_res()
            lab_gather = [k_l for k_l in labs_got.keys()]
            for k_o in ocrs_got.keys(): # Focus, full labels empty plz
                if k_o not in lab_gather: labs_got[k_o] = 'None'
            keys_ocr_set = [key_ocr for key_ocr in ocrs_got.keys()] # set Excel header
            keys_ocr_set.insert(0, '文件名/准确率')
            return self.deal_final_info(labs_got, ocrs_got, keys_ocr_set)

class Maker:

    def __init__(self, baskets, diy_name) -> None:
        self.key_pre = baskets['keys'] # headers
        self.diy_name = diy_name.split('.')[0]
        full_pre = [None for k_idx in self.key_pre] # full headers
        mix_pre = zip(self.key_pre, full_pre) # mix them
        self.frames = OrderedDict(mix_pre)
        self.apples = baskets['apples'] # is a list, includ dict

    def calculate_more(self, an_apple):
        if not an_apple: return 0
        core_score, apple_score = 0, len(an_apple)
        for apple_core in an_apple:
            coco = apple_core.split('|>..<|')[0]
            if coco == 'True': core_score += 1
        return core_score / apple_score

    def calculate_apple(self, apples_up):
        more_new, more_list = 0, []
        for apple_cal in apples_up:
            if apple_cal == 'None': continue
            else: more_list.append(apple_cal)
        more_new = self.calculate_more(more_list)
        apples_up.append(more_new)
        return apples_up

    def apple_process(self, keyss, appless):
        new_apples = []
        for apple in appless:
            for apple_k, apple_v in apple.items():
                if apple_k == keyss:
                    new_apples.append(apple_v)
        if keyss == '文件名/准确率':
            new_apples.append('准确率')
        else:
            new_apples = self.calculate_apple(new_apples)
        return new_apples

    def frame_process(self) -> None:
        for key_frame in self.frames.keys():
            val_frame = self.apple_process(key_frame, self.apples)
            final_value = {key_frame: val_frame}
            self.frames.update(final_value)

    def stats_final_score(self, data_frame):
        score_list0 = data_frame.iloc[-1, 1:]
        score_list = []
        for sco in score_list0:
            if sco > 0: score_list.append(sco)
            continue
        each_score, all_len = 0, len(score_list)
        for score_sgl in score_list: each_score += score_sgl
        try:
            final_score = each_score / all_len
        except ZeroDivisionError:
            final_score = 0
            print('I am sorry, there are no correct answers.')
        data_frame.iloc[-1, 0] = '准确率: {:.3f}'.format(final_score)
        return data_frame

    def make_excel(self) -> None:
        self.frame_process()
        df0 = pd.DataFrame(self.frames)
        df = self.stats_final_score(df0)
        # ValueError: arrays must all be same length
        # df = pd.DataFrame.from_dict(self.frames, orient='index').T
        excel_name = self.diy_name + '.xlsx'
        excel_path = os.path.join('Excels', excel_name)
        RightHand.make_dirs(os.path.split(excel_path)[0])
        try: df.to_excel(excel_path)
        except PermissionError:
            print('Plz shutdown the excel and try again...')
        else: print('Work completed!')

class Diy(Collector):

    def __init__(self, res_l, img_o, sub_o, main_o, server_o, file_name) -> None:
        super().__init__(res_l, img_o, sub_o, main_o, server_o, file_name)

    def operator_manual(self, lab_got, ocr_got, key_lab):
        # Left label result, Right ocr result
        lab_v, ocr_v = lab_got[key_lab], ocr_got[key_lab]
        lab_m, ocr_m = lab_v, ocr_v
        # ------------ diy area ------------------
        period_though = RightHand.out('[\u4e00-\u9fa5]+', key_lab) == '税款所属时期'
        if key_lab == '填发日期' or period_though:
            lab_m = RightHand.out('[^\u4e00-\u9fa5\s]+', lab_v)
            ocr_m = RightHand.out('[^\u4e00-\u9fa5\s]+', ocr_v)
        if key_lab == '完税编号':
            lab_m = lab_v.replace('.', '')
            lab_m = lab_v.replace('.', '')
            ocr_m = ocr_v.replace('税收完税证明', '')
        if key_lab == '填票人':
            lab_m = lab_v.replace('.', '')
            ocr_m = ocr_v.replace('.', '')
        if key_lab == '总金额':
            lab_m = lab_v.replace(lab_v[0], '￥')
            ocr_m = ocr_v.replace(ocr_v[0], '￥')
        if key_lab in ['税种', '税款所属时期', '实缴(退)金额']:
            ocr_m = ocr_v.replace('<..>', '')
            if key_lab == '税款所属时期':
                lab_m = RightHand.out('[^\u4e00-\u9fa5\s]+', lab_v)
                ocr_m = RightHand.out('[^\u4e00-\u9fa5\s]+', ocr_v)
                ocr_m = ocr_m.replace('<..>', '')
        if key_lab in ['实缴(退)金额', '总金额']:
            ocr_m = ocr_v.replace('<..>', '')
            lab_m = lab_v.replace(',', '')
        # ------------ diy area ------------------
        if lab_m == 'None' and ocr_m == 'None':
            mix_val = 'None'
        elif lab_m == ocr_m:
            mix_val = f'True|>..<|{lab_m}|>..<|{ocr_m}'
        else:
            mix_val = f'False|>..<|{lab_m}|>..<|{ocr_m}'
        return mix_val

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

    def is_ok(self, img_path, label_path):
        img_ok = os.path.exists(img_path)
        lab_ok = os.path.exists(label_path)
        if img_ok and lab_ok: return 1

    async def work_leader(self):
        async with aiohttp.ClientSession() as session:
            tasks, the_basket = [], {'apples': [], 'keys': None}
            for img_path in RightHand.through_full_path(self.images):
                img_name = os.path.split(img_path)[-1]
                lab_name = img_name.split('.')[0] + '.json'
                label_path = os.path.join(self.labels, lab_name)
                if self.is_ok(img_path, label_path):
                    with open(label_path, 'r', encoding='utf8') as lda: lab_cont = lda.read()
                    with open(img_path, 'rb') as ida: ida_cont = ida.read()
                    tasks.append(self.work_man_one(the_basket, lab_cont, ida_cont, img_name, session))
                else: return 'Nothing'
            await asyncio.wait(tasks)
            self.work_man_two(the_basket)

    def work_work(self):
        print('----------------- Start the process -----------------\n')
        start = time.perf_counter()
        try: some_thing = asyncio.run(self.work_leader())
        except aiohttp.ClientConnectionError: print('Aiohttp Connection aborted...')
        else:
            if some_thing == 'Nothing':
                print('Input error, stoped the program, please check the data folder.')
        stop = time.perf_counter() - start
        final_show = RightHand.electronic_clock(stop)
        hour, minute, second = final_show[0], final_show[1], final_show[2]
        print('\nTotal time:「 %02d : %02d : %02d 」' % (hour, minute, second))
        print('---------------- Process is completed ---------------')


if __name__ == '__main__':
    peo = Peons(labels_origin, images_origin, sub_sce_origin,
                main_sce_origin, service_eng_origin, file_name_origin)
    peo.work_work()