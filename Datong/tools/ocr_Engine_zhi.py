# --- 虽有多闻 若不修行 与不闻等 如人说食 终不能饱


import os
import sys
import base64
from requests import post
sys.dont_write_bytecode = True


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
        async with self.session.post(self.predict_url, json=data, timeout=1200) as resp:
            return await resp.json()

