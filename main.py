from stock import Stock
import datetime
import time
import mysql_util
import mail


def sleep(h, m, s):
    return h * 3600 + m * 60 + s


def work():
    s = Stock()
    s.set_error_func(lambda e: print(e))
    s.set_complete_func(after_work)
    s.request_stocks()


def after_work():
    recommend()
    print("執行完畢")


def recommend():
    results = []
    results.extend(mysql_util.select())
    results.extend(mysql_util.select())

    if len(results) == 0:
        content = "暂无推荐"
    else:
        content = "今日（%s）推荐：\n" % datetime.datetime.now().strftime("%Y-%m-%d")
        for r in results:
            content += "%s  %s \n" % (r.code, r.name)

    mail.send(content)


if __name__ == '__main__':
    second = sleep(0, 0, 10)
    cur_date = datetime.datetime.now().strftime("%Y-%m-%d")
    done = False
    while 1 == 1:
        now = datetime.datetime.now()
        if cur_date != now.strftime("%Y-%m-%d"):
            cur_date = now.strftime("%Y-%m-%d")
            done = False

        if not done and now.hour > 15:
            print("开始执行脚本")
            done = True
            work()

        time.sleep(second)
