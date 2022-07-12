## 使用方法

### 1. 安装依赖

该脚本除了python基础依赖库，需要安装 `requests` 和 `requests_toolbelt` 两个库：

```python
pip install requests
pip install requests_toolbelt
```

安装完成后即可正常使用脚本

### 2. 个人配置

在目录下的`configs.py`文件里，用户可以对自己的脚本进行配置，下面对配置进行解读：

#### a. 配置默认使用图床

![image-20220403223953708](https://gitee.com/CYX12138/cloudimage/raw/master/img/202204032239779.png)

在`configs.py`文件的第11行可以配置默认使用的图床网站，而使用的图床**必须从下面5种中选择**。可以设置一种或者多种，按表格样式配置即可。

这里推荐使用CSDN，因为目前实测不需要频繁更换cookie，可以比较稳定的使用。

#### b. 配置登录cookie

因为使用的各服务提供商图床需要登录cookie，所以需要用户进入自己的浏览器抓包获得对应字段cookie后填入。

下面介绍各浏览器cookie的获取方法：

##### CSDN

登录自己的CSDN，然后进入个人中心 (https://i.csdn.net/)，打开浏览器的开发者工具（chrome 默认 `ctrl`+`alt`+`I`），找到`UserName`和`UserToken`，将对应的值复制。

![image-20220403225058211](https://gitee.com/CYX12138/cloudimage/raw/master/img/202204032250262.png)

然后粘贴到第26行的 `csdn_cookies`内，即完成配置。

![image-20220403225219093](https://gitee.com/CYX12138/cloudimage/raw/master/img/202204032252118.png)

##### 知乎

登录自己的知乎，然后进入主页 (https://www.zhihu.com/)，打开浏览器的开发者工具，找到`z_c0`，将对应的值复制，然后填入33行对应的`zhihu_cookies`里即完成配置。

![image-20220403230304735](https://gitee.com/CYX12138/cloudimage/raw/master/img/202204032303788.png)

知乎的图片默认支持3种，`src`, `watermark_src`, `original_src`，`watermark_src`是水印原图，`original_src`是原图，`src`是展示图，用户可以自己选择。

##### b站

登录自己的b站，然后进入主页 (https://www.bilibili.com/)，打开浏览器的开发者工具，找到`SESSDATA`，将对应的值复制，然后填入41行对应的`bili_cookies`里即完成配置。

![image-20220403230545655](https://gitee.com/CYX12138/cloudimage/raw/master/img/202204032305695.png)

##### 简书

登录自己的简书，然后进入主页 (https://www.jianshu.com/)，打开浏览器的开发者工具，找到`remember_user_token`和`_m7e_session_core`字段，将对应的值复制，然后填入47行对应的`jianshu_cookies`里即完成配置。

![image-20220403225425468](https://gitee.com/CYX12138/cloudimage/raw/master/img/202204032254513.png)

##### 博客园

登录自己的博客园，然后进入主页 (https://www.cnblogs.com/)，打开浏览器的开发者工具，找到`.Cnblogs.AspNetCore.Cookies`字段，将对应的值复制，然后填入53行对应的`bokeyuan_cookies`里即完成配置。

![image-20220403230025459](https://gitee.com/CYX12138/cloudimage/raw/master/img/202204032300502.png)

### 3.  命令行调用

脚本的使用方法为：

````python
python convert.py
````

使用该命令后，默认读取当前脚本所处目录下的所有md文件，并逐个读取扫描图片链接或本地路径，按照配置里指定的转换方式，转换后再输出为{New_(mode)_(原始名)}。

![image-20220403231909674](https://gitee.com/CYX12138/cloudimage/raw/master/img/202204032319760.png)

如果需要指定转化的文件，使用命令：

````python
python convert.py -f new.md
````

而如果不适用默认的转换图床，需要额外指定转换图床，使用命令：

``````python
python convert.py -m csdn
``````

这两个参数可以同时指定，转换效果如下：

![image-20220403232234371](https://gitee.com/CYX12138/cloudimage/raw/master/img/202204032322424.png)

