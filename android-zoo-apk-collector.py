from google_play_scraper import app
import csv
from datetime import datetime
import time
import json
from requests import get
import os
from joblib import Parallel, delayed
import shutil

# AndroZoo variables
apiKey = os.environ['ANDROID_ZOO_KEY']
androZooUrl = "https://androzoo.uni.lu/api/download?apikey={}&sha256={}"

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


def download_androzoo_apk(appID):
    try:
        filename = '{}.apk'.format(appID)

        # Get the sha according to the appID
        sha = ""
        with open(androzoo_csv_filepath) as androzoo_csv_file:
            androzoo_csv_reader = csv.DictReader(androzoo_csv_file)
            for row in androzoo_csv_reader:
                if row['pkg_name'] == appID:
                    sha = row['sha256']
                    break
        if sha != "":
            download_filepath = apks_folder + '/' + filename
            download(androZooUrl.format(apiKey, sha), download_filepath)
    except Exception as e:
        print(e)
        return "{} - {}".format( appName, e)
    return None

androzoo_csv_reader = ""
androzoo_csv_filepath = "latest.csv"

csv_filepath = "app_ids.csv"

apks_folder = "data/androzoo_apks"

DEFAULT_PARALLELISM = 10
PARALLELISM = int(os.environ['PARALLEL_WORKERS']) if 'PARALLEL_WORKERS' in os.environ.keys() else DEFAULT_PARALLELISM

os.system('mkdir -p {}'.format(apks_folder))

with open(csv_filepath) as csv_file:
    with open('error.log', 'w') as error_file:
        csv_reader = csv.DictReader(csv_file)

        cnt = 0
        batches = 1
        appIDs = []
        for row in csv_reader:
            appID = row['handle']
            if appID != "" and row['source'] == 'android_zoo':
                appIDs.append(appID)
                cnt += 1
                if cnt % (PARALLELISM+1) == 0:
                    print("Processing batch {}".format(batches), end="\r")
                    results = Parallel(n_jobs=PARALLELISM)(delayed(download_androzoo_apk)(appID) for appID in appIDs)
                    for log in results:
                        if log:
                            print(log, file=error_file)
                    appIDs = []
                    cnt = 0
                    batches += 1

        if len(appIDs) != 0:
            print("Processing last batch")
            results = Parallel(n_jobs=PARALLELISM)(delayed(download_androzoo_apk)(appID, androzoo_csv_reader) for appID in appIDs)
            for log in results:
                if log:
                    print(log, file=error_file)
