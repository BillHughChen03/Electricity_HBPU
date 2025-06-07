

# 湖北理工学院电力查询系统

一个2021级计算机科学与技术系牛马的无奈。

## 目的

写这个鸟系统的原因是因为我校每次快没电了也没个提醒，每次半夜两三点空调没电了热得我一雷，结果晚上这个鸟系统电费还充不进去。还有就是白天跑代码的时候，每次炼丹炉跑了一整天快跑完的时候没电了，结果充了电费从头再来。痛定思痛一定要搞得什么东西来缓解一下我的用电焦虑。

后来发现【慧新e校】是可以查电费的，但是就是没有推送。遂抓了一下学校的接口，写了这个系统。由于开发周期非常短，从抓包到搭建到测试上线使用只用了两天，所以估计有一大堆bug，但是不重要，核心功能能用。别吐槽我数据库连接那的屎山代码，第一次用FastAPI写后端，用了一下VF_Admin这个基于Ruoyi改造的FastAPI框架[RuoYi-Vue3-FastAPI](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI)，有很多不足之处还请海涵，希望后继有人能够优化一下数据库连接性能、规范一下写法等等，甚至可以在这个上面进一步拓展出你自己的功能，前提是不要高速访问学校的API，导致学校系统、服务器崩溃被请喝茶那是你自己的事情了，别把自己搞个处分了。

## 吐槽

慧新e校你个鸟东西，谁让你这么选房间的。楼层高一点的我得翻一万年，还生怕选错房间号，充错房间。

<img src=".\screenshot\image-20250607195937874.png" alt="image-20250607195937874" style="zoom:100%;" />

你写一个大接口，四次筛选不就搞定了吗？怎么这么好优化的东西就是不做，拿个表扁平化存一下不就好了，到底是谁让你们这么写的。这样子分四层是很难吗？

<img src=".\screenshot\序列 01.gif" alt="序列 01" style="zoom:100%;" />

实现起来其实也不会很难吧，首先你把表平化一下。

<img src=".\screenshot\image-20250607200142413.png" alt="image-20250607200142413" style="zoom:100%;" />

再转换成csv，导入到数据库。

<img src=".\screenshot\image-20250607200242060.png" alt="image-20250607200242060" style="zoom:100%;" />

然后你代码这么实现一下不就好了。

<img src=".\screenshot\image-20250607200323222.png" alt="image-20250607200323222" style="zoom:100%;" />

<img src=".\screenshot\image-20250607200416641.png" alt="image-20250607200416641" style="zoom:100%;" />

<img src=".\screenshot\image-20250607200458174.png" alt="image-20250607200458174" style="zoom:100%;" />

希望学校如果看到这里，就把你们的系统查询升级一下。

## 使用方法

常规按照部署方法，还原SQL数据库，敏感数据就没提供sql文件了，有需要的可以发邮件给我要一下：billchancbr@foxmail.com，请说明你的学院、专业、学号还有姓名，多少核实一下再给，礼貌一点。

