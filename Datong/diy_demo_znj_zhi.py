# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import sys
sys.dont_write_bytecode = True
from .tools.regexOut import out
from .compare_zhi import Collector


class Diy(Collector):

    def __init__(self, res_l, img_o, sub_o, main_o, server_o, file_name) -> None:
        super().__init__(res_l, img_o, sub_o, main_o, server_o, file_name)

    def operator_manual(self, lab_got, ocr_got, key_lab):
        # Left label result, Right ocr result
        lab_v, ocr_v = lab_got[key_lab], ocr_got[key_lab]
        lab_m, ocr_m = lab_v, ocr_v
        # ------------ diy area ------------------
        if key_lab == '填发日期':
            ocr_m = out('[^\u4e00-\u9fa5]+', ocr_v)
        # ------------ diy area ------------------
        if lab_m == 'None' and ocr_m == 'None':
            mix_val = 'None'
        elif lab_m == ocr_m:
            mix_val = f'{lab_m}|>..<|{ocr_m}|>..<|True'
        else:
            mix_val = f'{lab_m}|>..<|{ocr_m}|>..<|False'
        return mix_val