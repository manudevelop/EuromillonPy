from Factories.BaseFactory import BaseFactory
from Models.Config import Config

class ConfigFactory(BaseFactory):

    def __init__(self, factories):
        super().__init__(factories)

    def GetAll(self):
        result = {}
        cursor = self.Connection.cursor()
        for row in cursor.execute(f'SELECT * FROM configs'):
            result[row[1]] = row[2]
        return result 

    def Get(self, tag):
        cursor = self.Connection.cursor()
        for row in cursor.execute(f'SELECT * FROM configs WHERE tag = \'{tag}\''):
            config = Config()
            config.id = row[0] 
            config.tag = row[1] 
            config.value = row[2] 
            return config 
    
    def GetValue(self, tag):
        config = self.Get(tag)
        return None if config == None else config.value

    def Add(self, tag, value, commit = True):
        cursor = self.Connection.cursor()
        instruccion = f'INSERT INTO configs (tag, value) values (\'{tag}\', \'{value}\')'
        cursor.execute(instruccion)
        if(commit):
            self.Connection.commit()

    def Update(self, tag, value, commit = True):
        cursor = self.Connection.cursor()
        instruccion = f'UPDATE configs SET value = \'{value}\' WHERE tag = \'{tag}\''
        cursor.execute(instruccion)
        if(commit):
            self.Connection.commit()