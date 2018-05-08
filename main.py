from stock import Stock
import datetime
import time
import mysql_util
import mail
import constant
import logging
import os


def sleep(h, m, s):
    return h * 3600 + m * 60 + s


def set_log_file():
    path = os.path.abspath('.') + "/logs/"
    if not os.path.exists(path):
        os.mkdir(path)

    logging.basicConfig(filename="%s%s.log" % (path, datetime.datetime.now().strftime("%Y-%m-%d")),
                        format="%(asctime)s - %(levelname)s: %(message)s")


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
        logging.error(e)
        global working, work_error
        working = False
        work_error = True


    def after_work():
        recommend()
        logging.warning("执行完毕")
        global working, work_has_done, work_error
        working = False
        work_has_done = True
        work_error = False


    def recommend():
        results = []
        try:
            results.extend(mysql_util.select(constant.DB_NAME, constant.RECOMMEND_SQL_1))
            results.extend(mysql_util.select(constant.DB_NAME, constant.RECOMMEND_SQL_2))
        except Exception as e:
            logging.error(e)
            return

        if len(results) == 0:
            content = "暂无推荐"
        else:
            content = "今日（%s）推荐：\n" % datetime.datetime.now().strftime("%Y-%m-%d")
            for r in results:
                content += "%s  %s \n" % (r.code, r.name)

        mail.send(content)
        logging.warning("发送邮件")


    second = sleep(0, 1, 0)
    cur_date = datetime.datetime.now().strftime("%Y-%m-%d")
    set_log_file()
    while 1 == 1:
        now = datetime.datetime.now()
        if cur_date != now.strftime("%Y-%m-%d"):
            cur_date = now.strftime("%Y-%m-%d")
            set_log_file()
            work_has_done = False

        if not working and (work_error or (not work_has_done and now.weekday() < 5 and now.hour >= 15)):
            working = True
            if work_error:
                logging.warning("尝试重新执行脚本")
            else:
                logging.warning("开始执行脚本")
            work()

        time.sleep(second)
