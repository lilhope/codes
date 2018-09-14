### Usage Guide of Process Monitor

#### baseline
```
python monitor.py --pid 11648 --view img --time 60
#pid: the process ID you monitor
#view: the view module:
      -img:view on dynamic image
      -cmd:view on console
      -file:write the monitor info to log file
#time: listen time: second
```
### 使用向导  
#### 命令
```
python monitor.py --pid 11648 --view img --time 60
#pid: 监控的进程PID
#view: 监控模式:
      -img:以动态图片的形式展示
      -cmd:在控制台显示
      -file:将控制信息写入文件
#time: 监控时长(单位：秒)
```

#### 在linux环境中使用
##### 环境依赖
- jupyter notebook([参考此向导安装配置jupyter](https://blog.csdn.net/a819825294/article/details/55657496))
- python 3.x
##### 使用
- 远程登录，IP:port,输入密码，登录jupyter
- 新建一个jupyter文件
- 将monitor.py的内容粘贴
- 执行该jupyter文件即可