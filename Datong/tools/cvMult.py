# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import pyzbar.pyzbar as pyz


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
    def mid_process(upper_list):
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
        # get a normal list
        y0, y1, x0, x1 = int(sign[1]), int(sign[-1]), int(sign[-2]), int(sign[2])
        # switch negative
        final_li = CvMultMethod.mid_process([y0, y1, x0, x1])
        y0, y1, x0, x1 = final_li[0], final_li[1], final_li[2], final_li[-1]
        return ci_data_image[y0:y1, x0:x1]

