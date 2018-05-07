from stock import Stock
import datetime
import time
import mysql_util
import mail
import constant


def sleep(h, m, s):
    return h * 3600 + m * 60 + s


if __name__ == '__main__':
    working = False
    work_has_done = False
    work_error = False


    def work():
        s = Stock()
        s.set_error_func(error_work)
        s.set_complete_func(after_work)
        s.request_stocks()


    def error_work(e):
        print(e)
        global working, work_error
        working = False
        work_error = True


    def after_work():
        recommend()
        print("執行完畢")
        global working, work_has_done, work_error
        working = False
        work_has_done = True
        work_error = False


    def recommend():
        results = []
        results.extend(mysql_util.select(constant.DB_NAME, constant.RECOMMEND_SQL_1))
        results.extend(mysql_util.select(constant.DB_NAME, constant.RECOMMEND_SQL_2))

        if len(results) == 0:
            content = "暂无推荐"
        else:
            content = "今日（%s）推荐：\n" % datetime.datetime.now().strftime("%Y-%m-%d")
            for r in results:
                content += "%s  %s \n" % (r.code, r.name)

        mail.send(content)


    second = sleep(0, 0, 10)
    cur_date = datetime.datetime.now().strftime("%Y-%m-%d")
    while 1 == 1:
        now = datetime.datetime.now()
        if cur_date != now.strftime("%Y-%m-%d"):
            cur_date = now.strftime("%Y-%m-%d")
            work_has_done = False

        if not working and (work_error or (not work_has_done and now.hour > 15)):
            working = True
            print("开始执行脚本")
            work()

        time.sleep(second)
