import os
import csv
import subprocess
import json
import time

APK_FOLDERS = "data/apk"

FILEPATH = 'app_ids.csv'

uninstall_confirmation_coordinates = [877, 1182]

install_small_length_name = [574, 757]
install_normal_length_name = [574, 877]
install_long_length_name = [574, 997]

uninstall_small_length_name = [200, 620]
uninstall_normal_length_name = [200, 747]
uninstall_long_length_name = [200, 860]

SLEEPING_TIME_BETWEEN_ACTIONS = 3 # in seconds

SLEEPING_TIME_BETWEEN_APPS = 60 # in seconds

LIMIT_DOWNLOAD_TIME = 120 # in seconds


def installAppShortName(appID):
    os.system("adb shell am start -a android.intent.action.VIEW -d 'market://details?id={}'".format(appID))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)
    os.system('adb shell input tap {}'.format(' '.join(uninstall_small_length_name)))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)

def installAppLongName(appID):
    os.system("adb shell am start -a android.intent.action.VIEW -d 'market://details?id={}'".format(appID))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)
    os.system('adb shell input tap {}'.format(' '.join(uninstall_normal_length_name)))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)

def installAppVeryLongName(appID):
    os.system("adb shell am start -a android.intent.action.VIEW -d 'market://details?id={}'".format(appID))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)
    os.system('adb shell input tap {}'.format(' '.join(install_long_length_name)))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)

def uninstallAppShortName():
    os.system('adb shell input tap {}'.format(' '.join(uninstall_small_length_name)))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)
    os.system('adb shell input tap {}'.format(' '.join(uninstall_confirmation_coordinates)))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)

def uninstallAppLongName():
    os.system('adb shell input tap {}'.format(' '.join(uninstall_normal_length_name)))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)
    os.system('adb shell input tap {}'.format(' '.join(uninstall_confirmation_coordinates)))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)

def uninstallAppVeryLongName():
    os.system('adb shell input tap {}'.format(' '.join(uninstall_long_length_name)))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)
    os.system('adb shell input tap {}'.format(' '.join(uninstall_confirmation_coordinates)))
    time.sleep(SLEEPING_TIME_BETWEEN_ACTIONS)

def wait_and_extract(appID, LIMIT_SLEPT):
    TO_REMOVE_PREFIX = 'package:'
    TO_REMOVE_SUFFIX = '=' + appID
    INDEX_PREFIX = len(TO_REMOVE_PREFIX)

    subprocess_return = ""
    slept = 0
    while subprocess_return == "" and slept < LIMIT_SLEPT:
        # Apk has not been downloaded yet, so we wait and we retry
        time.sleep(timeToSleep)
        slept = slept + timeToSleep
        p = subprocess.Popen('adb shell pm list packages -f | grep {}'.format(appID), shell=True, stdout=subprocess.PIPE)
        subprocess_return = p.stdout.read().decode('utf-8')
    if slept >= LIMIT_SLEPT:
        return False

    INDEX_SUFFIX = len(subprocess_return) - (len(TO_REMOVE_SUFFIX) + 1)
    filepath = subprocess_return[INDEX_PREFIX:INDEX_SUFFIX]
    mobile_folderpath = filepath[:filepath.rfind('/')+1]
    destination_folderpath = "{}/{}".format(APK_FOLDERS, appID)
    os.system("mkdir {}".format(destination_folderpath))
    os.system("adb pull {} {}".format(mobile_folderpath, destination_folderpath))
    return True

def extract(appID, s):
    TO_REMOVE_PREFIX = 'package:'
    TO_REMOVE_SUFFIX = '=' + appID
    INDEX_PREFIX = len(TO_REMOVE_PREFIX)
    INDEX_SUFFIX = len(s) - (len(TO_REMOVE_SUFFIX) + 1)
    path = s[INDEX_PREFIX:INDEX_SUFFIX]


with open(FILEPATH) as csvfile:
    reader = csv.DictReader(csvfile)
    cpt = 0

    install_functions = [installAppShortName, installAppLongName, installAppVeryLongName]
    uninstall_functions = [uninstallAppShortName, uninstallAppLongName, uninstallAppVeryLongName]

    for row in reader:
        appID = row['handle']
        if appID != '' and row['source'] == 'playpass':
            cpt = cpt + 1
            for index in range(len(install_functions)):
                install_function = install_functions[index]
                install_function(appID)
                res = wait_and_extract(appID, LIMIT_DOWNLOAD_TIME)
                if res:
                    uninstall_function = uninstall_functions[index]
                    uninstall_function()
                    break
            print('Finishing app {}'.format(appID))
            time.sleep(SLEEPING_TIME_BETWEEN_APPS)