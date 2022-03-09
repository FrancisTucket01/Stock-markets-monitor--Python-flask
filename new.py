import sys
from selenium import webdriver
from ltwallet import mysql, app
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time

class dataget():
  def __init__(self):
    sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    self.wd = webdriver.Chrome('chromedriver',options=options)
    url = "https://www.investing.com/currencies/single-currency-crosses"
    self.wd.get(url)
    time.sleep(2)

  def sel(self,value):
    select = Select(self.wd.find_element(By.ID, "symbols"))
    select.select_by_value(value)
    time.sleep(2)

  def getd(self):
    quotes = self.wd.find_elements(By.XPATH, "//*[@id='cr1']/tbody/tr")

    for quote in quotes[0:6]:
      val = quote.find_element(By.XPATH, ".//td[2]").text.replace("/","")
      bid = quote.find_element(By.XPATH, ".//td[3]").text
      ask = quote.find_element(By.XPATH, ".//td[4]").text
      high = quote.find_element(By.XPATH, ".//td[5]").text
      low = quote.find_element(By.XPATH, ".//td[6]").text
      time = quote.find_element(By.XPATH, ".//td[9]").text

      with app.app_context():
            cursor = mysql.connection.cursor()
            with  cursor as f:
                smt = f"INSERT INTO newcurrent(quote, bid, ask, high, low, time) VALUES('{val}', {bid}, {ask}, {high}, {low}, '{time}');"
                f.execute(smt)
            mysql.connection.commit()
            cursor.close()



status = True
F = dataget()
while status:
  F.getd()
  F.sel("17")
  F.getd()
  F.sel("3")
  F.getd()
  F.sel("12")
