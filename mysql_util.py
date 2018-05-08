import pymysql


def execute(dbName, sql):
    try:
        db = __get_db(dbName)
        cursor = db.cursor()

        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            print("Error: unable to execute sql, reason: %s" % e.__str__())
            raise e
        finally:
            db.close()
    except Exception as e:
        print("Error: %s fail to open, reason: %s" % (dbName, e.__str__()))
        raise e


def select(dbName, sql):
    try:
        db = __get_db(dbName)
        cursor = db.cursor()

        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("Error: unable to fetch data, reason: %s" % e.__str__())
            raise e
        finally:
            db.close()
    except Exception as e:
        print("Error: %s fail to open, reason: %s" % (dbName, e.__str__()))
        raise e

    return []


def __get_db(dbName):
    return pymysql.connect("localhost", "root", "linyuangege1989", dbName, charset="utf8")
