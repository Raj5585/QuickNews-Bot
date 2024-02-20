import psycopg2
from qrlib.QRUtils import display
import psycopg2
import datetime
from qrlib.QREnv import QREnv


class Database:
    def __init__(self):
        super().__init__()
        self.conn = None
        self.cursor = None

    def connection(self):
        try:
            self.conn = psycopg2.connect(
                host=QREnv.VAULTS["test"]["host"],
                port=QREnv.VAULTS["test"]["port"],
                user=QREnv.VAULTS["test"]["user"],
                password=QREnv.VAULTS["test"]["password"],
                database=QREnv.VAULTS["test"]["database"],
            )
        except Exception as e:
            display(e)

        if self.conn:
            display("---------------connection sucessful!-----------------")
            self.cursor = self.conn.cursor()

    def sendtodb(self, newslst):

        try:
            display("---------------------------------- create -----------------")
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS test_news_table(
                id SERIAL PRIMARY KEY, 
                newspaper VARCHAR(30), 
                keyword VARCHAR(30),
                title VARCHAR(512), 
                link VARCHAR(512), 
                content VARCHAR(512), 
                date_ad VARCHAR(30), 
                date_bs VARCHAR(30))
                """
            )
            self.conn.commit()

        except Exception as create_table_error:
            print("Error creating table:", create_table_error)

        display(
            "---------------sending data to database-----------------"
        )  # requires a dictanory and portal name
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        for news_dict in newslst:
            try:
                display(news_dict)
                insert_query = """
                        INSERT INTO test_news_table(keyword, title, content, link, newspaper, date_ad, date_bs)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                self.cursor.execute(
                    insert_query,
                    (
                        news_dict["keyword"],
                        news_dict["title"],
                        news_dict["content"],
                        news_dict["link"],
                        news_dict["newspaper"],
                        current_date,
                        "",
                    ),
                )
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
