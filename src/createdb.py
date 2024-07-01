import sqlite3

def are_you_sure(table_name):
    """Asks the user if they are sure they want to drop the table."""
    result = input(f"Table {table_name} already exists. Would you like to drop it? (yes/N): ")
    if result.lower() == "yes":
        result = input(f"Are you sure? This WILL result in a loss of data type {table_name} to continue: ")
        if result == table_name:
            return True
        else:
            return False
    else:
        return False

VIDEOS = """ CREATE TABLE videos (
video_id CHAR(11),
channel_id CHAR(24),
description text,
viewcount integer,
published_at timestamp,
updated_at timestamp,
positive_test boolean,
false_positive boolean,
PRIMARY KEY (video_id, updated_at)
)"""

COMMENTS = """ CREATE TABLE comments (
comment_id CHAR(26),
video_id CHAR(11),
author_id CHAR(24),
text text,
published_at timestamp,
updated_at timestamp,
positive_test boolean,
false_positive boolean,
PRIMARY KEY (comment_id, updated_at)
)"""

LINKS = """ CREATE TABLE links (
link_id CHAR(64),
url text,
occurrences integer,
newest_occurrence timestamp,
oldest_occurrence timestamp,
PRIMARY KEY (link_id)
)"""

LINK_OCCURRENCE = """ CREATE TABLE link_occurrence (
    link_id CHAR(64),
    video_id CHAR(11),
    comment_id CHAR(26),
    PRIMARY KEY (link_id, video_id, comment_id)
    )"""

def create_videos():
    """Creates the videos table."""
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    try:
        cursor.execute(VIDEOS)
    except sqlite3.OperationalError:
        if are_you_sure("videos"):
            cursor.execute("DROP TABLE videos")
            cursor.execute(VIDEOS)
    connection.commit()
    connection.close()

def create_comments():
    """creates the comments table."""
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    try:
        cursor.execute(COMMENTS)
    except sqlite3.OperationalError:
        if are_you_sure("comments"):
            cursor.execute("DROP TABLE comments")
            cursor.execute(COMMENTS)
    connection.commit()
    connection.close()

def create_links():
    """Creates the links table."""
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    try:
        cursor.execute(LINKS)
    except sqlite3.OperationalError:
        if are_you_sure("links"):
            cursor.execute("DROP TABLE links")
            cursor.execute(LINKS)
    connection.commit()
    connection.close()

def create_link_occurrence():
    """Creates the link_occurrence table."""
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    try:
        cursor.execute(LINK_OCCURRENCE)
    except sqlite3.OperationalError:
        if are_you_sure("link_occurrence"):
            cursor.execute("DROP TABLE link_occurrence")
            cursor.execute(LINK_OCCURRENCE)
    connection.commit()
    connection.close()

def auto_links():
    """Creates the links table and the link_occurrence table."""
    create_links()
    create_link_occurrence()

def create_automatic():
    """Creates all tables automatically."""
    create_videos()
    create_comments()
    create_links()
    create_link_occurrence()

if __name__ == "__main__":
    print("Do not run this file directly. Run run.py instead.")