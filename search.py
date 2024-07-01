from googleapiclient.discovery import build
import pandas as pd
import json
import os

queries = ["free robux"]
API_KEY = os.environ.get("YOUTUBE_API_KEY")

SERVICE_NAME="youtube"
API_VERSION="v3"

def search_youtube(queries):
    #run search with all queries
    youtube = build(SERVICE_NAME, developerKey=API_KEY, version=API_VERSION)
    search = youtube.search().list(
        q=queries,
        part="snippet",
        maxResults=50
    ).execute()
    
    return search

if __name__ == "__main__":
    print(search_youtube("hi"))
