import sqlite3
from Factories.ConfigFactory import ConfigFactory
from Factories.SorteoFactory import SorteoFactory
from Factories.MigrationFactory import MigrationFactory

class Factories:
    def __init__(self):
        self.Connection = sqlite3.connect("euromillones.db")
        self.Sorteos = SorteoFactory(self)
        self.Migrations = MigrationFactory(self)
        self.Configs = ConfigFactory(self)
    
    def __del__(self):
        self.Connection.close()

    def getConnection(self): return self.Connection

        