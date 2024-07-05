"""This file is used for running cron jobs. it will need to be edited manually"""
import process
import run
import os
#####################
# EDIT THIS SECTION #
#####################

QUERY = ["INSERT", "YOUR", "QUERIES", "HERE"]
PROCESS_SEARCH = True

###################
# DONT EDIT BELOW #
###################

import os
script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)

run.search_youtube(QUERY)

if PROCESS_SEARCH:
    process.process_all()