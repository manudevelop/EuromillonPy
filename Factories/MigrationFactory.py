from datetime import datetime
from Factories.BaseFactory import BaseFactory
from Models.Migration import Migration
from Models.Migration import migrations as Migrations
import Helpers.DbHelper as DbHelper

class MigrationFactory(BaseFactory):

    def __rowToMigration(selft, row):
        migration = Migration()
        migration.id = row[0] 
        migration.name = row[1] 
        migration.created_on = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        return migration 

    def __init__(self, factories):
        super().__init__(factories)

    def GetAll(self):
        result = []
        cursor = self.Connection.cursor()
        instruccion = f'SELECT * FROM migrations'
        for row in cursor.execute(instruccion):
            result.append(self.__rowToMigration(row))
        return result

    def GetLast(self):
        cursor = self.Connection.cursor()
        instruccion = f'SELECT * FROM migrations WHERE id = (SELECT MAX(id) FROM migrations)'
        for row in cursor.execute(instruccion):
            return self.__rowToMigration(row)

    def Get(self, name):
        cursor = self.Connection.cursor()
        instruccion = f'SELECT * FROM migrations WHERE name =\'{name}\''
        for row in cursor.execute(instruccion):
            return self.__rowToMigration(row)

    def Add(self, name, commit = True):
        cursor = self.Connection.cursor()
        instruccion = f'INSERT INTO migrations (name) VALUES (\'{name}\')'
        cursor.execute(instruccion)
        if(commit):
            self.Connection.commit()

    def Delete(self, name):
        cursor = self.Connection.cursor()
        instruccion = f'DELETE FROM migrations WHERE name =\'{name}\''
        cursor.execute(instruccion)

    def Upgrade(self, name = None, commit = True):
        cursor = self.Connection.cursor()
        lastMigration = None if not DbHelper.tableExists("migrations", self.Connection) else self.GetLast()
        if lastMigration == None:
            for migration in Migrations:
                for inst in migration.up():
                    cursor.execute(inst)
                self.Add(migration.name)
        else:
            ignore = True
            for migration in Migrations:
                if not ignore:  
                    for inst in migration.up():
                        cursor.execute(inst)
                    self.Add(migration.name)
                
                if lastMigration.name == migration.name:
                    ignore = False
                
                if migration.name == name:
                    break
        if(commit):
            self.Connection.commit()

    def Downgrade(self, name = None, commit = True):
        cursor = self.Connection.cursor()
        lastMigration = None if not DbHelper.tableExists("migrations", self.Connection) else self.GetLast()
        ignore = True
        i = len(Migrations) - 1
        while i >= 0:
            currentMigration = Migrations[i]
            if(currentMigration.name == name):
                break
            if currentMigration.name == lastMigration.name:
                ignore = False
            if not ignore:    
                for inst in currentMigration.down():
                    cursor.execute(inst)
                    self.Delete(currentMigration.name)
            i=i-1
        if(commit):
            self.Connection.commit()
