import MySQLdb as M
import gdax, time
from datetime import datetime

class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self, db_conn):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        self.mysql_conn = db_conn
        self.message_count = 0
        print("-- MySQL connection is successfully created!--")

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

def main():
    client = create_websocket_client()
    

if __name__ == "__main__":
    main()
