# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import sys
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import pyzbar.pyzbar as pyz
sys.dont_write_bytecode = True


class CvMultMethod:


    @staticmethod
    def byte2ndarray(b2n_data_image):
        """Convert buffer to ndarray"""
        one_array = np.frombuffer(b2n_data_image, np.uint8)
        return cv2.imdecode(one_array, cv2.IMREAD_COLOR)


    @staticmethod
    def ndarray2byte(ndarray_image):
        """Convert ndarray to byte"""
        img_barray = BytesIO()
        Image.fromarray(ndarray_image).save(img_barray, format='PNG', quality=95)
        return img_barray.getvalue()

    @staticmethod
    def barcode_recognition(br_data_image):
        """
        br_data_image: byte data
        return: barcode information
        """
        buf2nday = CvMultMethod.byte2ndarray(br_data_image)
        gray_img = cv2.cvtColor(buf2nday, cv2.COLOR_BGR2GRAY)
        return pyz.decode(gray_img)[0].data.decode('utf-8')

    @staticmethod
    def crop_process(upper_list):
        """
        crop middle procee
        upper_list: from function "crop_image"
        return: list without negative
        """
        for x in range(len(upper_list)):
            if upper_list[x] < 0:
                if x == 0: upper_list[1], upper_list[0] = upper_list[1] + abs(upper_list[0]), 0
                if x == 1: upper_list[0], upper_list[1] = upper_list[0] + abs(upper_list[1]), 0
                if x == 2: upper_list[-1], upper_list[2] = upper_list[-1] + abs(upper_list[2]), 0
                if x == -1: upper_list[2], upper_list[-1] = upper_list[2] + abs(upper_list[-1]), 0
        return upper_list

    @staticmethod
    def crop_attendant(img, sign_up, *yyxx):
        """
        output the final crop
        img: image data
        sign_up: index list
        yyxx: y0:y1, x0:x1 possible number
        return: crop image by cv2
        """
        y0 = int(sign_up[yyxx[0]])
        y1 = int(sign_up[yyxx[1]])
        x0 = int(sign_up[yyxx[2]])
        x1 = int(sign_up[yyxx[-1]])
        mid_list = CvMultMethod.crop_process([y0, y1, x0, x1]) # switch negative
        y0, y1, x0, x1 = mid_list[0], mid_list[1], mid_list[2], mid_list[-1]
        return img[y0:y1, x0:x1]

    @staticmethod
    def crop_image(ci_data_image, list_bboxes):
        """
        Get a crop image
        ci_data_image: image data
        list_bboxes: bboxes list [[a,b],[c,d],[e,f],[g,h]]
        return: a crop image by cv2
        """
        # into a composite list
        shapes = np.array(list_bboxes).shape
        # sign = sum(list_bboxes, [])
        sign = sum(list_bboxes, []) if len(shapes) != 1 else list_bboxes
        crop_one = np.array([])
        possible = [(1, -1, -2, 2), (3, -1, 0, -2), (-1, 1, 2, -2), (-1, 3, -2, 0)]
        for pos in possible:
            if crop_one.size: break
            a, b, c, d = pos[0], pos[1], pos[2], pos[-1]
            crop_one = CvMultMethod.crop_attendant(ci_data_image, sign, a, b, c, d)
        return crop_one

    @staticmethod
    def vertical_horizontal(img_list, v_h, interpolation=cv2.INTER_CUBIC):
        """
        img_list: [img1, img2, img3...]
        v_h: v or h (vertical & horizontal)
        interpolation:
            INTER_NEAREST 最近邻插值
            INTER_LINEAR 双线性插值（默认设置）
            INTER_AREA 使用像素区域关系进行重采样
            INTER_CUBIC 4x4像素邻域的双三次插值
            INTER_LANCZOS4 8x8像素邻域的Lanczos插值
        return: merged image
        """
        w_min = min(img0.shape[1] for img0 in img_list) # take minimum width
        h_min = min(img.shape[0] for img in img_list) # take minimum hight
        im_list_resize = []
        for img1 in img_list: # resizing images
            w_old, h_old = img1.shape[1], img1.shape[0]
            if v_h == 'v': w_h_new = w_min, int(w_min * h_old / w_old)
            elif v_h == 'h': w_h_new = int(w_old * h_min / h_old), h_min
            cvr = cv2.resize(img1, w_h_new, interpolation=interpolation)
            im_list_resize.append(cvr)
        if v_h == 'v': final_vh_img = cv2.vconcat(im_list_resize)
        elif v_h == 'h': final_vh_img = cv2.hconcat(im_list_resize)
        return final_vh_img # return final image
