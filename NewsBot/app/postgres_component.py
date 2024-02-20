import psycopg2
from qrlib.QRUtils import display
import psycopg2
import datetime
from qrlib.QREnv import QREnv
class Database():
    def __init__(self):
        super().__init__()
        self.conn = None
        self.cursor= None
    def connection(self):
        try:
            self.conn = psycopg2.connect(
            host= QREnv.VAULTS['test']['host'],
            port= QREnv.VAULTS['test']['port'],
            user= QREnv.VAULTS['test']['user'],
            password =QREnv.VAULTS['test']['password'],
            database =QREnv.VAULTS['test']['database']
            )
        except Exception as e: 
            display(e)

        if(self.conn):
            display("---------------connection sucessful!-----------------")
            self.cursor = self.conn.cursor()

    def sendtodb(self, newslst):
        display("---------------sending data to database-----------------") # requires a dictanory and portal name 
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        for dict in newslst:
            try:
                display(dict)
                insert_query = """
                        INSERT INTO newsbase(keyword, title, content, link, newspaper, date_ad, date_bs)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                self.cursor.execute(insert_query, (dict['keyword'], dict['title'], dict['content'], dict['link'], dict['newspaper'], current_date, ''))
                self.conn.commit()
                display("data added")
            except Exception as e:
                display(e)
                
            
    def closeDb(self):
        self.cursor.close()
        display("connection close")

    def fetchData(self):
        display("--------------fetching data from database --------------")
        self.cursor.execute("SELECT * FROM newsbase")
        results = self.cursor.fetchall()
        display(results)
        return results
        




