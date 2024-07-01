import sqlite3

connection = sqlite3.connect("youtube.db")
cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='videos'")
table_exists = cursor.fetchone()
cursor.close()
cursor = connection.cursor()
if table_exists:
    result = input("Table already exists. Would you like to drop it? (yes/N): ")
    if result.lower() == "yes":
        result = input("Are you sure? This WILL result in a loss of data (yes/N): ")
        if result.lower() == "yes":
            cursor.execute("DROP TABLE videos")
            cursor.execute("DROP TABLE comments")
            print("Table dropped successfully")
            result = input("Would you like to recreate the table? (Y/n): ")
            if result == "n":
                print("Exiting...")
                exit()
            else:
                pass
        else:
            print("Exiting...")
            exit()
    else:
        print("Exiting...")
        exit()


VIDEOS = """ CREATE TABLE videos (
    video_id CHAR(11),
    channel_id CHAR(24),
    description text,
    viewcount integer,
    updated_at timestamp,
    recorded_at timestamp,
    positive_test boolean,
    false_positive boolean,
    PRIMARY KEY (video_id, recorded_at)
)"""

COMMENTS = """ CREATE TABLE comments (
    comment_id CHAR(26),
    video_id CHAR(11),
    author_id CHAR(24),
    text text,
    published_at timestamp,
    recorded_at timestamp,
    positive_test boolean,
    false_positive boolean,
    PRIMARY KEY (comment_id, video_id)
    )"""

cursor.execute(VIDEOS)
cursor.execute(COMMENTS)

print("Table created successfully")

connection.commit()
connection.close()
