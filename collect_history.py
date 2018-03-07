import MySQLdb as M
import gdax, time
from datetime import datetime

class myWebsocketClient(gdax.WebsocketClient):
    def __init__(self, db_conn):
        gdax.WebsocketClient.__init__(self)
        self.mysql_conn = db_conn
        print("-- MySQL connection is successfully created!--")
        
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        self.message_count = 0

    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print("Message type: ", msg["type"], "\t@ {:.3f}".format(float(msg["price"])))

    def on_close(self):
        print("-- Goodbye! --")


def create_websocket_client():
    db = M.connect(host = "localhost",
                   user = "root",
                   passwd = "871121",
                   db = "gdax")
    ws_client = myWebsocketClient(db)
    return(ws_client)

def write_to_db(rates, db):
    cur = db.cursor()
    print("  Start to write to database...")
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

    print("  Write Finished!")
        

def main():
    pc = gdax.PublicClient()
    db = M.connect(host = "localhost",
                   user = "root",
                   passwd = "871121",
                   db = "gdax")
    rates = pc.get_product_historic_rates('BTC-USD', granularity = 60)
    start_ts = rates[len(rates) - 1][0]
    start_dt = datetime.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M:%S")
    end_ts = rates[0][0]
    end_dt = datetime.fromtimestamp(end_ts).strftime("%Y-%m-%d %H:%M:%S")
    ts_diff = end_ts - start_ts
    print("Fetch data from %s to %s" % (start_dt, end_dt))
    print("Time Stamp difference is %s" % str(ts_diff))
    write_to_db(rates, db)

    db.close()
    

if __name__ == "__main__":
    main()