后端在backnd里面去运行requirements.txt，建议Python 3.9以上版本。然后在.env.prod和.env.dev中记得修改MySQL和Redis的连接配置。一个是生产环境，一个是开发环境，这里不赘述，可以去看一下原来[VF_Admin](https://gitee.com/insistence2022/RuoYi-Vue3-FastAPI)的文档。

前端建议Node.js版本在18+，然后按照常规去打包就行，这里也可以去看一下VF_admin和Ruoyi-Vue3的文档，搜一下就有，然后把dist扔给nginx去运行就行。

务必注意前后端的端口号放行问题，你可以选择放两个端口号，比如前端运行在80上，后端运行在9099上，这里不赘述。

当然如果外部端口不充裕的话，可以像我这样利用nginx的转发特性，去修改后缀达到在一个端口上实现转发的的效果，上传的程序就是这么搞的。

前端配置：

<img src=".\screenshot\image-20250607201520310.png" alt="image-20250607201520310" style="zoom:100%;" />

<img src=".\screenshot\image-20250607201600883.png" alt="image-20250607201600883" style="zoom:100%;" />

后端配置别的端口，假设我的是9099端口。

<img src=".\screenshot\image-20250607202017074.png" alt="image-20250607202017074" style="zoom:100%;" />

先启动后端（生产环境）"python app.py --env=prod"，然后如下配置nginx转发即可。前端打包的dist放在nginx的根目录下。

<img src=".\screenshot\image-20250607202203168.png" alt="image-20250607202203168" style="zoom:100%;" />

原理大概如下所示：

<img src=".\screenshot\绘图1.png" alt="img" style="zoom:100%;" />

前端记得去创建一下定时推送的任务，每天八点钟开始执行。

<img src=".\screenshot\image-20250607204235736.png" alt="image-20250607204235736" style="zoom:100%;" />

## 二开

本项目支持二开的哈，最主要的学校接口的登录在这两个文件中，并提供了连接示例。

<img src=".\screenshot\image-20250607203105420.png" alt="image-20250607203105420" style="zoom:100%;" />

<img src=".\screenshot\image-20250607203147117.png" alt="image-20250607203147117" style="zoom:100%;" />

续签暂时用不了，但是发现学校给的access_token非常长，有十天，而且不用担心推送不了。

## 一些解答

1. 为了健壮性，在自动推送的代码中写了个如果发现access_token过期or异地登陆，直接重新登录去刷新这个access_token，代码在module_task/scheduler_test中，找到run_fee_send这个方法。当然有很多异常情况因为我没有捕获到（学校接口返回的结果），所以没办法做到100%健壮性，我只能预设”异处登录/登录过期“两个去执行了，那么就是刷新一次access_token。如果有同学捕获到新的结果可以给我提issue。

<img src=".\screenshot\image-20250607204052742.png" alt="image-20250607204052742" style="zoom:100%;" />



2. 推送微信用的是“方糖”的推送，具体而言就是打开这个网站去微信关注公众号，然后就能获取SendKey了，然后把SendKey填回去，勾选推送，保存就行。

   <img src=".\screenshot\image-20250607204822303.png" alt="image-20250607204822303" style="zoom:100%;" />

   <img src=".\screenshot\image-20250607204840320.png" alt="image-20250607204840320" style="zoom:100%;" />

   <img src=".\screenshot\image-20250607204856916.png" alt="image-20250607204856916" style="zoom:100%;" />

3. 推送方式？推送方式按照数据库逐个开始推送，没写多线程，怕学校给你封IP了。建议是再校园网内使用，校园网内他会自动解析到内网IP，那么一个接口调用只要30ms到200ms，但是你在公网去调用他会走学校总出口，一个人的查询要用28s左右，这是一个很垃圾的时间，有条件的可以在校园网拿个树莓派部署一下，一个开发板可以带个十来个人，也就是十多个寝室（一个寝室出一个账号就行），外网的话那你就只能慢慢等，建议是一台服务器不要带太多人，怕ban。

4. 进一步优化？可以用Redis加速等等，你们的天下了。

5. 一卡通的登录账号和密码是什么？这里用的是【慧新e校】的接口，因为没有验证码。账户一般是学号，密码是身份证后六位。有问题去西门一卡通中心重置。

6. 怎么注册？没写注册，怕别人恶意搞。管理员自己去新增就行。

   <img src=".\screenshot\image-20250607205815272.png" alt="image-20250607205815272" style="zoom:100%;" />

   <img src=".\screenshot\image-20250607205929781.png" alt="image-20250607205929781" style="zoom:100%;" />

7. 出现这种白页怎么办？   <img src=".\screenshot\image-20250607205328999.png" alt="image-20250607205328999" style="zoom:100%;" />

   很奇葩的nginx导致的问题，刷新一下就行。



# 系统演示

<img src=".\screenshot\image-20250607205435744.png" alt="image-20250607205435744" style="zoom:100%;" />

<img src=".\screenshot\image-20250607205450952.png" alt="image-20250607205450952" style="zoom:100%;" />

<img src=".\screenshot\image-20250607205504609.png" alt="image-20250607205504609" style="zoom:100%;" />

手机端也适配了一下。

<img src=".\screenshot\image-20250607210231525.png" alt="image-20250607210231525" style="zoom:100%;" />

<img src=".\screenshot\image-20250607205722733.png" alt="image-20250607205722733" style="zoom:100%;" />

<img src=".\screenshot\1.png" alt="1" style="zoom:60%;" />

<img src=".\screenshot\2.png" alt="2" style="zoom:60%;" />
