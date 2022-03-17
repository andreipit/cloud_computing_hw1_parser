import time
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pandas as pd
import numpy as np

last_df = pd.DataFrame()

def surf_web():
    # load urls & queries
    queries=[]
    urls=[]
    for line in open('search_query.txt',encoding="utf8"): queries.append(line.rstrip())
    for line in open('urls.txt'): urls.append(line.rstrip())

    # init df
    df = pd.DataFrame(columns = ['url', 'query', 'count'])
    for u in urls:
        for q in queries:
            df = df.append(pd.Series({'url': u, 'query': q, 'count': 0}) , ignore_index=True)

    # download page and count words
    for url in urls:
        fhand = urllib.request.urlopen(url)    #same as file.open
        for line in fhand:
            line = line.decode().strip()
            for query in queries:
                if query in line:
                    df['count'][(df['url']==url) & (df['query']==query)] += 1

    return df[(df['count']!=0)]

def save_df2html(df):
    HEADER = '''
    <html>
        <head>

        </head>
        <body>
    '''
    FOOTER = '''
        </body>
    </html>
    '''
    with open('result.html', 'w', encoding='utf8') as f:
        f.write(HEADER)
        f.write(df.to_html(classes='df'))
        f.write(FOOTER)

def save_df2redis(df):
    import redis
    import pickle
    import redis
    import zlib
    EXPIRATION_SECONDS = 600
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.setex("key", EXPIRATION_SECONDS, zlib.compress( pickle.dumps(df)))

def load_df_from_redis(key):
    rehydrated_df = pickle.loads(zlib.decompress(r.get(key)))
    return rehydrated_df

def save_df2sql(df):
    import sqlite3
    import urllib.request
    conn = sqlite3.connect('result.sqlite')
    cur = conn.cursor()
    cur.execute('''
    DROP TABLE IF EXISTS Search''')
    cur.execute('''
    CREATE TABLE Search (url TEXT, query TEXT, count INTEGER)''')
    df.apply(lambda row: cur.execute('''INSERT INTO Search (url, query, count) VALUES ( ?, ?, ? )''', ( str(row['url']), str(row['query']), int(row['count']))), axis=1)
    conn.commit()
        
def update():
    global last_df
    df = surf_web()
    if last_df.equals(df):
        print('df is same -> no notification')
    else:
        last_df = df
        save_df2html(df)
        save_df2sql(df)
        save_df2redis(df)
        print('saved')
        print(load_df_from_redis('key'))

if __name__ == '__main__':
    # loop & wait, loop & wait...
    i = 0
    while True:
        i += 1
        update()
        time.sleep(10)
        if i==2: break
