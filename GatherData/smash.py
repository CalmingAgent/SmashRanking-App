import pysmashgg
import os
import json
import sys
import time
import logging

#parent directory import
sys.path.append("Database")
import SQLite

orgnl_stdout = sys.stdout

#SSBU ID
game_id = 1386
game_release_date = 1544158800 #dec 7 2018

#total number of requests made to Smash.gg API, allowed 80 per minute
num_request = 0
#year of date gathered
file_year = "4"
year_2019 = 1575694800 #dec 7 2019
year_2020 = 1607317200 #dec 7 2020
year_2021 = 1638853200 #dec 7 2021
todays_date = int(time.time())
year_start = 1651305600
year_end= todays_date

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
    logger.setLevel(logging.CRITICAL)

#formats log
formatter = logging.Formatter("  %(pathname)s\n\tlevel: %(levelname)s \n\ttime: %(asctime)s\n\tFunction: %(funcName)s,\
        \n\tMessage: %(message)s\n-----------------------------------------------------------------")

#handles and sets the file/file formating
file_handler = logging.FileHandler("Gatherdata_SmashGG_log.log", "w", "utf-8")
file_handler.setFormatter(formatter)

#adds handler
logger.addHandler(file_handler)

'''returns the number of pages in an event
    takes in the Smash object and the event id for location'''
def get_num_page_events(smash, event_id):
    global num_request
    pages = 1
    #items per page
    items = 1
    #tests to see if there was too many requests made, 5 minutes sleep and 5 request made.
    num_of_retrys = 0
    #tests whether there are not items left, no items = no page
    while items !=0:
        try:
            items =len(smash.event_show_sets(event_id,pages))
            #add loger for items
            logger.debug(f"event pages = {pages}: event items = {items}")
            num_request += 1
            pages += 1
        except:
            num_of_retrys +=1
            time.sleep(15)
            if num_of_retrys > 10:
                logger.debug("no more events")
                items = 0

        if num_request % 70 == 0:
            time.sleep(30)
            num_request = 0

    print(f"number of event pages: {pages}")
    return pages

def get_num_page_standings(smash, event_id):
    global num_request
    pages = 1
    #items per page
    items = 1
    num_of_retrys = 0
    logger.debug(f"event_id = {event_id}")
    while items !=0:
        logger.debug(f"Before: standing pages = {pages}: standing items = {items}")
        try:
            items = len(smash.event_show_lightweight_results(event_id, pages))
            num_request += 1
            pages += 1
            logger.debug(f"standing pages = {pages}: standing items = {items}")
        except:
            logger.debug(f"retrys: {num_of_retrys} standing pages = {pages}: standing items = {items}")
            num_of_retrys +=1
            time.sleep(15)
            if num_of_retrys > 10:
                print("end of the line")
                items = 0

        if num_request % 70 == 0:
            time.sleep(30)
            num_request = 0
    print(f"number of standing pages: {pages}")
    return pages

def get_num_page_tourn(entrants_limit:int, game_id:int, game_release_date:int, year_2019:int, page:int):
    global num_request
    pages = 1
    #items per page
    items = 1
    num_of_retrys = 0
    while items !=0:
        logger.debug(f"Before: length of tourn items {items} and pages: {pages}")
        try:
            tournaments = smash.tournament_show_event_by_game_size_dated(entrants_limit, game_id, game_release_date, year_2019, pages)
            items =len(tournaments)
            num_request += 1
            pages += 1
            logger.debug(f"after: length of tourn items {items}, pages: {pages} \n {tournaments} \n\n")
        except:
            num_of_retrys +=1
            time.sleep(15)
            if num_of_retrys > 10:
                logger.debug("end of the line")
                items = 0
        if num_request % 70 == 0:
            time.sleep(30)
            num_request = 0
    
    return pages


# check number of request at end of method, if request 
'''prints smash event details to a file'''
def events (smash,event_id, tourney):
    global num_request
    with open("events" + file_year + ".txt", "a", encoding="utf-8") as events_file:
        sys.stdout = events_file
     
        print(f"{tourney['tournamentName']} \nends at: {tourney['endAt']} \ntourney standings")
        event_page = 1
        num_pages = get_num_page_standings(smash,event_id)
        #nothing in SKulls Smash.gg API for returning in progress tourneys so this is a work around, in progress tourneys return 1 page
        # because in progress tourneys have no standinds 
        if num_pages > 1:
            logger.debug(f"tourney_page: {event_page} num_pages {num_pages}")
            while event_page <= num_pages:
                if num_request % 70 == 0:
                    time.sleep(30)
                    num_request = 0
                try:
                    standings = smash.event_show_lightweight_results(event_id, event_page)
                    num_request+= 1

                except:
                        event_page -= 1
                        time.sleep(30)
                        print(f"reached end of event, if error will retry")

                event_page +=1
                for standing in standings:
                    print(standing)
                    print("-----------------")
                
            event_page = 1
            num_pages = get_num_page_events(smash,event_id)
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
        else:
            logger.critical(f"Tourney in progress, will crash program")


def tournament(smash):
    global num_request
    global year_start
    global year_end
    continue_date = year_start
    entrants_limit = 50
    page = 1
    online = "online"
    ult_id = "eventId"
    num_pages = get_num_page_tourn(entrants_limit, game_id, year_start, year_end, page)
    previous_tournament = []
    current_tournament = []
    while num_pages != 0:
        try:
            tournaments = smash.tournament_show_event_by_game_size_dated(entrants_limit, game_id, year_start, year_end, page)
        except:
            year_start = continue_date
            page = 0
            num_pages = get_num_page_tourn(entrants_limit, game_id, year_start, year_end, page)
        logger.debug(f"tournaments page = {tournaments}, page = {page}")
        num_request += 1

        #checks if tournament list is empty
        if tournaments != None:
            #creates previous_tournament list
            for current in current_tournament:
                previous_tournament.append(current)
            current_tournament.clear()

            #loops through all tournaments in a given timeframe and prints sets and standings to a file
            for tournament in tournaments:
                logger.info(f"start date: {int(tournament['startAt'])}, continue: {continue_date}")
                #prevents duplicates
                if tournament["tournamentId"] not in previous_tournament:
                    with open("tournaments" + file_year + ".txt", 'a', encoding="utf-8") as tournament_file:
                        sys.stdout = tournament_file
                        if tournament[online] == False and ("singles" in tournament['eventName'].lower()):
                            print(f"tournament name: {tournament['tournamentName']}")
                            event_id = tournament[ult_id]
                            events(smash,event_id, tournament)
                            logger.info(f"tournament = {tournament}\n\n\n")
                            continue_date = int(tournament['startAt'])
                            current_tournament.append(tournament["tournamentId"])
            previous_tournament.clear()
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


tournament(smash)
sys.stdout = orgnl_stdout
print("data extraction complete")

