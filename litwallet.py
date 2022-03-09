import sys
import time
from ltwallet import mysql, app
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from termcolor import colored
import csv 

print(colored("###        ###    ######      ###############  ##            ##     ###########  ##     ##  ############  ##############","cyan"))
print(colored("####      ####    ##   ##            ##        ##            ##    ###        \  ##    ##   ##                  ##","cyan"))
print(colored("####      ####    ##    ##           ##        ##            ##   ###            ##   ##    ##                  ##","cyan"))
print(colored("## ##    ## ##    ##   ##            ##        ##            ##   ###            ##  ##     ##                  ##","cyan"))
print(colored("##  ### ##  ##    ## ###             ##        ###          ###   ##             #####      ############        ##","cyan"))
print(colored("##   ####   ##    ##   ##            ##        ###          ###   ###            ##  ##     ##                  ##","cyan"))
print(colored("##          ##    ##    ##    ###    ##         ####      ####     ###        /  ##   ##    ##                  ##","cyan"))
print(colored("##          ##    ##     ##   ###    ##          ############       ###########  ##    ##   ############        ##","cyan"))

class Tables:
    def __init__(self):
        self.quotes = ["news","GBP-USD", "GBP-EUR","GBP-CAD","GBP-AUD","GBP-CHF","BTC-GBP", "EUR-USD","EUR-JPY","EUR-CHF","EUR-AUD", "BTC-EUR","USD-CAD","USD-CHF", "USD-AUD","USD-JPY", "BTC-USD", ".INX:INDEXSP", ".DJI:INDEXDJX"]

    def create(self):
        with app.app_context():
            cursor = mysql.connection.cursor()
            with  cursor as f:
                for quote in self.quotes:
                    if "-" in quote:
                        quote = quote.replace("-", "")
                    elif "." in quote:
                        quote = quote.strip(".").replace(":", "")
                    else:
                        quote = quote
                    
                    smt = f"CREATE TABLE IF NOT EXISTS {quote}( id INT NOT NULL AUTO_INCREMENT, date TEXT, info TEXT, link VARCHAR(255), PRIMARY KEY(ID) );"
                    f.execute(smt)
                sm = f"CREATE TABLE IF NOT EXISTS current( id INT NOT NULL AUTO_INCREMENT, quote VARCHAR(255), value VARCHAR(255), time VARCHAR(255), PRIMARY KEY(ID) );"
                f.execute(sm)
                ins = """LOAD DATA LOCAL INFILE '/content/drive/MyDrive/Envs/Flaskt/flaskt/current.csv' INTO TABLE current FIELDS TERMINATED BY ','  ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"""
                f.execute(ins)
                gm = "CREATE TABLE IF NOT EXISTS newcurrent(id INT NOT NULL AUTO_INCREMENT, quote VARCHAR(255), bid FLOAT,  ask FLOAT, high FLOAT, low FLOAT, time VARCHAR(255), PRIMARY KEY(id));"
                f.execute(gm)

            mysql.connection.commit()
            cursor.close()
    def drop(self):
        with app.app_context():
            cursor = mysql.connection.cursor()
            with  cursor as f:
                for quote in self.quotes:
                    if "-" in quote:
                        quote = quote.replace("-", "")
                    elif "." in quote:
                        quote = quote.strip(".").replace(":", "")
                    else:
                        quote = quote
                    
                    smt = f"DROP TABLE IF EXISTS {quote};"
                    f.execute(smt)
                f.execute("DROP TABLE IF EXISTS current;")
                f.execute("DROP TABLE IF EXISTS newcurrent")
            
            mysql.connection.commit()
            cursor.close()


class News:
    def __init__(self,quote):
        self.text_var = []
        self.date_var = []
        self.links = []
        sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.wd = webdriver.Chrome('chromedriver',options=options)
        self.url = f"https://www.google.com/finance/quote/{quote}"
        self.dbname = quote
        self.quote = quote
        
    def get_data(self):
        self.wd.get(self.url)
        self.text_var = self.wd.find_elements(By.CLASS_NAME, 'Yfwt5')
        self.date_var = self.wd.find_elements(By.CLASS_NAME, "Adak")
        for t in self.text_var:
            r = t.find_element(By.XPATH, "..")
            r = r.find_element(By.XPATH, "..").get_attribute('href')
            self.links.append(r)
    
    def dbwrite(self):
        i=0
        j=0
        k=0
        if "-" in self.quote:
            quote = self.quote.replace("-", "")
        elif "." in self.quote:
            quote = self.quote.strip(".").replace(":", "")
        else:
            quote = quote
        with app.app_context():
            cursor = mysql.connection.cursor()
            with  cursor as f:
                while i < len(self.text_var) and j < len(self.date_var) and k < len(self.links):
                    val1 = str(self.text_var[i].text).replace("'", "")
                    val2 = str(self.date_var[j].text).replace("'", "")
                    val3 = str(self.links[k])
                    smt = f"INSERT INTO news(date, info, link) VALUES('{val2}', '{val1}', '{val3}');"
                    f.execute(smt)
                    i += 1
                    j +=1
                    k+=1
            
            mysql.connection.commit()
            cursor.close()
    
    def dbwrite_news(self):
        i=0
        j=0
        k=0
        if "-" in self.quote:
            quote = self.quote.replace("-", "")
        elif "." in self.quote:
            quote = self.quote.strip(".").replace(":", "")
        else:
            quote = self.quote
        with app.app_context():
            cursor = mysql.connection.cursor()
            with  cursor as f:
                while i < len(self.text_var) and j < len(self.date_var) and k < len(self.links):
                    val1 = str(self.text_var[i].text).replace("'", "")
                    val2 = str(self.date_var[j].text).replace("'", "")
                    val3 = str(self.links[k])
                    smt = f"INSERT INTO {quote}(date, info, link) VALUES('{val2}', '{val1}', '{val3}');"
                    f.execute(smt)
                    i += 1
                    j +=1
                    k +=1
            
            mysql.connection.commit()
            cursor.close()

