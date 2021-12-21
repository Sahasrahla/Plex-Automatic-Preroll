#!/usr/bin/python
import subprocess
import sys
try:
    from plexapi.server import PlexServer

except:
    print('\033[91mERROR:\033[0m PlexAPI is not installed.')
    x = input("Do you want to install it? y/n:")
    if x == 'y':
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'PlexAPI==4.2.0'])
        from plexapi.server import PlexServer
    elif x == 'n':
        sys.exit()

import re
import requests
import yaml
from urllib.parse import quote_plus, urlencode
import datetime
from dateutil.easter import *

from plexapi import media, utils, settings, library
from plexapi.base import Playable, PlexPartialObject
from plexapi.exceptions import BadRequest, NotFound

from argparse import ArgumentParser
import os
import random
import shutil
import pathlib
from configparser import *

print('#############################')
print('#                           #')
print('#  Plex Automated Preroll!  #')
print('#                           #')
print('#############################' + '\n')


file = pathlib.Path("config.yml")
if file.exists():
    print('Pre-roll updating...')
else:
    Master = ','
    print('No config file found! Lets set one up!')
    file1 = open("config.yml", "w+")
    file1.write("Plex: " + "\n")
    x = input("Enter your (https) plex url:")
    file1.write("  url: " + x + "\n")
    x = input("Enter your plex token: (not sure what that is go here "
              "https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/): ")
    file1.write("  token: " + x + "\n")
    file1.write("MasterList: "  + "\n")
    x = input("Do you want to enable a Masterlist of Trailers? (Y/N)")
    if x.lower() == 'y':
        file1.write("  UseMaster: " + "Yes" + "\n")
        x = input("Do you want Plex to play the items in the Masterlist randomly? (Y/N)")
        if x.lower() == 'y':
            Master = ';'
            file1.write("  MasterRandom: " + "Yes" + "\n")
        else:
            Master = ','
            file1.write("  MasterRandom: " + "No" + "\n")
        file1.write("# If the path for the Master List is left blank the script will create the path " + "\n")
        file1.write("# based on if Monthly, Weekly, or Daily are set to be used in the Master List " + "\n")
        file1.write("# otherwise you can populate the path with your own set of trailers" + "\n")
        file1.write("  Path: ")
    else:
        file1.write("  UseMaster: " + "No"  + "\n")
        file1.write("  MasterRandom: " + "No"  + "\n")
        file1.write("  # If the path for the Master List is left blank the script will create the path " + "\n")
        file1.write("  # based on if Monthly, Weekly, or Daily are set to be used in the Master List " + "\n")
        file1.write("  # otherwise you can populate the path with your own set of trailers" + "\n")
        file1.write("  Path: "  + "\n")
    file1.write("Monthly: "  + "\n")
    x = input("Do you want to enable Monthly Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path(s) you enter!')
        x = input("Enter the January trailer path(s):" + "\n")
        res = re.split(',|;', x)
        file1.write("  Jan: " + x)
        x = input("Enter the February trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  Feb: " + x)
        x = input("Enter the March trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  Mar: " + x)
        x = input("Enter the April trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  Apr: " + x)
        x = input("Enter the May trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  May: " + x)
        x = input("Enter the June trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  June: " + x)
        x = input("Enter the July trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  July: " + x)
        x = input("Enter the August trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  Aug: " + x)
        x = input("Enter the September trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  Sept: " + x)
        x = input("Enter the October trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  Oct: " + x)
        x = input("Enter the November trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  Nov: " + x)
        x = input("Enter the December trailer path(s):" + "\n")
        res = res + re.split(',|;', x)
        file1.write("  Dec: " + x)
        x = input("Do you want to use the Monthly list in the Master list? (Y/N)")
        if x.lower() == 'y':
            file1.write("  MasterList: Yes" + "\n")
        else:
            file1.write("  MasterList: No" + "\n")
        listToStr = Master.join([str(elem) for elem in res])
        file1.write("  MasterListValue: " + listToStr)
        file1.write("  UseMonthly: Yes" + "\n")
    else:
        file1.write("  Jan: " + "\n")
        file1.write("  Feb: " + "\n")
        file1.write("  Mar: " + "\n")
        file1.write("  Apr: " + "\n")
        file1.write("  May: " + "\n")
        file1.write("  June: " + "\n")
        file1.write("  July: " + "\n")
        file1.write("  Aug: "  + "\n")
        file1.write("  Sept: " + "\n")
        file1.write("  Oct: " + "\n")
        file1.write("  Nov: " + "\n")
        file1.write("  Dec: " + "\n")
        file1.write("  MasterList: No" + "\n")
        file1.write("  MasterListValue: " + "\n")
        file1.write("  UseMonthly: No" + "\n")
    file1.write("Weekly: " + "\n")
    x = input("Do you want to enable Weekly Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path you enter!')
        print("Enter the Start Date: " + "\n")
        year = int(input('Enter a year: '))
        month = int(input('Enter a month: '))
        day = int(input('Enter a day: '))
        date1 = datetime.date(year, month, day)
        file1.write("  StartDate: " + str(date1) + "\n")
        print("Enter the End Date:")
        year = int(input('Enter a year: '))
        month = int(input('Enter a month: '))
        day = int(input('Enter a day: '))
        date1 = datetime.date(year, month, day)
        file1.write("  EndDate: " + str(date1))
        x = input("Enter the trailer path(s):" + "\n")
        file1.write("  Path: " + x)
        x = input("Do you want to use the Weekly list in the Master list? (Y/N)")
        if x.lower() == 'y':
            file1.write("  MasterList: Yes" + "\n")
        else:
            file1.write("  MasterList: No" + "\n")
        file1.write("  UseDaily: Yes" + "\n")
    else:
        file1.write("  StartDate: " + "\n")
        file1.write("  EndDate: " + "\n")
        file1.write("  Path: " + "\n")
        file1.write("  MasterList: No" + "\n")
        file1.write("  UseWeekly: No" + "\n")
    file1.write("Daily: " + "\n")
    x = input("Do you want to enable Daily Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path you enter!')
        print("Enter the Start Date: ")
        year = int(input('Enter a year: '))
        month = int(input('Enter a month: '))
        day = int(input('Enter a day: '))
        date1 = datetime.date(year, month, day)
        file1.write("  StartDate: " + str(date1) + "\n")
        print("Enter the End Date:")
        year = int(input('Enter a year: '))
        month = int(input('Enter a month: '))
        day = int(input('Enter a day: '))
        date1 = datetime.date(year, month, day)
        file1.write("  EndDate: " + str(date1) + "\n")
        x = input("Enter the trailer path(s):")
        file1.write("  Path: " + x + "\n")
        x = input("Do you want to use the Daily list in the Master list? (Y/N)")
        if x.lower() == 'y':
            file1.write("  MasterList: Yes" + "\n")
        else:
            file1.write("  MasterList: No" + "\n")
        file1.write("  UseDaily: Yes" + "\n")
    else:
        file1.write("  StartDate: " + "\n")
        file1.write("  EndDate: " + "\n")
        file1.write("  Path: " + "\n")
        file1.write("  MasterList: No" + "\n")
        file1.write("  UseDaily: No" + "\n")
    file1.write("Misc: " + "\n")
    x = input("Do you want to enable Misc (Random with one static trailer) Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path you enter!')
        x = input("Enter the trailer path(s):")
        file1.write("  Path: " + x + "\n")
        x = input("Enter the static trailer path:")
        file1.write("  StaticTrailer: " + x + "\n")
        x = input("Enter the number of trailers to use ex: Path contains 5 trailers you set this value to 2 the "
                  "program will pick two at random as well as the static trailer to play in order:")
        file1.write("  TrailerListLength: " + x + "\n")
        file1.write("  UseMisc: Yes" + "\n")
    else:
        file1.write("  Path: " + "\n")
        file1.write("  StaticTrailer: " + "\n")
        file1.write("  TrailerListLength: " + "\n")
        file1.write("  UseMisc: No" + "\n")
    print('config file (config.yml) created')
    file1.close()

def getArguments():
    name = 'Automated-Plex-Preroll-Trailers'
    version = '1.1.0'
    parser = ArgumentParser(description='{}: Set monthly trailers for Plex'.format(name))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(name, version), help="show the version number and exit")
    args = parser.parse_args()


def main():
    sort = ','
    x = datetime.date.today()
    res = "null"
    # Open config
    with open('config.yml', 'r') as file:
        doc = yaml.load(file, Loader=yaml.SafeLoader)

    # Arguments
    arguments = getArguments()
    # Thanks to https://github.com/agrider for the reordering and error handling for pre-roll paths
    if doc["Plex"]["url"] is not None:
        session = requests.Session()
        session.verify = False
        requests.packages.urllib3.disable_warnings()
        plex = PlexServer(doc["Plex"]["url"], doc["Plex"]["token"], session, timeout=None)
        prerolls = ''
        i = 0
        ThanksgivingDay = 22 + (10 - datetime.date(x.year,11,1).weekday()) % 7

        # Valentine's Day - Feb 14th
        if x.strftime("%b%d") == 'Feb14':
            count = len(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Valentines'))
            if count <= 10:
                for file in os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Valentines'):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Valentines", file) + ";"
                    i = i + 1
            else:
                for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Valentines'), 10):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Valentines", file) + ";"
                    i = 10
        # April Fools' Day - April 1st
        elif x.strftime("%b%d") == 'Apr01':
            count = len(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\April Fools'))
            if count <= 10:
                for file in os.listdir(r'\\plex\c$\Plex\Pre-roll videos\April Fools'):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\April Fools", file) + ";"
                    i = i + 1
            else:
                for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\April Fools'), 10):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\April Fools", file) + ";"
                    i = 10
        # Independence Day - July 4th
        elif x.strftime("%b%d") == 'Jul04':
            count = len(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Independence Day'))
            if count <= 10:
                for file in os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Independence Day'):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Independence Day", file) + ";"
                    i = i + 1
            else:
                for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Independence Day'), 10):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Independence Day", file) + ";"
                    i = 10
        # Mardi Gras - 47 days before Easter
        if easter(x.year) - datetime.timedelta(days=47) == x:
            count = len(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Mardi Gras'))
            if count <= 10:
                for file in os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Mardi Gras'):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Mardi Gras", file) + ";"
                    i = i + 1
            else:
                for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Mardi Gras'), 10):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Mardi Gras", file) + ";"
                    i = 10


        # Easter - Good Friday through Easter Sunday
        if easter(x.year) - datetime.timedelta(days=3) <= x <= easter(x.year):
            count = len(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Easter'))
            if count <= 10:
                for file in os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Easter'):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Easter", file) + ";"
                    i = i + 1
            else:
                for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Easter'), 10 - i):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Easter", file) + ";"
                    i = 10
        # Halloween - Last week of October
        elif x.strftime("%b") == "Oct" and int(x.strftime("%d")) >= 23:
            count = len(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Halloween'))
            if count <= 10:
                for file in os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Halloween'):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Halloween", file) + ";"
                    i = i + 1
            else:
                for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Halloween'), 10 - i):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Halloween", file) + ";"
                    i = 10
        # Thanksgiving - Week of...
        elif datetime.date(x.year,11,ThanksgivingDay) - datetime.timedelta(days=3) <= x <= datetime.date(x.year,11,ThanksgivingDay) + datetime.timedelta(days=4):
            count = len(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Thanksgiving'))
            if count <= 10:
                for file in os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Thanksgiving'):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Thanksgiving", file) + ";"
                    i = i + 1
            else:
                for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Thanksgiving'), 10 - i):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Thanksgiving", file) + ";"
                    i = 10
        # Christmas + New Years - Dec 24th through end of year
        elif x.strftime("%b") == "Dec" and int(x.strftime("%d")) >= 24:
            count = len(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Christmas'))
            if count <= 10:
                for file in os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Christmas'):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Christmas", file) + ";"
                    i = i + 1
            else:
                for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Christmas'), 10 - i):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Christmas", file) + ";"
                    i = 10

        # Add pre-rolls from Monthly folder up to max 10
        if i < 10:
            count = len(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\\' + str(x.strftime("%B"))))
            if count < 10 - i:
                for file in os.listdir(r'\\plex\c$\Plex\Pre-roll videos\\' + str(x.strftime("%B"))):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\\" + str(x.strftime("%B")), file) + ";"
                    i = i + 1
            else:
                for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\\' + str(x.strftime("%B"))), 10 - i):
                    prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\\" + str(x.strftime("%B")), file) + ";"
                    i = 10
        # Add random pre-rolls from Default folder up to max 10
        if i < 10:
            for file in random.sample(os.listdir(r'\\plex\c$\Plex\Pre-roll videos\Default'), 10 - i):
                prerolls = prerolls + os.path.join("C:\Plex\Pre-roll videos\Default", file) + ";"
        if str(doc["Misc"]["UseMisc"]).lower() == 'true':
            if str(doc["Misc"]["Random"]).lower() == 'true':
                sort = ';'
            else:
                sort = ','
            res = re.split(',|;', doc["Misc"]["Path"])
            i = 1
            while i < int(doc["Misc"]["TrailerLength"]):
                trailer = trailer + sort + res[random.randint(0, len(res) - 1)]
                i += 1
            trailer = trailer + sort + doc["Misc"]["StaticTrailer"]
            prerolls = trailer
        prerolls = prerolls.rstrip(';')
        plex.settings.get('cinemaTrailersPrerollID').set(prerolls)    
        plex.settings.save()
        #print(prerolls)
        print('Pre-roll updated')

if __name__ == '__main__':
    main()
