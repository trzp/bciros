![bciros](bciros_logo.png)

Copyright (C) 2018, Nudt, JingshengTang, All Rights Reserved

Author: Jingsheng Tang

Email: 810899799@qq.com

# bciros
bciros是一个依赖于ROS1环境的用于开发BCI实验程序的python包。它包含两个子集，一个是bcicore,一个是guiengine。guiengine一般只在需要设计图形交互界面的时候用到（大多数时候是需要的），而core包含了实现BCI实验程序的核心架构。

# bciros包的安装
pip install bcicore-1.0-py3-none-any.wheel

pip install guiengine-1.0-py3-none-any.wheel

**如果计算机中安装有多个python,您可能需要在pip命令前加上python -m指令，限定包安装的python版本**

# bciros的核心概念
在bci实验中，涉及到实验流程的控制，图形刺激界面的配合，信号采集和信号处理等模块。在bciros的体系中，这里的每个功能模块将作为一个节点node在独立的进程中运行，它们之间的信息交互通过ROS标准完成，即主题的发布/订阅模式。以下是bciros中的核心概念：

* phase: 状态机，决定实验流程的跳转
* core: 核心，决定实验的核心逻辑
* source: 信号源
* sigpro: 信号处理
* sigsave: 信号保存
* guiengine: 图形引擎

# bcicore
ttttttttttttt

# guiengine
## 安装
pip install guiengine-1.0-py3-none-any.wheel

## guiengine包构成
guiengine包包含了GuiEngine类,若干刺激类：block,sinblock,circle,sincircle和一个控制类guictr.

## 快速开始
### 安装了guiengine包后，可以运行demo查看效果

```javascript
from guiengine.guiengine import demo
demo()
```

