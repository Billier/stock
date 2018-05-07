import requests
import mysql_util
import datetime
from page import Page

APP_KEY = "b690dbd794c308aeafbfd86f247b6b73"
DB_NAME = "stock"
SH_URL = "http://web.juhe.cn:8080/finance/stock/shall"
SZ_URL = "http://web.juhe.cn:8080/finance/stock/szall"


class Stock:
    def __init__(self):
        self.__request_count = 0
        self.__error_func = None
        self.__complete_func = None

    def set_error_func(self, func):
        if callable(func):
            self.__error_func = func

    def set_complete_func(self, func):
        if callable(func):
            self.__complete_func = func

    def request_stocks(self):
        self.__remove_old_data()
        self.__request_count = 2
        self.__get_stocks(SH_URL, Page())
        self.__get_stocks(SZ_URL, Page())

    def __remove_old_data(self):
        mysql_util.execute(DB_NAME, "DELETE FROM stock")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        mysql_util.execute(DB_NAME, "DELETE FROM daily WHERE date='%s'" % date)

    def __get_stocks(self, url, page):
        if page.get_total_page() > 0 and not page.has_more_page():
            self.__request_count -= 1
            if self.__request_count <= 0:
                if self.__complete_func is not None:
                    self.__complete_func()
            return

        params = {
            "key": APP_KEY,
            "stock": "a",
            "page": page.get_cur_page(),
            "type": 4
        }
        res = requests.get(url, params)
        json = res.json()
        if json:
            error_code = json["error_code"]
            if error_code == 0:
                # 成功请求
                data = json["result"]

                total = int(data["totalCount"])
                size = int(data["num"])
                page.set_total_page(total / size + (1 if (total % size > 0) else 0))
                page.next_page()

                if not self.__save_stocks(data["data"]):
                    if self.__error_func is not None:
                        self.__error_func("save data error")
                    return

                self.__get_stocks(url, page)
            else:
                error_str = "%s:%s" % (json["error_code"], json["reason"])
                print(error_str)
                if self.__error_func is not None:
                    self.__error_func(error_str)
        else:
            print("request api error")
            if self.__error_func is not None:
                self.__error_func(res.reason)

    def __save_stocks(self, data_list):
        if data_list is None or not isinstance(data_list, list):
            return False

        return self.__save_stock(data_list) and self.__save_daily(data_list)

    def __save_stock(self, data_list):
        sql = "INSERT INTO stock(code,name,symbol,per,pb,nmc,mktcap,update_datetime) VALUES "
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        can_save = True
        for s_map in data_list:
            symbol = s_map.get("symbol", "")
            code = s_map.get("code", "")
            if code == "":
                can_save = False
                break
            name = s_map.get("name", "")
            symbol = str(symbol).replace(str(code), "")
            per = s_map.get("per", 0.0)
            pb = s_map.get("pb", 0.0)
            nmc = s_map.get("nmc", 0.0)
            mktcap = s_map.get("mktcap", 0.0)

            sql += "('%s', '%s', '%s', %f, %f, %f, %f, '%s')," \
                   % (code, name, symbol, per, pb, nmc, mktcap, time)

        if can_save:
            sql = sql[:-1]
            if mysql_util.execute(DB_NAME, sql):
                return True

        return False

    def __save_daily(self, data_list):
        sql = "INSERT INTO daily(code,trade,price_change,change_percent,settlement," \
              "open,high,low,volume,amount,date,ticktime) VALUES "
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        can_save = True
        for s_map in data_list:
            code = s_map.get("code", "")
            if code == "":
                can_save = False
                break
            trade = s_map.get("trade", 0.0)
            price_change = s_map.get("pricechange", 0.0)
            change_percent = s_map.get("changepercent", 0.0)
            settlement = s_map.get("settlement", 0.0)
            op = s_map.get("open", 0.0)
            high = s_map.get("high", 0.0)
            low = s_map.get("low", 0.0)
            volume = s_map.get("volume", 0)
            amount = s_map.get("amount", 0)
            ticktime = s_map.get("ticktime", "00:00:00")

            sql += "('%s', %s, %s, %s, %s, %s, %s, %s, %d, %d, '%s', '%s')," \
                   % (code, trade, price_change, change_percent, settlement, op, high,
                      low, int(volume), int(amount), date, ticktime)

        if can_save:
            sql = sql[:-1]
            if mysql_util.execute(DB_NAME, sql):
                return True

        return False


if __name__ == '__main__':
    s = Stock()
    s.request_stocks()
