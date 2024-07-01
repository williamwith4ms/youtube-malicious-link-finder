from search import search_youtube
import createdb
import process


def search_youtube_manager():
    """Manages the search youtube function."""
    queries = []
    while(True):
        result = input(f"""
Search Youtube
current queries: {queries}
    1. Add query
    2. Remove query
    3. Search
    b. Back
    q. Exit
""")
        
        if result == "1":
            query = input(f"""\nEnter query\n(Tip you can use , to add multiple queries at once): """).split(",")
            queries.extend(query)
        elif result == "2":
            remove = input("\nEnter query to remove\n(Tip you can use , to remove multiple queries at once): """).split(",")
            for query in remove:
                queries.remove(query)
        elif result == "3":
            search_youtube(queries)
        elif result == "b":
            break
        elif result == "q":
            exit()
        
        
def process_data_manager():
    """manages the process data function."""
    while(True):
        result = input(f"""
Process Data
(if you dont know what you are doing only use option 1, the rest is for advanced use cases)
    1. Run all (recommended)
    2. Process all
    3. Positive test
    4. Process link occurrences
    5. Advanced
    b. Back
    q. Exit
""")
        if result == "1":
            process.all()
        elif result == "2":
            process.process_all()
        elif result == "3":
            process.process_positive_test()
        elif result == "4":
            process.process_link_occurrences()
        elif result == "5":
            process_data_advanced()
        elif result == "b":
            break
        elif result == "q":
            exit()
    
    
def process_data_advanced():
    """Manages the advanced data processing."""
    result = input(f"""
Advanced Data Processing
    1. Process comments (only)
    2. Process video (only)
    3. Positive test video (only)
    4. Positive test comment (only)
    5. Process occurrence times (only)
    b. Back
    q. Exit""")
    if result == "1":
        process.process_comments()
    elif result == "2":
        process.process_videos()
    elif result == "3":
        process.process_positive_test_video()
    elif result == "4":
        process.process_positive_test_comment()
    elif result == "5":
        process.process_occurrence_times()
    elif result == "b":
        return
    elif result == "q":
        exit()


def create_db_manager():
    """manages the create database function."""
    while(True):
        result = input(f"""
Create Database
    1. Automated (recommended)
    2. Manual
    b. Back
    q. Exit""")
        
        if result == "1":
            createdb.create_automatic()
        elif result == "2":
            create_db_manual()
        elif result == "b":
            break
        elif result == "q":
            exit()


def create_db_manual():
    """Manages the manual database creation."""
    while(True):
        result = input(f"""
Manual Database Creation
    1. Create Videos
    2. Create Comments
    3. Auto Create Links
    4. Create Links (advanced)
    5. Create Link Occurrence (advanced)
    b. Back
    q. Exit
""")
    
        if result == "1":
            createdb.create_videos()
        elif result == "2":
            createdb.create_comments()
        elif result == "3":
            createdb.auto_links()
        elif result == "4":
            result = input("This will cause problems if the link occurrence table is not created, are you sure? (y/n): ")
            if result == "y":
                createdb.create_links()
        elif result == "5":
            result = input("This will cause problems if the links table is not created, are you sure? (y/n): ")
            createdb.create_link_occurrence()
        elif result == "b":
            break
        elif result == "q":
            exit()
    

def main():
    """Main function that manages the main options."""
    while(True):
        # main options
        result = input(f"""Youtube Malicious Link Finder
    1. Search Youtube
    2. Process Data
    3. Query Data (not implemented)
    4. Create Database
    q. Exit
""")
        
        if result == "1":
            search_youtube_manager()
        elif result == "2":
            process_data_manager()
        elif result == "3":
            print("Not implemented")
        elif result == "4":
            create_db_manager()
        elif result == "q":
            break
        
        

if __name__ == "__main__":
    main()