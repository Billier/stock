APP_KEY = "b690dbd794c308aeafbfd86f247b6b73"
SH_URL = "http://web.juhe.cn:8080/finance/stock/shall"
SZ_URL = "http://web.juhe.cn:8080/finance/stock/szall"

DB_NAME = "stock"

RECOMMEND_SQL_1 = """
select s.* from stock s
left join daily d on s.code=d.code
where mktcap>300000 and mktcap<1500000
and date=(select distinct date from daily order by date desc limit 1)
and volume/nmc > 0.08
and high<settlement
and trade<25
and trade<open
and low<settlement*0.93
and change_percent>-2
"""

RECOMMEND_SQL_2 = """
select s.* from stock s
left join daily d on s.code=d.code
where mktcap>300000 and mktcap<1500000
and date=(select distinct date from daily order by date desc limit 1)
and volume/nmc > 0.08
and high>settlement*1.06
and trade<25
and trade<open
and low<settlement*1.03
and change_percent>-0.5
"""
