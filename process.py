import sqlite3
import re
from hashlib import sha256
# load preloaded list of safe domains
SAFE_DOMAINS = []
with open("safe_domains.txt", "r") as f:
    for line in f:
        SAFE_DOMAINS.append(line.strip())


def get_rows():
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    cursor.execute("SELECT video_id,updated_at, description FROM videos")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def process_row(row):
    _, _, description = row
    if description == "":
        return 0
    
    # regex to get a list of all links in the description
    links = re.findall(r'(https?://[^\s]+)', description)
    if len(links) == 0:
        return 0
    return links

def process_links(links,row):
    video_id, updated_at, _ = row
    
    bad_links = []
    for link in links:
        # check if link is in the safe domains list
        safe = False
        for domain in SAFE_DOMAINS:
            if str.startswith(link, domain):
                safe = True
                break
        if safe:
            continue
        else:
            bad_links.append(link)
                
    
    
    return bad_links, len(bad_links)
            
def create_link(row, link):
    video_id, updated_at, _ = row
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    
    link_id = sha256(link.encode()).hexdigest()
    # check if link already exists
    cursor.execute("SELECT link_id FROM links WHERE link_id=?", (link_id,))
    result = cursor.fetchone()
    
    
    if result == None:
        cursor.execute("INSERT INTO links VALUES (?,?,?,?,?)", (link_id, link,None,None,None))
    
    # create occurrence for the link
    # check if the link is already in the table
    cursor.execute("SELECT * FROM link_occurrence WHERE link_id=? AND video_id=?", (link_id, video_id))
    result = cursor.fetchone()
    if result == None:
        cursor.execute("INSERT INTO link_occurrence VALUES (?,?,?)", (link_id, video_id, None))
    
    connection.commit()
    connection.close()
    
        
            
            
def process_videos():
    rows = get_rows()
    for row in rows:
        links = process_row(row)
        if links == 0:
            continue
        links, result = process_links(links, row)
        if result == 0:
            continue
        for link in links:
            create_link(row, link)

def get_comments():
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    cursor.execute("SELECT comment_id, updated_at, text FROM comments")
    result = cursor.fetchall()
    cursor.execute("SELECT video_id FROM comments")
    extra = cursor.fetchall()
    cursor.close()
    connection.close()
    return result, extra

def create_link_comment(row, link, video_id):
    comment_id, updated_at, _ = row
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    
    link_id = sha256(link.encode()).hexdigest()
    # check if link already exists
    cursor.execute("SELECT link_id FROM links WHERE link_id=?", (link_id,))
    result = cursor.fetchone()
    if result == None:
        cursor.execute("INSERT INTO links VALUES (?,?,?,?,?)", (link_id, link,None,None,None))
    
    # create occurrence for the link
    # check if the link is already in the table
    cursor.execute("SELECT * FROM link_occurrence WHERE link_id=? AND comment_id=?", (link_id, comment_id))
    result = cursor.fetchone()
    if result == None:
        cursor.execute("INSERT INTO link_occurrence VALUES (?,?,?)", (link_id, video_id, comment_id))
    
    connection.commit()
    connection.close()
    
def process_comments():
    rows, extra = get_comments()
    for row in rows:
        links = process_row(row)
        if links == 0:
            continue
        links, result = process_links(links, row)
        if result == 0:
            continue
        for i, link in enumerate(links):
            create_link_comment(row, link, str(extra[i][0]))
        
def process_positive_test_video():
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    
    # if video_id is refranced in the occurance table, set positive_test to True
    cursor.execute("SELECT video_id FROM link_occurrence")
    result = cursor.fetchall()
    for video_id in result:
        cursor.execute("UPDATE videos SET positive_test=1 WHERE video_id=?", (video_id[0],))
    connection.commit()

def process_positive_test_comment():
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    
    # if comment_id is refranced in the occurance table, set positive_test to True
    cursor.execute("SELECT comment_id FROM link_occurrence")
    result = cursor.fetchall()
    for comment_id in result:
        cursor.execute("UPDATE comments SET positive_test=1 WHERE comment_id=?", (comment_id[0],))
    connection.commit()
        
def process_link_occurrences():
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    
    # get all link ids
    cursor.execute("SELECT link_id FROM links")
    result = cursor.fetchall()
    for link_id in result:
        # get all occurrences for the link
        cursor.execute("SELECT video_id, comment_id FROM link_occurrence WHERE link_id=?", (link_id[0],))
        occurrences = cursor.fetchall()
        cursor.execute("UPDATE links SET occurrences=? WHERE link_id=?", (len(occurrences), link_id[0]))
    connection.commit()
        
def process_occurrence_times():
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    
    # get all link ids
    cursor.execute("SELECT link_id FROM links")
    result = cursor.fetchall()
    
    # get the oldest uploaded date of a video that contains the link
    for link_id in result:
        # get all occurrences for the link
        cursor.execute("SELECT video_id FROM link_occurrence WHERE link_id=?", (link_id[0],))
        occurrences = cursor.fetchall()
        # get uploaded date of all videos that contain the link
        dates = []
        for video_id in occurrences:
            video_id = video_id[0]
            try:
                cursor.execute("SELECT published_at FROM videos WHERE video_id=?", (video_id,))
                date = cursor.fetchone()
                dates.append(date[0])
            except:
                cursor.execute("SELECT published_at FROM comments WHERE video_id=?", (video_id,))
                date = cursor.fetchone()
                dates.append(date[0])
            dates.sort()
            cursor.execute("UPDATE links SET oldest_occurrence=? WHERE link_id=?", (dates[0], link_id[0]))
            dates.reverse()
            cursor.execute("UPDATE links SET newest_occurrence=? WHERE link_id=?", (dates[0], link_id[0]))
    connection.commit()
    connection.close()


def main():
    # # create links and tables
    process_videos()
    process_comments()
    
    # # process positive tests
    process_positive_test_video()
    process_positive_test_comment()
    
    # calculate number of occurrences
    process_link_occurrences()
    process_occurrence_times()

if __name__ == "__main__":
    main()