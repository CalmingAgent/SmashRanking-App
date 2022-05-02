from lib2to3.pytree import convert
import sqlite3
from sqlite3 import Error
import string
'''SQL object to create and edit DB, default constructor is the connection name; this is required. 
    The default columns and values wins,loses,ranking, tourney_placings, and the key name have already been created'''
class SQLite:
    test = True
    #Detailed information, typically of interest only when diagnosing problems
    debuging = True
    # Confirmation that things are working as expected.
    info = False
    #An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected. 
    #no need to have variable for this because Warning is the default value of logger
    
    #Due to a more serious problem, the software has not been able to perform some function.
    log_error_testing= False
    #A serious error, indicating that the program itself may be unable to continue running.
    critical_error_testing = False

    def __init__(self, conn_name):
        self.cur = None
        self.conn = None
        self.conn_name = conn_name
        self.default_wins = 0
        self.default_losses = 0 
        self.default_ranking = 0 
        self.default_tourney_placings = ""
        self.primary_key_name = "DNA"

    '''opens the SQLite DB object
        Retuns the cursor object of the open database'''
    def open_DB(self)-> sqlite3.connect:
        try:
            conn = sqlite3.connect(self.conn_name)
        except Error as e:
            #error log here
            print(e)
    
        self.conn = conn
        self.cur = self.conn.cursor()
        return conn        

    '''Finds a value and returns the row-column value, only one column at a time'''
    def find_value(self,primary_key,key_name:string, column_name:string, table_name):
        with self.open_DB():
            select_query = "SELECT " + column_name + " FROM " + table_name + " WHERE " + key_name + "=?"
            self.cur.execute(select_query, (primary_key,))
            select_value = self.cur.fetchone()
            return select_value       
       
    '''updates a value in a column'''
    def update_column(self,primary_key,key_name:string, column_name:string, table_name, updated_value:string):
        with self.open_DB():
            update_query = "UPDATE "+ table_name + " SET " + column_name + " = ? WHERE " + key_name + " = ?"
            self.cur.execute(update_query, (updated_value,primary_key))
            self.conn.commit()
            #info log here for to check if correct information was committed.            
    
    '''insert new entry into database'''
    def insert_player_default(self, table_name, primary_key):
        with self.open_DB():
            key_if_exist= self.find_value(primary_key, self.primary_key_name, "*", table_name)
            if key_if_exist == None:
                insert_query = "INSERT INTO "+ table_name + " VALUES (?,?,?,?,?)"
                self.cur.execute(insert_query,(primary_key,self.default_wins, self.default_losses, self.default_ranking, self.default_tourney_placings))
                self.conn.commit()
                #info log here for to check if correct information was committed.
            else:
                #info log that it was not inserted and exists already
                pass
    
    '''solely for db to model, can't have list in sqlite'''            
    def convert_placings(self, db_tourney, tourney_placings:list =None):
        convert_placings =""
        
        if tourney_placings ==None:
            #convert single tuple string to list will need this a lot in sqlite
            for i in db_tourney:
                convert_placings = convert_placings + i
            #convert the string into list
            list_convert = convert_placings.split()
            #convert string list to int list
            list_convert = [int(i) for i in list_convert]
            return list_convert
        else:
            return convert_placings.join(tourney_placings)

    



    
    
#testing database
#conn=SQLite("DB")
# cur =conn.open_DB()
# cur.execute('''CREATE TABLE IF NOT EXISTS Players (
#     DNA STRING PRIMARY KEY, 
#     wins REAL, 
#     loses REAL,
#     ranking REAL,
#     tourney_placings STRING)''')


# #testing methods
# conn.insert_player_default("Players", "hello")
# conn.insert_player_default("Players", "boss")
# conn.update_column("hello","DNA", "wins","Players","72")
# conn.update_column("boss","DNA","tourney_placings", "Players","27 28 23 1 7 4")
# #self,primary_key,key_name:string, column_name:string, table_name
# db_tourney = SQLite.find_value(conn,"boss", "DNA", "tourney_placings", "players")
# placings = SQLite.convert_placings(conn,db_tourney)
# print(placings)
# for row in cur.execute("SELECT * FROM Players"):
#     print(row)

