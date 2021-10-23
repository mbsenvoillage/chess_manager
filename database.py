from tinydb import TinyDB, Query, table, where

db = TinyDB('db.json')

players = db.table('players')
tournaments = db.table('tournaments')

