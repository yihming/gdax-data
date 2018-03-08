import MySQLdb as M
import gdax, time, json
from datetime import datetime
import pytz

def write_to_db(rates, db):
    cur = db.cursor()
    logging("  Start to write to database...")
    try:
        for entry in rates:
            cur.execute(
                """INSERT INTO history (timestamp, low, high, open, close, volume, utc_datetime, mt_datetime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5],
                 datetime.utcfromtimestamp(entry[0]).strftime("%Y-%m-%d %H:%M:%S"),
                 datetime.fromtimestamp(entry[0]).strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    except:
        db.rollback()

    logging("  Write Finished!")

def logging(str, file = None):
    if file is None:
        print(str)

## Needed
def utcstr_to_timestamp(utcstr):
    dt_utc = datetime.strptime(utcstr, "%Y-%m-%dT%H:%M:%S")
    dt_utc = dt_utc.replace(tzinfo = pytz.utc)
    ts = time.mktime(dt_utc.timetuple())
    return int(ts)

## Needed
def timestamp_to_utcstr(ts):
    dt_utc = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S")
    return dt_utc

def dtstr_to_timestamp(dt):
    ts = time.mktime(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timetuple())
    return int(ts)

def timestamp_to_dtstr(ts):
    dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    return dt
        
def main():
    pc = gdax.PublicClient()
    db = M.connect(host = "localhost",
                   user = "root",
                   passwd = "871121",
                   db = "gdax")

    von = "2018-03-05T00:00:00"
    bis = "2018-03-06T23:59:00"

    ts_start = utcstr_to_timestamp(von)
    ts_end = utcstr_to_timestamp(bis)
    h = 4

    cur_ts = ts_start
    while cur_ts != ts_end:
        if cur_ts + 4 * 3600 >= ts_end:
            next_ts = ts_end
        else:
            next_ts = cur_ts + 4 * 3600

        cur_str = timestamp_to_utcstr(cur_ts)
        next_str = timestamp_to_utcstr(next_ts)
        rs = pc.get_product_historic_rates('BTC-USD', start = cur_str, end = next_str, granularity = 60)
        logging("Fetch data from " + cur_str + " to " + next_str)
        write_to_db(rates, db)
        logging("--------------------------------")
        
        cur_ts = next_ts + 60
     

    db.close()
    

if __name__ == "__main__":
    main()
