# --- Namo tassa bhagavato arahato sammāsambuddhassa


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
        # ------------ diy area ------------------
        if lab_m == 'None' and ocr_m == 'None':
            mix_val = 'None'
        elif lab_m == ocr_m:
            mix_val = f'True|>..<|{lab_m}|>..<|{ocr_m}'
        else:
            mix_val = f'False|>..<|{lab_m}|>..<|{ocr_m}'
        return mix_val