class Unitas:
    def __init__(self):
        self.heading = []
        self.content = []
        sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.wd = webdriver.Chrome('chromedriver',options=options)
        self.url = "https://tradingeconomics.com/stream?c=united+states"
  

    def get_data(self):
        self.wd.get(self.url)
        time.sleep(5)
        self.content = self.wd.find_elements(By.CLASS_NAME,'list-group-item')

    def dbwrite_news(self):
        i=0
        while i < len(self.content):
            if i > 3:
                c = self.content[i].text.rsplit("\n")
                head2= c[1]
                content= c[2]
            i += 1
            with app.app_context():
                cursor = mysql.connection.cursor()
                with  cursor as f:
                    while i < len(self.content):
                        val3 = "none"
                        if i > 3:
                            c = self.content[i].text.replace("'", "").rsplit("\n")
                            head = c[0]
                            head2= c[1]
                            content= c[2]
                            smt = f"INSERT INTO news(date, info, link) VALUES('{head2}', '{content}', '{val3}');"
                            f.execute(smt)
                        i += 1
                mysql.connection.commit()
                cursor.close()


class Current:
    def __init__(self,quote,tim):
        self.heading = []
        self.content = []
        self.database = []
        sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.wd = webdriver.Chrome('chromedriver',options=options)
        self.quote = quote
        self.url = f"https://www.google.com/finance/quote/{self.quote}"
        self.tim = tim

    def get_data(self):
        self.wd.get(self.url)
        self.content = self.wd.find_elements(By.CLASS_NAME, "fxKbKc")

    def insert_data(self):
        i=0
        if "-" in self.quote:
            quote = self.quote.replace("-", "")
        elif "." in self.quote:
            quote = self.quote.strip(".").replace(":", "")
        else:
            quote = self.quote
        with app.app_context():
            cursor = mysql.connection.cursor()
            with  cursor as f:
                while i < len(self.content):
                    val1 = str(self.content[i].text)
                    smt = f"INSERT INTO current(quote, value, time) VALUES('{quote}', '{val1}', '{tim}');"
                    f.execute(smt)
                    i += 1
            
            mysql.connection.commit()
            cursor.close()
    
    def insert_csv(self):
        i=0
        if "-" in self.quote:
            quote = self.quote.replace("-", "")
        elif "." in self.quote:
            quote = self.quote.strip(".").replace(":", "")
        else:
            quote = self.quote
        current_csv = "/content/drive/MyDrive/Envs/Flaskt/flaskt/current.csv"
        row = [[]]
        with  open(current_csv, "a") as f:
            csvwriter = csv.writer(f)
            while i < len(self.content):
                val1 = str(self.content[i].text)
                row[i].append(i)
                row[i].append(quote)
                row[i].append(val1)
                row[i].append(self.tim)
                csvwriter.writerow(row[i])
                i += 1


f = Tables()
try:
    option = sys.argv[1]
    option = option.lower()
    if option == "create":
        print(colored("Creating the Necesary tables for operation ...", "cyan"))
        f.create()
        print(colored("Table Creation Complete", "cyan"))
    elif option == "drop":
        print(colored("Droping All Tables ...", "cyan"))
        f.drop()
        print(colored("Droping of tables complete", "cyan"))
    elif option == "news":
        quotes = ["GBP-USD", "GBP-EUR","GBP-CAD","GBP-AUD","GBP-CHF","BTC-GBP", "EUR-USD","EUR-JPY","EUR-CHF","EUR-AUD", "BTC-EUR","USD-CAD","USD-CHF", "USD-AUD","USD-JPY", "BTC-USD", ".INX:INDEXSP", ".DJI:INDEXDJX"]
        print(colored("Fetching FOREX News ...", "cyan"))
        for quote in quotes:
            N = News(quote)
            N.get_data()
            N.dbwrite()
            N.dbwrite_news()
        print(colored("Fetching of FOREX News Complete", "cyan"))
    elif option == "us":
        print(colored("Fetching United States News ...", "cyan"))
        U = Unitas()
        U.get_data()
        U.dbwrite_news()
        print(colored("Fetching of United States News Complete", "cyan"))
    elif option == "current":
        quotes = ["GBP-USD", "GBP-EUR","GBP-CAD","GBP-AUD","GBP-CHF","BTC-GBP", "EUR-USD","EUR-JPY","EUR-CHF","EUR-AUD", "BTC-EUR","USD-CAD","USD-CHF", "USD-AUD","USD-JPY", "BTC-USD", ".INX:INDEXSP", ".DJI:INDEXDJX"]
        print(colored("Fetching of Curent FPP in Progress ...", "cyan"))
        while True:
            for quote in quotes:
                now = datetime.now()
                tim =  now.strftime("%H:%M:%S")
                C = Current(quote,tim)
                C.get_data()
                C.insert_data()
                C.insert_csv()

    else:
        print(colored("Option supplied is Not recognised", "red"))
        print(colored("To create Tables supply option 'create'", "red"))
        print(colored("To Drop all Tables supply option 'drop'", "red"))
except IndexError as e:
    print(colored("No Option supplied", "red"))
    print(colored("To create Tables supply option 'create'", "red"))
    print(colored("To Drop all Tables supply option 'drop'", "red"))

