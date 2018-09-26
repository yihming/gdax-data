import datetime
import calendar
import requests
import pandas as pd
import json
import os.path
import time
import MySQLdb as M

def write_to_db(df, db):
    print "Write %d entries to database." % df.shape[0]
    cur = db.cursor()

    try:
        for row in df.itertuples():
            print "(%s, %s, %s, %s, %s, %s)" % (row.Time, row.Open, row.Close, row.High, row.Low, row.Volume)
            cur.execute(
                """INSERT INTO finex_history (timestamp, open, close, high, low, volume)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (row.Time, row.Open, row.Close, row.High, row.Low, row.Volume))
        db.commit()
        print "Write successfully!\n"
    except:
        print "Database error happens!\n"
        db.rollback()


def collect_data(db, latest_time = int(time.time() - 60 * 60 * 24)):

    starttime = datetime.datetime.strptime('09/24/2018', '%m/%d/%Y');
    
    start_unixtime = calendar.timegm(starttime.utctimetuple())

    latest_time = int(time.time() - 60 * 60 * 24) #The real ending time. Collect data from starttime to current time - 24 hours

    track_time = time.time() #because bitstamp only allows 10 requests per minute. Take rest if we are faster than that
    count = 0

    while (start_unixtime < latest_time):
        end_unixtime = start_unixtime + 60 * 999 #60*60*24*30 #30 days at a time
    
        if (end_unixtime > latest_time):
            end_unixtime = latest_time #if the time is in future.

        url = 'https://api.bitfinex.com/v2/candles/trade:1m:tBTCUSD/hist?start={}&end={}&limit=1000'.format(str(start_unixtime) + "000", str(end_unixtime) + "000") #1 hour can be changed to any timeframe
        response = requests.get(url)
        data = response.json()

        df = pd.DataFrame(data)
        
        df.columns = ['Time', 'Open', 'Close', 'High', 'Low', 'Volume']
        df.set_index('Time')

        write_to_db(df, db)
        
        start_unixtime = end_unixtime + 60 #to prevent duplicates
        count = count + 1
    
        if (count == 10): #if 10 requests are made
            count = 0 #reset it
        
            diff = time.time() - track_time
        
            if (diff <= 60):
                print('Sleeping for {} seconds'.format(str(60 - diff)))
                time.sleep(60 - diff) #sleep
            
        
            track_time = time.time()
        #bitstamp limits to 10 requests per minute
	





def main():
    config = json.load(open('dbconn.json'))["mysql"]
    db = M.connect(host = config["host"],
                   user = config["user"],
                   passwd = config["password"],
                   db = config["database"])

    collect_data(db)

    db.close()

    
if __name__ == "__main__":
    main()
