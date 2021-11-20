# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱

from json.decoder import JSONDecodeError
import os
import sys
import copy
import json
import pandas as pd
from typing import Counter
sys.dont_write_bytecode = True
from collections import OrderedDict
from .tools.ocrService import OCR
from .tools.completeOther import make_dirs


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

    def mix_useful(self, sts, swh, deal_lista): # Label about
        out_use_list = deal_lista[swh:swh+sts]
        out_use_val = ''.join(out_use_list)
        return out_use_val, out_use_list # 2021617, ['2021', '6', '17']

    def del_categroy(self, scate, deal_listb) -> None: # Label about
        for deal_idx in range(len(deal_listb) -1, -1, -1):
            if deal_listb[deal_idx] == scate:
                del deal_listb[deal_idx]

    def del_value(self, del_list, deal_listc) -> None: # Label about
        for deal_idx in range(len(deal_listc) -1, -1, -1):
            if deal_idx in del_list:
                del deal_listc[deal_idx]

    def split_monks_again(self, specll, valdd, catss, valss): # Label about
        for sp_sgl1 in specll:
            sp_cate1, sp_times1, sp_where1 = sp_sgl1[0], sp_sgl1[1], sp_sgl1[2]
            # refresh original position of category
            catss.append(sp_cate1)
            # refresh original position of value
            key_vals = self.mix_useful(sp_times1, sp_where1, valdd)[0]
            valss.append(key_vals)
        return catss, valss

    def deal_special_guy(self, cats, vals, specl): # Label about
        vald = copy.deepcopy(vals)
        should_del = []
        for sp_sgl in specl: # del categroies
            sp_cate, sp_times, sp_where = sp_sgl[0], sp_sgl[1], sp_sgl[2]
            self.del_categroy(sp_cate, cats)
            should_del.append(list(range(sp_where, sp_where+sp_times)))
        should_del = sum(should_del, [])
        self.del_value(should_del, vals) # del values
        return self.split_monks_again(specl, vald, cats, vals)

    def split_monks(self, category_list, value_list): # Label about
        frequencies, special_list = Counter(category_list), []
        for ky, ts in frequencies.items():
            if ts > 1:
                sp_wh = category_list.index(ky)
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

    def get_ocr_res(self): # OCR about
        engine_ocr = OCR(self.server_o, self.img_o, self.main_o, self.sub_o)
        try:
            origin_ocr_result = engine_ocr.post_request()
        except TimeoutError: print('Connection aborted, no response')
        else: return origin_ocr_result

    def select_ocr_res(self): # OCR about Final
        try:
            ocr_res = self.get_ocr_res()
        except JSONDecodeError: print('Expecting value wrong, maybe a mistake')
        else:
            ocr_res_list = ocr_res['data']['result'][0]['data']
            ename_ocr = [enames['element_name'] for enames in ocr_res_list]
            # eval_ocr = [evals['element_value'] for evals in ocr_res_list]
            eval_ocr = []
            for evals in ocr_res_list:
                ocr_yes = evals['element_value']
                if ocr_yes: eval_ocr.append(ocr_yes)
                else: eval_ocr.append('None')
            # self.all_ocr_cates = ename_ocr
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
            mix_val = self.operator_manual(lgot, ogot, klab)
            the_apple[klab] = mix_val
        return the_apple, keys_ocr

    def processing_room(self):
        ocrs_got = self.select_ocr_res()
        labs_got = self.select_label_res()
        lab_gather = [k_l for k_l in labs_got.keys()]
        for k_o in ocrs_got.keys(): # Focus, full labels empty plz
            if k_o not in lab_gather: labs_got[k_o] = 'None'
        # set Excel header
        keys_ocr_set = [key_ocr for key_ocr in ocrs_got.keys()]
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
        make_dirs(os.path.split(excel_path)[0])
        try: df.to_excel(excel_path)
        except PermissionError:
            print('Plz shutdown the excel and try again...')
        else: print('Work completed!')