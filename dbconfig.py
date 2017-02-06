# -*- coding: utf-8 -*-
'''
This config file sets up a database and establishes table schema
'''

import os
import pandas as pd
from sqlalchemy import create_engine


def createdb():
    '''Creates db'''
    p = (os.path.dirname(os.path.abspath(__file__)))
    engine = create_engine('sqlite:////%s/companies.db' % (p))
    conn = engine.connect()
    conn.close()


def dbWrite(df, tableName):
    '''Writes to db'''
    p = (os.path.dirname(os.path.abspath(__file__)))
    engine = create_engine('sqlite:////%s/companies.db' % (p))
    df.to_sql(tableName, engine, index=False, if_exists='append')


def main():
    colSequence = ['industryName',
                   'serial',
                   'companyName',
                   'companyUrl',
                   'companyDescription',
                   'companyAddress',
                   'ceoTitle',
                   'ceoName',
                   'facebook',
                   'linkedin',
                   'twitter',
                   'logo',
                   'profileUrl']
    data = [{'industryName': 'Example',
             'serial': '0',
             'companyName': 'example',
             'companyUrl': 'example',
             'companyDescription': 'example',
             'companyAddress': 'example',
             'ceoTitle': 'example',
             'ceoName': 'example',
             'facebook': 'example',
             'linkedin': 'example',
             'twitter': 'example',
             'logo': 'example',
             'profileUrl': 'example'}]
    try:
        df = pd.DataFrame(data, columns=colSequence)
        createdb()
        dbWrite(df, 'companies')
    except Exception as e:
        raise SystemExit(e, e.args)


if __name__ == "__main__":
    main()
