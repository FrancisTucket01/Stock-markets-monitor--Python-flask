import sys
from selenium import webdriver
from ltwallet import mysql, app
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

class everything():
    def __init__(self):
        sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.wd = webdriver.Chrome('chromedriver',options=options)

        self.url = "https://www.tradingview.com/forex-screener/"
        self.wd.get(self.url)
        time.sleep(10)
        


    def get(self):
        values = self.wd.find_elements(By.XPATH, "//*[@id='js-screener-container']/div[4]/table/tbody/tr[@data-symbol]")
        quotes = ["news","GBP-USD", "GBP-EUR","GBP-CAD","GBP-AUD","GBP-CHF","BTC-GBP", "EUR-USD","EUR-JPY","EUR-CHF","EUR-AUD", "BTC-EUR","USD-CAD","USD-CHF", "USD-AUD","USD-JPY", "BTC-USD"]
        for val in values:
            try:
                x=WDW(val, 20).until(EC.presence_of_element_located((By.XPATH, ".//td[1]/div/div[2]/a")))
                for quote in quotes:
                    if "-" in quote:
                        quote = quote.replace("-", "")
                    elif "." in quote:
                        quote = quote.strip(".").replace(":", "")
                    else:
                        quote = quote
                
                    if quote == x.text:
                        bid = val.find_element(By.XPATH, ".//td[5]").text
                        ask = val.find_element(By.XPATH, ".//td[6]").text
                        high = val.find_element(By.XPATH, ".//td[7]").text
                        low = val.find_element(By.XPATH, ".//td[8]").text

                        with app.app_context():
                            cursor = mysql.connection.cursor()
                            with  cursor as f:
                                smt = f"INSERT INTO newcurrent(quote, bid, ask, high, low) VALUES('{quote}', {bid}, {ask}, {high}, {low});"
                                print(smt)
                            mysql.connection.commit()
                            cursor.close()
            except StaleElementReferenceException as e:
                pass

everything()
while True:
    print("Executing!!!")
    everything().get()
        

