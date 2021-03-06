# Contest_Warrior

Version：1.2

Python：3.8.5

Pandas：1.3.1

Openpyxl：3.0.7

Requests：2.24.0

Aiohttp：3.8.1 （3.6.2+）



对比 AutoOCR 标注与服务端返回信息值的正确率与细节，在易用性与可视化方面完全领先 AutoOCR 产品内部 inference，v1.2 采用了异步IO，使得效率较之前大幅提高（速度是 v1.1 的 2倍+），但受限于不同平台性能有别，故使用时应注意 session 限制，Windows 下 3 较为合适。



### 请注意：

现阶段本程序在配置较低的机器上处理的文件较多时可能出现”内存泄漏“的情况，其原因是获取OCR结果后暂时存放的位置都堆在了内存中，正在尝试解决该问题（寻找更好的存储方式，待选项为：外写json(无更多工具需求)、数据库(代码环境需求增大)），相关问题代码位置：Datong/compare_zhi.py



### 使用方法：

直接使用一键版：**ContestWarrior_OneStep_Async_v1.2_zhi.py**，修改其头部如下信息，然后python它。

```python
# -------------------------------------------------
data_origin = 'data' # 指定输入路径，其下必有固定名字两个文件夹 Images, Labels
labels_origin = os.path.join(data_origin, 'Labels')
images_origin = os.path.join(data_origin, 'Images')
sub_sce_origin = 'xxxx' # 场景 Scene
main_sce_origin = 'xxxx'  # Scene 上级，如 ticket
service_eng_origin = 'http://127.0.0.1:8888/' # 请求URL，注意最后一定要有 "/"
file_name_origin = 'my_score' # 最后输出的Excel名，默认输出到当前路径下 Excels
limit_client_session = 3 # 0 是不限制; Windows 下建议 <= 6; Linx 下可根据性能适当提高, 实测 NVIDIA A10 可开至 300
# -------------------------------------------------
```

或使用正式版……

创建并编辑 **holder_zhi.json** 。

```json
{
  "Data": "data", # 指定输入路径，其下必有固定名字两个文件夹 Images, Labels
  "Scene": "xxxx", # 场景 Scene
  "Scene_Main": "xxxx", # Scene 上级，如 ticket
  "Host&Port": "http://127.0.0.1:2021/", # 请求URL，注意最后一定要有 "/"
  "Excel_Name": "my_score", # 最后输出的Excel名，默认输出到当前路径下 Excels
  "Limit_Num": 6 # 0 是不限制; Windows 下建议 <= 6; Linx 下可根据性能适当提高, 实测 NVIDIA A10 可开至 300
}
```

确认图片与标注结果数量相等一一对应后，将其分别放在 **data/Images** 和 **data/Labels** 下。

然后启动入口文件 **slaveholder_zhi.py** 。

```python
python slaveholder_zhi.py
```

等待程序结束，如无意外终端会打印 **"Work completed!"**，即代表成功。

生成的 **excel** 在当前目录 **Excels** 下。



### 进阶玩法：

考虑到人工标注的数据和最终 **OCR** 结果在一些字段上多少会存在差异，故开放了一个类方法用以根据实际情况适时调整双方数据的最终形态，方便程序对比与计算最终分值。

大体思路是：重写我的**收集类方法**，将**重写好的类**替换其之前的工作位置，完成diy规则。

详细信息可参考包内三个文件：**peon_zhi.py**，**compare_zhi.py**，**diy_demo_znj_zhi.py**。

其中 **peon_zhi.py** 的 **work_man_one** 方法是替换类的工作位置。

```python
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
```

**Collector** 是原始的数据处理类，其下的 **operator_manual** 方法是关键，重写该方法即可达成效果，详情请对比 **compare_zhi.py**，**diy_demo_znj_zhi.py**，一目了然。



### 分数计算方法：

每个字段对比，单项正确为 **True** 加一分，否则 **False** 不加分，本身没有提取结果也不加分，最后根据本列（也就是一个字段）的分数除以总项数获得最终分，**全错**或**完全没有结果**的字段为0，全部正确为1，有错有对则是常见小数，最后将其加在一起除以**有结果的项数**获得最终成绩。

根据这样的计算方式，需在拿到表格后第一时间调查**全错**或**完全没有结果**的字段是否正确，如不正确应当及时调整策略或**重写收集类方法**。
