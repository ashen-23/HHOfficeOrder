#!/usr/bin/env bash

source Classes/venv/bin/activate
nohup python3 -u Classes/app.py> out.log 2>&1 &

ps -ef|grep python

echo '启动成功'



#假如要停止app.py
#ps -ef|grep python
#我们可以看到 app.py是在 15450下跑
#然后 kill -9 15450
