# Contest_Warrior

Version：1.1

Python：3.8.5

pandas：1.3.1

openpyxl：3.0.7

requests：2.24.0



AutoOCR 的 infer 结果（end2end_score）实在太差了，可视性极差，功能鸡肋，特写个方便法帮自己更好地对比标注与识别结果，希望也有机会帮助新人好且便捷地完成工作。

### 

### 请注意：

##### 图片与标注结果必须一一对应（别多也别少）。



### 使用方法：

创建并编辑 **holder_zhi.json** 。

```json
{
  "Data": "data", # 指定输入路径，其下必有固定名字两个文件夹 Images, Labels
  "Excel_Name": "my_score", # 最后输出的Excel名，默认输出到当前路径下 Excels
  "Scene": "xxxx", # 场景 Scene
  "Scene_Main": "xxxx", # Scene 上级，如 ticket
  "Host&Port": "http://127.0.0.1:2021/" # 请求URL，注意最后一定要有 "/"
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
def work_man_one(self, basket, lab_cont, ida_cont, img_name): # diy here
        # ------------ diy area ------------------
        # c = Collector(lab_cont, ida_cont, self.sub_sce,
        #             self.main_sce, self.service_eng, img_name)
        # res = c.processing_room()
        d = Diy(lab_cont, ida_cont, self.sub_sce,
                    self.main_sce, self.service_eng, img_name)
        res = d.processing_room()
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
