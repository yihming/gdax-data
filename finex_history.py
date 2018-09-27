import datetime
import calendar
import requests
import pandas as pd
import json
import os.path
import time
import MySQLdb as M

from gdax_history import timestamp_to_utcstr

def connect_to_db():
    config = json.load(open('dbconn.json'))["mysql"]
    db = M.connect(host = config["host"],
                   user = config["user"],
                   passwd = config["password"],
                   db = config["database"])
    return db

def write_to_db(df, db):
    print "Write %d entries to database." % df.shape[0]
    cur = db.cursor()

    try:
        for row in df.itertuples():
            ts = row.Time / 1000
            cur.execute(
                """INSERT INTO finex_history (timestamp, open, close, high, low, volume, utc_datetime)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                [ts, row.Open, row.Close, row.High, row.Low, row.Volume, timestamp_to_utcstr(ts)])
        db.commit()
        print "Write successfully!\n"
    except (M.Error, M.Warning) as e:
        print e
        db.rollback()


def collect_data(start, end):

    starttime = datetime.datetime.strptime(start, '%m/%d/%Y')
    endtime = datetime.datetime.strptime(end, '%m/%d/%Y')
    
    start_unixtime = calendar.timegm(starttime.utctimetuple())
    end_unixtime = calendar.timegm(endtime.utctimetuple())

    track_time = time.time() #because bitstamp only allows 10 requests per minute. Take rest if we are faster than that
    count = 0

    df = pd.DataFrame(data = [], columns = ['Time', 'Open', 'Close', 'High', 'Low', 'Volume'])

    while (start_unixtime < end_unixtime):
        cur_end_unixtime = start_unixtime + 60 * 999 #60*60*24*30 #30 days at a time
    
        if (cur_end_unixtime > end_unixtime):
            cur_end_unixtime = end_unixtime #if the time is in future.

        url = 'https://api.bitfinex.com/v2/candles/trade:1m:tBTCUSD/hist?start={}&end={}&limit=1000'.format(str(start_unixtime) + "000", str(cur_end_unixtime) + "000") #1 hour can be changed to any timeframe
        response = requests.get(url)
        data = response.json()

        df_tmp = pd.DataFrame(data)
        
        df_tmp.columns = ['Time', 'Open', 'Close', 'High', 'Low', 'Volume']
        #df.set_index('Time')

        df = pd.concat([df, df_tmp])
        
        start_unixtime = cur_end_unixtime + 60 #to prevent duplicates
        count = count + 1
    
        if (count == 10): #if 10 requests are made
            count = 0 #reset it
        
            diff = time.time() - track_time
        
            if (diff <= 60):
                print('Sleeping for {} seconds'.format(str(60 - diff)))
                time.sleep(60 - diff) #sleep
            
        
            track_time = time.time()
        #bitstamp limits to 10 requests per minute

    df = df.sort_values(by = ['Time'])

    return df



def main():
    db = connect_to_db()
    df = collect_data(start = '09/24/2018', end = '09/26/2018')
    write_to_db(df, db)

    db.close()

    
if __name__ == "__main__":
    main()
