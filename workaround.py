# -*- coding: utf-8 -*-
'''Innumerate the list of companies'''

import os
import time
import random
import datetime
from selenium import webdriver
from extract import Extractor
from sqlalchemy import create_engine
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def writeData(df, tableName):
    '''Write a Pandas df to db'''
    p = (os.path.dirname(os.path.abspath(__file__)))
    engine = create_engine('sqlite:////%s/companies.db' % (p))
    try:
        df.to_sql(tableName, engine, index=False, if_exists='append')
    except IOError:
        raise SystemExit(df.head(), 'Exited: IOError in writeData function')
    except Exception as e:
        raise SystemExit(e, e.args, 'Exited: writeData function')


def main():
    base = 'https://www.owler.com'
    # path = '/sector/industrial-machinery-equipment-companies'
    # path = '/industry/industrial-goods-services-companies'
    path = '/industry/industrial-goods-services-companies?p=1319'
    url = base + path
    driver = webdriver.Firefox()
    time.sleep(7)
    wait = WebDriverWait(driver, 20)
    driver.get(url)
    time.sleep(10)
    # with open('sample.txt', 'r') as f:  # Mocked
    #     sHtml = f.read()  # Mocked
    resultsInfo = Extractor(driver.page_source)
    sdf = resultsInfo.getData()
    # writeData(sdf, 'biggertest')  # Mocked
    writeData(sdf, 'companies')
    n = resultsInfo.nResults()
    print(n, 'this is main N')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('%s seconds - Crawl will begin' % (i))
    # for v in range(2, (int(n/15)+1)):
    for v in range(1320, (int(n/15)+1)):
        randomPause = random.randint(8, 13)
        for i in range(randomPause, 0, -1):
            time.sleep(1)
            # print('%s seconds - Next page will begin' % (i))
        wait = WebDriverWait(driver, 20)
        wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="next-15"]')))
        driver.find_element_by_xpath('//*[@id="next-15"]').click()
        html = driver.page_source
        info = Extractor(html)
        df = info.getData()
        # writeData(df, 'biggertest')  # Mocked
        writeData(df, 'companies')
        print('Page %s of %s' % (v, int(n/15)))
        if info.title() == 'Pardon Our Interruption':
            print('wait: %s, p: %s of %s' % (randomPause, v, str(int(n/15)+1)))
            print(datetime.datetime.now())
            driver.quit()
            raise SystemExit('They\'re onto us! Ghost out!')
    driver.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise SystemExit(e, e.args, 'Exited: main')
