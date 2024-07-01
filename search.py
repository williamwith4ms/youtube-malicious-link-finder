import json
import os
import sys
import sqlite3
import pandas as pd
import time
from googleapiclient.discovery import build

keywords = ["fortnite skin swapper"]
API_KEY = os.environ.get("YOUTUBE_API_KEY")

SERVICE_NAME="youtube"
API_VERSION="v3"

def df_to_sql(df):
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    current_time = time.strftime('%Y-%m-%dT%H:%M:%SZ')
    video_ids = df['id.videoId'].to_list()
    for i, row in df.iterrows():
        cursor.execute("INSERT INTO videos VALUES (?,?,?,?,?,?,?,?)", (row['id.videoId'], row['snippet.channelId'], row['snippet.description'], row['statistics.viewCount'], row['snippet.publishedAt'], current_time, False, False))
    connection.commit()
    connection.close()
    
    print("Data inserted successfully")
    get_comments(df, current_time)

def get_additional_data(row):
    id = row['id.videoId']
    youtube = build(SERVICE_NAME, developerKey=API_KEY, version=API_VERSION)
    
    if '--test' in sys.argv:
        row['statistics.viewCount'] = 0
        return row
    
    print("Requesting additional data for video: ", id)
    request = youtube.videos().list(id=id, part="snippet,statistics").execute()
    
    row['snippet.description'] = request['items'][0]['snippet']['description']
    row['statistics.viewCount'] = request['items'][0]['statistics']['viewCount']
    
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
    if '--test' in sys.argv:
        with open("test_data.json" ,"r", encoding="utf-8") as f:
            search = json.load(f)
    else:  
        youtube = build(SERVICE_NAME, developerKey=API_KEY, version=API_VERSION) 
        search = youtube.search().list(
            q=queries,
            part="snippet",
            maxResults=50
        ).execute()
    
    process_search(search)

def get_comments(df, current_time):
    ids = df['id.videoId'].to_list()        
    
    for id in ids:
        print("Requesting comments for video: ", id)
        try:
            youtube = build(SERVICE_NAME, developerKey=API_KEY, version=API_VERSION)
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=id,
                maxResults=100
            ).execute()
            
            comment_df = pd.json_normalize(request['items'])
            
            insert_into_sql(id,comment_df, current_time)
        except Exception as e:
            print("Error: ", e)
            continue

def insert_into_sql(id,comment_df, current_time):
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    
    for i, row in comment_df.iterrows():
        cursor.execute("INSERT INTO comments VALUES (?,?,?,?,?,?,?,?)", (row['id'], id, row['snippet.topLevelComment.snippet.authorChannelId.value'], row['snippet.topLevelComment.snippet.textDisplay'], row['snippet.topLevelComment.snippet.publishedAt'], current_time, False, False))
    connection.commit()
    connection.close()
        

if __name__ == "__main__":
    search_youtube(keywords)
