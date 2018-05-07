from stock import Stock
import datetime
import time
import mail


def sleep(h, m, s):
    return h * 3600 + m * 60 + s


def work():
    s = Stock()
    s.set_error_func(lambda e: print(e))
    s.set_complete_func(lambda: mail.send("執行完畢"))
    s.request_stocks()


if __name__ == '__main__':
    second = sleep(0, 0, 10)
    cur_date = datetime.datetime.now().strftime("%Y-%m-%d")
    done = False
    while 1 == 1:
        now = datetime.datetime.now()
        if cur_date != now.strftime("%Y-%m-%d"):
            cur_date = now.strftime("%Y-%m-%d")
            done = False

        if not done:
            done = True
            work()

        time.sleep(second)
