from google_play_scraper import app
import csv
from datetime import datetime
import time
import json
from requests import get
import os
from joblib import Parallel, delayed
import shutil

json_output_folder = 'data/json'

FILEPATH = './app_ids.csv'



def execute_fetch(appName):
    try:
        print(appName)
        # Retrieving information from the Play Store
        result = app(
            appName,
            lang='en',  #
            country='uk'  #
        )

        # Removing unnecessary information
        del result["icon"]
        del result["description"]
        del result["summary"]
        del result["descriptionHTML"]
        del result["summaryHTML"]
        del result["headerImage"]
        del result["screenshots"]
        del result["video"]
        del result["videoImage"]
        del result["recentChanges"]
        del result["recentChangesHTML"]
        del result["comments"]

        # Writing the JSON information to disk
        with open('{}/{}.json'.format(json_output_folder, appName), 'w') as json_file:
            json.dump(result, json_file)

    except Exception as e:
        print(e)
        return "{} - {}".format( appName, e)

    return None

DEFAULT_PARALLELISM = 10
PARALLELISM = int(os.environ['PARALLEL_WORKERS']) if 'PARALLEL_WORKERS' in os.environ.keys() else DEFAULT_PARALLELISM

with open('error.log', 'w') as error_file:
    os.system('mkdir -p {}'.format(json_output_folder))


    with open(FILEPATH) as csvfile:
        reader = csv.DictReader(csvfile)
        cnt = 0
        batches = 1
        appIDs = []
        for row in reader:
            appID = row['handle']
            appIDs.append(appID)
            cnt += 1
            if cnt % (PARALLELISM+1) == 0:
                print("Processing batch {}".format(batches), end="\r")
                results = Parallel(n_jobs=PARALLELISM)(delayed(execute_fetch)(appID) for appID in appIDs)
                for log in results:
                    if log:
                        print(log, file=error_file)
                appIDs = []
                cnt = 0
                batches += 1

        if len(appID) != 0:
            print("Processing last batch")
            results = Parallel(n_jobs=PARALLELISM)(delayed(execute_fetch)(appID) for appID in appIDs)
            for log in results:
                if log:
                    print(log, file=error_file)
while 1:
    time.sleep(1)