### 程序设计
* demo代码的内容：
```python

from guiengine.guiengine import *

def demo():
    layout = {'screen': {'size': (600, 400), 'color': (0, 0, 0), 'type': 'normal',
                         'Fps': 60, 'caption': 'BciRosGuiDemo'},

              #nly text
              'cue1': {'class': 'Block', 'parm': {'size': (80, 80), 'position': (100, 100), 'anchor': 'center',
                                                  'forecolor': (100, 100, 100), 'transparent': True, 'borderon': False,
                                                  'borderwidth': 1, 'bordercolor': (255, 0, 0),
                                                  'textcolor': (0, 255, 0), 'textfont': 'arial', 'textanchor': 'center',
                                                  'textsize': 20, 'textbold': False, 'text': 'hello', 'layer': 1,
                                                  'visible': True}},
              #text + shadow
              'cue2': {'class': 'Block', 'parm': {'size': (80, 80), 'position': (200, 100), 'anchor': 'center',
                                                  'forecolor': (100, 100, 100), 'transparent': False, 'borderon': False,
                                                  'borderwidth': 1, 'bordercolor': (255, 0, 0),
                                                  'textcolor': (0, 255, 0), 'textfont': 'arial', 'textanchor': 'midleft',
                                                  'textsize': 20, 'textbold': False, 'text': 'hello', 'layer': 1,
                                                  'visible': True}},
              #text + border
              'cue3': {'class': 'Block', 'parm': {'size': (80, 80), 'position': (300, 100), 'anchor': 'center',
                                                  'forecolor': (100, 100, 100), 'transparent': True, 'borderon': True,
                                                  'borderwidth': 1, 'bordercolor': (255, 0, 0),
                                                  'textcolor': (0, 255, 0), 'textfont': 'arial', 'textanchor': 'midright',
                                                  'textsize': 20, 'textbold': False, 'text': 'hello', 'layer': 1,
                                                  'visible': True}},

              # text + border + shadow
              'cue4': {'class': 'Block', 'parm': {'size': (80, 80), 'position': (400, 100), 'anchor': 'center',
                                                  'forecolor': (100, 100, 100), 'transparent': False, 'borderon': True,
                                                  'borderwidth': 1, 'bordercolor': (255, 0, 0),
                                                  'textcolor': (0, 255, 0), 'textfont': 'arial', 'textanchor': 'midbottom',
                                                  'textsize': 20, 'textbold': False, 'text': 'hello', 'layer': 1,
                                                  'visible': True}},
              # text + border + sin
              'cue5': {'class': 'sinBlock', 'parm': {'size': (80, 80), 'position': (500, 100), 'anchor': 'center',
                                                     'bordercolor': (255, 0, 0), 'borderon': True, 'borderwidth': 2,
                                                     'textcolor': (0, 255, 0), 'textfont': 'arial',
                                                     'textanchor': 'midtop', 'textsize': 20, 'textbold': False,
                                           'text': 'hello', 'layer': 1, 'visible': True,
                                                     'start': True, 'frequency': 10, 'phase': 0}},

              # only text
              'cue6': {'class': 'Circle',
                       'parm': {'radius': 40, 'position': (100, 300), 'anchor': 'center', 'forecolor': (100, 100, 100),
                                'transparent': True, 'borderon': False, 'borderwidth': 2, 'bordercolor': (255, 0, 0),
                                'textcolor': (0, 255, 0), 'textfont': 'arial', 'textanchor': 'center',
                                'textsize': 20, 'textbold': False, 'text': 'hello', 'layer': 1, 'visible': True}},

              # text + shadow
              'cue7': {'class': 'Circle',
                       'parm': {'radius': 40, 'position': (200, 300), 'anchor': 'center', 'forecolor': (100, 100, 100),
                                'transparent': False, 'borderon': False, 'borderwidth': 2, 'bordercolor': (255, 0, 0),
                                'textcolor': (0, 255, 0), 'textfont': 'arial', 'textanchor': 'center',
                                'textsize': 20, 'textbold': False, 'text': 'hello', 'layer': 1, 'visible': True}},

              # text + border
              'cue8': {'class': 'Circle',
                       'parm': {'radius': 40, 'position': (300, 300), 'anchor': 'center', 'forecolor': (100, 100, 100),
                                'transparent': True, 'borderon': True, 'borderwidth': 2, 'bordercolor': (255, 0, 0),
                                'textcolor': (0, 255, 0), 'textfont': 'arial', 'textanchor': 'center',
                                'textsize': 20, 'textbold': False, 'text': 'hello', 'layer': 1, 'visible': True}},

              # text + shadow + border
              'cue9': {'class': 'Circle',
                       'parm': {'radius': 40, 'position': (400, 300), 'anchor': 'center', 'forecolor': (100, 100, 100),
                                'transparent': False, 'borderon': True, 'borderwidth': 2, 'bordercolor': (255, 0, 0),
                                'textcolor': (0, 255, 0), 'textfont': 'arial', 'textanchor': 'center',
                                'textsize': 20, 'textbold': False, 'text': 'hello', 'layer': 1, 'visible': True}},

              # text + shadow + border
              'cue10': {'class': 'sinCircle',
                        'parm': {'radius': 40, 'position': (500, 300), 'anchor': 'center', 'borderon': True,
                                 'borderwidth': 2, 'bordercolor': (255, 0, 0), 'textcolor': (0, 255, 0),
                                 'textfont': 'arial', 'textanchor': 'center', 'textsize': 20, 'textbold': False,
                                 'text': 'hello', 'layer': 1, 'visible': True, 'start': True, 'frequency': 8,
                                 'phase': 0}},
              }
    gui = GuiEngine(layout, 'BRN_gui', ['BRT_guictr'])
    gui.StartRun()

if __name__ == '__main__':
    demo()
```

## GuiEngine实现布局
*from guiengine.guiengine import GuiEngine*

*GuiEngine(stims = layout, node_name='BRN_gui', topics=[])*

