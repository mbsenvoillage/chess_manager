from tinydb import TinyDB

db = TinyDB('db.json')

players = db.table('players')
tournaments = db.table('tournaments')
