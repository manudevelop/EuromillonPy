import requests
from datetime import datetime
from Factories.BaseFactory import BaseFactory
from Models.Sorteo import Sorteo
import Helpers.JsonHelper as JsonHelper

class SorteoFactory(BaseFactory):

    def __init__(self, factories):
        super().__init__(factories) 
        
    def __rowToSorteo(selft, row):
        sorteo = Sorteo()
        sorteo.id = row[0] 
        sorteo.fecha = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        sorteo.numero1 = row[2] 
        sorteo.numero2 = row[3] 
        sorteo.numero3 = row[4] 
        sorteo.numero4 = row[5] 
        sorteo.numero5 = row[6] 
        sorteo.estrella1 = row[7] 
        sorteo.estrella2 = row[8] 
        sorteo.bote = row[9] 
        sorteo.recaudacion = row[10] 
        sorteo.premios = row[11] 
        sorteo.millon = row[12]
        return sorteo 

    def GetAll(self, where = None):
        cursor = self.Connection.cursor()
        where = f'WHERE {where}' if where != None else ''
        instruccion = f'select * from sorteos {where} order by fecha desc'
        result = []
        for row in cursor.execute(instruccion):
            sorteo = self.__rowToSorteo(row)
            result.append(sorteo)
        return result
    
    def GetLast(self):
        cursor = self.Connection.cursor()
        instruccion = f'select * from sorteos where fecha = (select MAX(fecha) from sorteos)'
        for row in cursor.execute(instruccion):
            return self.__rowToSorteo(row)
    
    def Get(self, id):
        cursor = self.Connection.cursor()
        instruccion = f'select * from sorteos where id = {str(id)}'
        for row in cursor.execute(instruccion):
            return self.__rowToSorteo(row)

    def GetByFecha(self, fecha):
        cursor = self.Connection.cursor()
        instruccion = f'select * from sorteos where strftime(\'%Y-%m-%d\',fecha) = \'{datetime.strftime(fecha, "%Y-%m-%d")}\''
        for row in cursor.execute(instruccion):
            return self.__rowToSorteo(row)

    def Add(self, item, commit = True):
        cursor = self.Connection.cursor()
        instruccion = f'INSERT INTO sorteos (id, fecha, numero1, numero2, numero3, numero4, numero5, estrella1, estrella2, bote, recaudacion, premios, millon) \
                        VALUES ({str(item.id)}, \'{datetime.strftime(item.fecha, "%Y-%m-%d %H:%M:%S")}\', {str(item.numero1)}, {str(item.numero2)}, {str(item.numero3)}, {str(item.numero4)}, {str(item.numero5)}, {str(item.estrella1)}, {str(item.estrella2)}, {str(item.bote)}, {str(item.recaudacion)}, {str(item.premios)}, \'{item.millon}\')'
        cursor.execute(instruccion)
        if(commit):
            self.Connection.commit()
    
    def Update(self, item, commit = True):
        cursor = self.Connection.cursor()
        instruccion = f'UPDATE sorteos \
            SET fecha = \'{datetime.strftime(item.fecha, "%Y-%m-%d %H:%M:%S")}\' ,\
                numero1 = {str(item.numero1)},\
                numero2 = {str(item.numero2)}, \
                numero3 = {str(item.numero3)}, \
                numero4 = {str(item.numero4)}, \
                numero5 = {str(item.numero5)}, \
                estrella1 = {str(item.estrella1)}, \
                estrella2 = {str(item.estrella2)}, \
                bote = {str(item.bote)}, \
                recaudacion = {str(item.recaudacion)}, \
                premios = {str(item.premios)}, \
                millon = \'{item.millon}\' \
            WHERE id = {str(item.id)}'
        cursor.execute(instruccion)
        if(commit):
            self.Connection.commit()
    
    def Delete(self, id, commit = True):
        cursor = self.Connection.cursor()
        instruccion = f'DELETE sorteos WHERE id = {str(id)}'
        cursor.execute(instruccion)
        if(commit):
            self.Connection.commit()

    def Sync(self, desdeFecha = None, hastaFecha = None, commit = True):
        lastSorteo = self.GetLast()
        hastaFecha = datetime.now() if hastaFecha == None else hastaFecha
       
        if desdeFecha == None:
            topeFecha = datetime(2004,2,13) if lastSorteo == None else lastSorteo.fecha
        else:
            topeFecha = datetime(2004,2,13) if desdeFecha < datetime(2004,2,13) else desdeFecha

        desdeFecha = datetime(hastaFecha.year, 1, 1)

        if(desdeFecha < topeFecha):
            desdeFecha = topeFecha

        ultimo_id = 0 if lastSorteo == None else lastSorteo.id
        while hastaFecha > topeFecha:
            api_url = "https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=EMIL&celebrados=true&fechaInicioInclusiva="+desdeFecha.strftime('%Y%m%d')+"&fechaFinInclusiva="+hastaFecha.strftime('%Y%m%d')
            response = requests.get(api_url)

            if JsonHelper.IsJson(response.content):
                resultJson = response.json()
                for item in resultJson:
                    combinacion = item['combinacion'].split('-')
                    
                    sorteo = Sorteo()
                    sorteo.id = int(item['id_sorteo'])
                    sorteo.numero1 = int(combinacion[0].strip())
                    sorteo.numero2 = int(combinacion[1].strip())
                    sorteo.numero3 = int(combinacion[2].strip())
                    sorteo.numero4 = int(combinacion[3].strip())
                    sorteo.numero5 = int(combinacion[4].strip())
                    sorteo.estrella1 = int(combinacion[5].strip())
                    sorteo.estrella2 = int(combinacion[6].strip())
                    sorteo.fecha = datetime.strptime(item['fecha_sorteo'], "%Y-%m-%d %H:%M:%S")
                    sorteo.premios = int(item['premios'])
                    sorteo.recaudacion = 0 if item['recaudacion'] == None else int(item['recaudacion'])
                    sorteo.bote = int(item['premio_bote'])
                    sorteo.millon = '' if item['millon'] == None else item['millon']['combinacion']
                    
                    if ultimo_id != sorteo.id :
                        self.Add(sorteo)

                    ultimo_id = sorteo.id

            hastaFecha = desdeFecha
            desdeFecha = desdeFecha.replace(year=desdeFecha.year - 1)

        lastSyncConfig = self.Factories.Configs.GetValue("LastSyncDate")
        if lastSyncConfig == None:
            self.Factories.Configs.Add('LastSyncDate', datetime.now())
        else:
            self.Factories.Configs.Update('LastSyncDate', datetime.now())

        if(commit):
            self.Connection.commit()

    def Check(self, numeros, estrellas, fecha = None):
        result = {}
        result['numeros'] = []
        result['estrellas'] = []
        result['premiado'] = False

        sorteo = self.GetLast() if fecha == None else self.GetByFecha(fecha)
        for numero in sorteo.numeros():
            if numero in numeros: result['numeros'].append(numero)
        
        for estrella in sorteo.estrellas():
            if estrella in estrellas : result['estrellas'].append(estrella)

        result['premiado'] = (len(result['numeros']) + len(result['estrellas'])) > 2
        return result