* 可以看到启动一个gui界面仅需要两步，第一步是初始化GuiEngine,然后调用StartRun()开始。而启动一个gui界面，意味着启动了一个ros节点。

* 参数： node_name 代表本节点的名称，如果在复杂的程序设计中，GuiEngine放在一个更大的程序中，而在这个大程序中已经初始化了节点的话，在这里是不能够初始化节点的，应为一个进程只能初始化一个节点。此时在node_name处可以传递None参数，GuiEngine将不会初始化节点。

* 参数：topics 代表本节点订阅的主题。可以看到我们将demo运行起来后，我们只是实现了界面的布局，元素的行为如何控制呢？通过订阅主题来实现。这里topics是一个列表，意味着它支持订阅多个主题，接受来自多个节点的控制信号，**但是这种情况下要非常注意正确的时序**。

* 参数：stims 代表了界面元素的布局。它由一个字典构成，这个字典应该是这样的：
* 示例：
```python
layout = {
            'screen':{'size':(600,500),'color':(0,0,0)},
            'cue1':{'class':'Block','parm':{'size':(100,40),'position':(600/2,30)}},
            'cue2':{'class':'Block','parm':{'size':(100,40),'position':(600/2,60)}},
         }
```
* 说明：该字典的形式为{'screen':{描述screen的属性}，'刺激1':{对刺激1的描述}，'刺激2':{对刺激2的描述}，}
* 至少应当包含对screen的描述，screen的属性有：
    * size: (width,height)
    * type: fullscreen/normal
    * color: (R,G,B)
    * caption: string
    * Fps: int, **一定要确认系统的Fps,linux下可通过xrandr命令查看Fps**
    * 补充说明：当且仅当type为fullscreen时，硬件加速才可开启。因此，在正式实验时，应当使用fullscreen模式。

* 对刺激的描述包含类别class和参数parm。
* 目前支持的刺激图形有：
    *  Block
    *  sinBlock
    *  Circle
    *  sinCircle

* 关于各个刺激类的使用，demo里已经给出了各个类的详细参数和可能的变化，直接参照demo即可。

## GuiCtr实现交互
* 前面提到，GuiEngine完成的是界面布局，它通过订阅topics来实现交互。事实上，为了更好地兼容，topics消息的格式是json字符串。该json字符串传递的是控制一个对象行为的描述，这种描述如下：
```python
# json字符串，实际上就是将python的字典转换为了json字符串
{'cue5': {'start': False},'cue10': {'start': False}}
```
* 为了隐藏对topic消息的直接操作，我们提供GuiCtr类来实现交互。

* 快速开始,配合guiengine.guiengine里运行的demo,可以看到交互情况
```python
from guiengine.guictr import demo
demo()
```

* 程序设计
```python
from guiengine.guictr import GuiCtr
GuiCtr(node_name = 'BRN_guictr',topic_name='BRT_guictr')
--update(reqdict = {}, echo = False)
```
   
* GuiCtr类初始化
    * node_name: 节点名，为None时，不初始化node
    * topic_name: 主题名，发布消息的主题名称
* update函数：每次调用将发布消息，请求接收节点进行gui更新
    * reqdict: 请求刷新的字典
    * echo: 是否将发布的消息打印到命令行
* guiengine.guictr中demo代码：
```python
def demo():
    guictr = GuiCtr('BRN_guictr',topic_name='BRT_guictr')
    rospy.sleep(3)
    guictr.update({'cue5': {'start': False},'cue10': {'start': False}},True)
    rospy.sleep(3)
    guictr.update({'cue5': {'start': True}, 'cue10': {'start': True}}, True)
    rospy.sleep(3)
    guictr.update({'cue5': {'start': False}, 'cue10': {'start': False}}, True)
    rospy.sleep(1)
    guictr.update({'_quit_':None},True)
    rospy.sleep(1)
```
**update请求参数为 {'\_quit\_':None}时将请求gui主节点结束进程**
