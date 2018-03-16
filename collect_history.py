import MySQLdb as M
import gdax, time, json, os
from datetime import datetime
from dateutil import tz

def write_to_db(rates, db, fp = None):
    if len(rates) == 0:
        return

    cur = db.cursor()
#    if fp is not None:
#        logging("  Start to write to database...\n", fp)
    try:
        for entry in rates:
            cur.execute(
                """INSERT INTO history (timestamp, low, high, open, close, volume, utc_datetime, mt_datetime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5],
                 timestamp_to_utcstr(entry[0]),
                 timestamp_to_localstr(entry[0])))
        db.commit()
    except:
        db.rollback()

#    if fp is not None:
#        logging("  Write Finished!\n", fp)
        

def logging(str, file = None):
    if file is not None:
        file.write(str)
    else:
        print(str)        

def utcstr_to_timestamp(ut_cstr):
    dt_utc = datetime.strptime(ut_cstr, "%Y-%m-%d %H:%M:%S")
    dt_utc = dt_utc.replace(tzinfo = tz.tzutc())
    dt_local = dt_utc.astimezone(tz.tzlocal())
    ts = time.mktime(dt_local.timetuple())
    return int(ts)


def timestamp_to_utcstr(ts):
    utc_str = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    return utc_str

def localstr_to_timestamp(local_str):
    ts = time.mktime(datetime.strptime(local_str, "%Y-%m-%d %H:%M:%S").timetuple())
    return int(ts)

def timestamp_to_localstr(ts):
    local_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    return local_str
        
def main():
    pc = gdax.PublicClient()
    config = json.load(open('dbconn.json'))["mysql"]
    db = M.connect(host = config["host"],
                   user = config["user"],
                   passwd = config["password"],
                   db = config["database"])

    if os.path.exists("./log"):
        try:
            os.remove("./log")
        except OSError:
            pass
            
    fp = open("./log", "w")

    product = 'BTC-USD'
    # UTC Datetime
    von = "2018-03-14 12:00:00"
    bis = "2018-03-15 00:00:00"

    start_ts = utcstr_to_timestamp(von)
    end_ts = utcstr_to_timestamp(bis)
    h = 4

    cnt = 0
    cur_ts = start_ts
    while cur_ts < end_ts:
        cnt = cnt + 1
        if cnt > 1:
            time.sleep(10)
        if cur_ts + 4 * 60 > end_ts:
            next_ts = end_ts
        else:
            next_ts = cur_ts + 4 * 3600

        cur_str = timestamp_to_utcstr(cur_ts)
        next_str = timestamp_to_utcstr(next_ts)
        rs = pc.get_product_historic_rates(product, start = cur_str, end = next_str, granularity = 60)
        if len(rs) < 240 and len(rs) > 0:
            logging("Data from " + cur_str + " to " + next_str + "\n", file = fp)
            logging("  size = " + str(len(rs)) + "\n", file = fp)
            logging("--------------------------------\n", file = fp)
        write_to_db(rs, db, fp)
        print("From " + cur_str + " to " + next_str + ": " + str(len(rs)) + " entries.")

        cur_ts = next_ts

    
    db.close()
    fp.close()
    

if __name__ == "__main__":
    main()
