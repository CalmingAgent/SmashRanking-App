import timeit
import pysmashgg
import os
import json
import sys
from pysmashgg.api import run_query
import time
import logging

#parent directory import
sys.path.append("Database")
import SQLite

#SSBU ID
game_id = 1386
game_release_date = 1544158800 #dec 7 2018
todays_date = 1651557600 #5.03.22 AT 00:00:00
num_request = 0
file_year = "1Test"
year_2019 = 1575694800 #dec 7 2019
year_2020 = 1607317200 #dec 7 2020
year_2021 = 1638853200 #dec 7 2021
test = True

#DEBUG = Detailed information, typically of interest only when diagnosing problems
#INFO = Confirmation that things are working as expected.
#WARNING = An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected. 
#ERROR =  Due to a more serious problem, the software has not been able to perform some function.
#Critical = indicating that the program itself may be unable to continue running.

logger = logging.getLogger(__name__)
#getting current logging level
if SQLite.SQLite.debuging == True:
    logger.setLevel(logging.DEBUG)
elif SQLite.SQLite.info == True:
    logger.setLevel(logging.INFO)
elif SQLite.SQLite.error == True:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel
#formats log
formatter = logging.Formatter("  %(pathname)s\n\tlevel: %(levelname)s \n\ttime: %(asctime)s\n\tFunction: %(funcName)s,\
        \n\tMessage: %(message)s\n-----------------------------------------------------------------")
#handles and sets the file/file formating
file_handler = logging.FileHandler("Gatherdata_SmashGG_log.log")
file_handler.setFormatter(formatter)
#adds handler
logger.addHandler(file_handler)

def get_num_page(smash, event_id, other:int):
    global num_request
    pages = 1
    #items per page
    items = 1
    num_of_retrys = 0
    if other < 0:
        while items !=0:
            try:
                items =len(smash.event_show_sets(event_id,pages))
                #add loger for items
                logger.info(f"event pages = {pages}: event items = {items}")
                num_request += 1
                pages += 1
            except:
                num_of_retrys +=1
                time.sleep(30)
                if num_of_retrys > 10:
                    print("end of the line")
                    items = 0

            if num_request % 70 == 0:
                time.sleep(30)
                num_request = 0
    #gets standings pages
    else:
        logger.info(f"event_id = {event_id}")
        while items !=0:
            try:
                items = len(smash.event_show_lightweight_results(event_id, pages))
                logger.info(f"standing pages = {pages}: standing items = {items}")
                num_request += 1
                pages += 1
            except:
                num_of_retrys +=1
                time.sleep(30)
                if num_of_retrys > 10:
                    print("end of the line")
                    items = 0

            if num_request % 70 == 0:
                time.sleep(30)
                num_request = 0

    print(f"number of pages: {pages}")
    return pages

def get_num_page_tourn(entrants_limit:int, game_id:int, game_release_date:int, year_2019:int, page:int):
    global num_request
    pages = 1
    #items per page
    items = 1
    num_of_retrys = 0
    while items !=0:
            print(pages)
            try:
                items =len(smash.tournament_show_event_by_game_size_dated(entrants_limit, game_id, game_release_date, year_2019, pages))
                #add loger for items
                logger.info(f"length of tourn items {items}")
                num_request += 1
                pages += 1
            except:
                num_of_retrys +=1
                time.sleep(30)
                if num_of_retrys > 10:
                    print("end of the line")
                    items = 0
            if num_request % 70 == 0:
                time.sleep(30)
                num_request = 0
    print(f"number of pages: {pages}")
    return pages


# check number of request at end of method, if request 
'''prints event details to a file'''
def events (smash,event_id):
    global num_request
    with open("events" + file_year + ".txt", "a", encoding="utf-8") as f:
        sys.stdout = f
        event_page = 1
        num_pages = get_num_page(smash,event_id,-1)
        while event_page <= num_pages:
            if num_request % 70 == 0:
                time.sleep(30)
                num_request = 0
            try:
                sets = smash.event_show_sets(event_id,event_page)
                num_request+= 1

            except:
                    event_page -= 1
                    time.sleep(60)
                    print(f"reached end of event, if error will retry")

            event_page +=1
            for set in sets:
                if set['completed'] == True:
                    print(f"(player1: {set['entrant1Id']}| player2: {set['entrant2Id']}| p1_score: {set['entrant1Score']}| p2_score: {set['entrant2Score']}); ")
                    print("--------------------------------------------------------------------------------------------------------")
                logger.info(f"full sets: {set}")
        
        print("tourney results")
        event_page = 1
        num_pages = get_num_page(smash,event_id,0)
        while event_page <= num_pages:
            if num_request % 70 == 0:
                time.sleep(30)
                num_request = 0
            try:
                standings = smash.event_show_lightweight_results(event_id, event_page)
                num_request+= 1

            except:
                    event_page -= 1
                    time.sleep(60)
                    print(f"reached end of event, if error will retry")

            event_page +=1
            for standing in standings:
                print(standing)
                print("-----------------")


def tournament(smash):
    global num_request
    entrants_limit = 50
    page = 1
    online = "online"
    ult_id = "eventId"
    num_page = get_num_page_tourn(entrants_limit, game_id, game_release_date, year_2019, page)
    while page <= num_page:
        tournaments = smash.tournament_show_event_by_game_size_dated(entrants_limit, game_id, game_release_date, year_2019, page)
        num_request += 1
        for tournament in tournaments:
            with open("tournaments" + file_year + ".txt", 'a', encoding="utf-8") as f1:
                sys.stdout = f1
                if tournament[online] == False and ("singles" in tournament['eventName'].lower()):
                    print(f"tournament name: {tournament['tournamentName']}")
                    event_id = tournament[ult_id]
                    events(smash,event_id)
                    logger.info(f"tournament = {tournament}\n\n\n")
        page += 1

key_file = "/Tokens12Xxg.json"
if os.path.exists(os.getcwd() + key_file): 
    with open("." + key_file) as f:
        config_data = json.load(f)
else:
    #have to run once to create json file
    template = {"Token": ""}

    with open(os.getcwd() + key_file, "w+") as f:
        json.dump(template, f)
token = config_data["Token"]
smash = pysmashgg.SmashGG(token)
#events(smash, 267495)
tournament(smash)

#1386 for Ultimate
#first event id 124827
