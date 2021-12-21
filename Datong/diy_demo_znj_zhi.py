# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import sys
sys.dont_write_bytecode = True
from .tools.right_Hand_zhi import RightHand
from .compare_zhi import Collector


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
