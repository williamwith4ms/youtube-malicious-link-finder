import json
import os
import sqlite3
import pandas as pd
import time
from googleapiclient.discovery import build

keywords = ["free robux"]
API_KEY = os.environ.get("YOUTUBE_API_KEY")

SERVICE_NAME="youtube"
API_VERSION="v3"

def df_to_sql(df):
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    for i, row in df.iterrows():
        cursor.execute("INSERT INTO videos VALUES (?,?,?,?,?,?,?,?)", (row['id.videoId'], row['snippet.channelId'], row['snippet.description'], row['statistics.viewCount'], row['snippet.publishedAt'], current_time, False, False))
    connection.commit()
    connection.close()
    print("Data inserted successfully")

def get_additional_data(row):
    id = row['id.videoId']
    print("Requesting additional data for video: ", id)
    # youtube = build(SERVICE_NAME, developerKey=API_KEY, version=API_VERSION)
    # 
    # request = youtube.videos().list(id=id, part="snippet,statistics").execute()
    # row['snippet.description'] = request['items'][0]['snippet']['description']
    # row['statistics.viewCount'] = request['items'][0]['statistics']['viewCount']
    row['statistics.viewCount'] = 0
    row['snippet.description'] = "test"  
    return row

def process_search(search):
    items = search['items']
    df = pd.json_normalize(items)
    channels = set(df['snippet.channelId'].to_list())
    
    # drop row if video id = NaN
    df = df.dropna(subset=['id.videoId'])
    df = df.apply(get_additional_data, axis=1)
    df_to_sql(df)
    return df

def search_youtube(queries):
    #run search with all queries
    print("Requesting search for queries: ", queries)
    #youtube = build(SERVICE_NAME, developerKey=API_KEY, version=API_VERSION) 
    #search = youtube.search().list(
    #    q=queries,
    #    part="snippet",
    #    maxResults=50
    #).execute()
    with open("test_data.json" ,"r", encoding="utf-8") as f:
        search = json.load(f)
    
    process_search(search)

if __name__ == "__main__":
    search_youtube(keywords)
