from flask_sqlalchemy import SQLAlchemy
import datetime
import time


start_time = 7
end_time = 34

weaks = ['壹', '贰', '叁', '肆', '伍', '陆', '日']

db = SQLAlchemy()


def fetch_time():
    return list(range(start_time,end_time))

# 转换为前端显示的日期
def getDesc(index):
    added = int((index - start_time) / 2)
    ended = (index - start_time) % 2
    tail = ':00' if ended == 0 else ':30'
    return '{}{}'.format(start_time + added, tail)


def time_desc(start, end, day):
    s_time = time.strftime("%m月%d号 ", time.localtime(day))
    return s_time + getDesc(start) + " - " + getDesc(end)


def fetch_data():
    time_span = fetch_time()

    results = []
    for rows in time_span:
        results.append({'number': rows, 'desc': getDesc(rows), 'reason': '被我占用'})
    return results


# 获取当前日期
def fetch_week():
    now = datetime.datetime.now().weekday()
    select_weak = range(now, now + 6)

    cur_time = time.time()

    res = []
    for i in range(len(select_weak)):
        info = {}
        info['week'] = weaks[select_weak[i] % 7]
        info['date'] = time.strftime("%m月%d号 ", time.localtime(cur_time))
        cur_time += 86400
        res.append(info)

    return res


