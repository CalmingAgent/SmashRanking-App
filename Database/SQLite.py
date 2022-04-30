from lib2to3.pytree import convert
import sqlite3
import string
import logging

class SQLite:
    test = False
    debuging = True

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
    def open_DB(self)-> sqlite3.Cursor:
        #opens a connection to DB and if it is testing use RAM instead of name
        if self.test == False:
            self.conn = sqlite3.connect(self.conn_name)
        else:
            self.conn = sqlite3.connect(":memory:")
        
        self.cur = self.conn.cursor()
        return self.conn.cursor()

    def find_value(self,primary_key,key_name:string, column_name:string, table_name):
        select_query = "SELECT " + column_name + " FROM " + table_name + " WHERE " + key_name + "=?"
        self.cur.execute(select_query, (primary_key,))
        select_value = self.cur.fetchone()
        self.conn.close()
        return select_value       
       

    def update_column(self,primary_key,key_name:string, column_name:string, table_name, updated_value:string):
        update_query = "UPDATE "+ table_name + " SET " + column_name + " = ? WHERE " + key_name + " = ?"
        self.cur.execute(update_query, (updated_value,primary_key))
        self.conn.commit()
        print (self.find_value(primary_key, key_name, column_name, table_name))
        self.conn.close()

    def insert_player_default(self, table_name, primary_key):
        key_if_exist= self.find_value(primary_key, self.primary_key_name, "*", table_name)
        if key_if_exist != None:
            insert_query = "INSERT INTO "+ table_name + "VALUES(?,?,?,?,?)"
            self.cur.execute(insert_query,(primary_key,self.default_wins, self.default_losses, self.default_ranking, self.default_tourney_placings))
            self.conn.commit()
        else:
            #log that it was not inserted and exists already
            pass

    def insert_player_custom(self, table_name, key_name,primary_key, wins_column:string, losses_column:string, ranking_column:string, tourney_placing_column:string):
        pass

    def convert_placings(self, db_tourney: string, tourney_placings:list =None):
        convert_placings =""
        if tourney_placings ==None:
            return db_tourney.split()
        else:
            return convert_placings.join(tourney_placings)

    



    
    

conn = SQLite("DB")
cur =conn.open_DB()
#conn.create_table("player", "win", "lose")
cur.execute('''CREATE TABLE IF NOT EXISTS Players (
    DNA STRING PRIMARY KEY, 
    wins REAL, 
    loses REAL,
    ranking REAL,
    tourney_placings STRING)''')

conn.insert_player_default("Players", "hello")
cur=conn.open_DB()
conn.update_column("hello","DNA", "wins","Players","72")

