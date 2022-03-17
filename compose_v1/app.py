import time

import redis
from flask import Flask
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pandas as pd
import numpy as np

import pickle
import redis
import zlib

last_df = pd.DataFrame()


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

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
    EXPIRATION_SECONDS = 600
    # r = redis.StrictRedis(host='localhost', port=6379, db=0)
    # r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    r = cache
    # r = redis.StrictRedis(host='127.0.0.1', port=5000, db=0)
    r.setex("key", EXPIRATION_SECONDS, zlib.compress( pickle.dumps(df)))
    return r

def load_df_from_redis(r, key):
    import pickle
    import zlib
    import redis
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
    df_str = None
    # if last_df.equals(df):
    #     print('df is same -> no notification')
    # else:
    last_df = df
    save_df2html(df)
    save_df2sql(df)
    r = save_df2redis(df)
    print('saved')
    # df_str = load_df_from_redis(r, 'key').to_string().encode('utf-8').strip()
    df_str = load_df_from_redis(r, 'key').to_string()#.encode('utf-8').strip()
    print(df_str)
    return df_str

@app.route('/')
def hello():
    # loop & wait, loop & wait...
    i = 0
    df_str = None
    while True:
        i += 1
        df_str = update()
        time.sleep(10)
        if i==2: break
    # count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(df_str)
    # return 'Hello World!'

# @app.route('/')
# def hello():
#     count = get_hit_count()
#     return 'Hello World! I have been seen {} times.\n'.format(count)