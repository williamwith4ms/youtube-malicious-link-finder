import sqlite3
import pandas as pd

def run_query(query):
    connection = sqlite3.connect("youtube.db")
    cursor = connection.cursor()
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    connection.close()
    return result


def format_query(result, query):
    # use pandas to print data frame
    df = pd.DataFrame(result)
    
    # use query to get column names by splitting the query
    columns = query.split("SELECT")[1].split("FROM")[0].strip()
    columns = columns.split(",")
    df.columns = columns
    return df


def format_hard_coded_col_names(result, columns):
    df = pd.DataFrame(result)
    df.columns = columns
    return df

def format_no_col_names(result):
    df = pd.DataFrame(result)
    return df

####################
# Pre-made queries #
####################


def get_videos():
    query = """
    SELECT * FROM videos
    """
    return format_hard_coded_col_names(run_query(query), ["video_id", "channel_id", "description", "viewcount", "published_at", "last_updated", "positive_test", "false_positive"])


def get_comments():
    query = """
    SELECT *
    FROM comments
    """
    return format_hard_coded_col_names(run_query(query), ["video_id", "comment_id", "author_id", "text", "published_at", "updated_at", "positive_test", "false_positive"])

def get_links():
    query = """
    SELECT *
    FROM links
    """
    return format_hard_coded_col_names(run_query(query), ["link_id", "url", "occurrences", "positive_test", "false_positive"])


def get_most_viewed():
    query = """
    SELECT video_id, viewcount
    FROM videos
    ORDER BY viewcount DESC
    """
    return format_query(run_query(query), query)


def get_most_common_link():
    query = """
    SELECT url
    FROM links
    ORDER BY occurrences DESC
    """
    return format_query(run_query(query), query)


def get_all_positive_test():
    query = """
    SELECT video_id, comment_id, positive_test
    FROM comments
    WHERE positive_test = 1
    UNION
    SELECT video_id, NULL AS comment_id, positive_test
    FROM videos
    WHERE positive_test = 1
    """
    return format_query(run_query(query), query)


def get_oldest_positive_test():
    query = """
    SELECT video_id, comment_id, published_at
    FROM comments
    WHERE positive_test = 1
    UNION
    SELECT video_id, NULL AS comment_id, published_at
    FROM videos
    WHERE positive_test = 1
    ORDER BY published_at ASC
    """
    return format_query(run_query(query), query)


def get_newest_positive_test():
    query = """
    SELECT video_id, comment_id, published_at
    FROM comments
    WHERE positive_test = 1
    UNION
    SELECT video_id, NULL AS comment_id, published_at
    FROM videos
    WHERE positive_test = 1
    ORDER BY published_at DESC
    """
    return format_query(run_query(query), query)


def get_false_positive():
    query = """
    SELECT video_id, comment_id, positive_test
    FROM comments
    WHERE false_positive = 1
    UNION
    SELECT video_id, NULL AS comment_id, positive_test
    FROM videos
    WHERE false_positive = 1
    """
    return format_query(run_query(query), query)


##################
# custom queries #
##################

def get(query):
    return run_query(query)

if __name__ == "__main__":
    print("dont run this file directly, use run.py instead")