import MySQLdb as M
from pymongo import MongoClient
import gdax, time

class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        self.message_count = 0
        print("Let's count the messages!")

    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print("Message type: ", msg["type"], "\t@ {:.3f}".format(float(msg["price"])))

    def on_close(self):
        print("-- Goodbye! --")
        
#wsClient = myWebsocketClient()
#wsClient.start()
#print(wsClient.url, wsClient.products)
#while (wsClient.message_count < 500):
#    print("\nmessage_count = ", "{} \n".format(wsClient.message_count))
#    time.sleep(1)
#wsClient.close()

#order_book = gdax.OrderBook(product_id = 'BTC-USD')
#order_book.start()
#time.sleep(10)
#order_book.close()
        
#public_client = gdax.PublicClient()

#res1 = public_client.get_products()
#res2 = public_client.get_product_order_book('BTC-USD', level = 3)
#res3 = public_client.get_product_ticker(product_id = 'BTC-USD')


def test_mongodb():
    ## MongoDB ##
    mongo_client = MongoClient("mongodb://localhost:27017")
    db = mongo_client.cryptocurrency_database
    BTC_collection = db.BTC_collection

    ## Using Websocket ##
    #ws_client = gdax.WebsocketClient(url = "wss://ws-feed.gdax.com", products = "BTC-USD", mongo_collection = BTC_collection, should_print = False)
    ws_client = myWebsocketClient(url = "wss://ws-feed.gdax.com", products = "BTC-USD", mongo_collection = BTC_collection)
    ws_client.start()
    time.sleep(10)
    ws_client.close()


def test_mysql():
    ## MySQL ##
    db = M.connect(host = "localhost",
                   user = "root",
                   passwd = "871121",
                   db = "gdax")

    cur = db.cursor()
    print(type(db))

    # cur.execute("SELECT * FROM orders")


def test_order_book():
    db = M.connect(host = "localhost",
                   user = "root",
                   passwd = "871121",
                   db = "gdax")
    ws_client = myWebsocketClient(url = "wss://ws-feed.gdax.com", products = "BTC-USD", mysql_conn = db)
