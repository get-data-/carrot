# -*- coding: utf-8 -*-
'''Innumerate the list of companies'''

import os
import sys
import time
# import requests
import dryscrape
from extract import Extractor
from sqlalchemy import create_engine


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
    if 'linux' in sys.platform:
        # start xvfb in case no X is running. Make sure xvfb
        # is installed, otherwise this won't work!
        dryscrape.start_xvfb()
    # sPage = requests.get(startUrl)
    # sHtml = sPage.text
    # sPage.raise_for_status()
    sess = dryscrape.Session(base_url='https://www.owler.com')
    sess.set_attribute('auto_load_images', False)
    sess.visit('/sector/industrial-machinery-equipment-companies')
    print(sess.status_code(), sess.headers())
    sHtml = sess.body()
    # with open('sample.txt', 'r') as f:  # Mocked
    #     sHtml = f.read()  # Mocked
    resultsInfo = Extractor(sHtml)
    sdf = resultsInfo.getData()
    print(type(sdf))
    # writeData(sdf, 'companies')
    writeData(sdf, 'runcompanies')  # Mocked
    n = resultsInfo.nResults()
    for i in range(5, 0, -1):
        time.sleep(1)
        print('%s seconds - Next page will begin' % (i))
    for v in range(2, int(n/15)):
        nextone = '/sector/industrial-machinery-equipment-companies?p=%s' % (v)
        print(nextone)
        # page = requests.get(nextpage)
        # page.raise_for_status()
        # html = page.text
        sess.visit(nextone)
        print(sess.status_code(), sess.headers())
        html = sess.body()
        info = Extractor(html)
        # info = Extractor(sHtml)  # Mocked
        df = info.getData()
        # writeData(df, 'companies')
        writeData(df, 'runcompanies')  # Mocked
        for i in range(20, 0, -1):
            time.sleep(1)
            print('%s seconds - Next page will begin' % (i))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise SystemExit(e, e.args, 'Exited: main')
