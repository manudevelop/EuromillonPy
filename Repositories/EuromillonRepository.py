from Models.Escrutinio import Escrutinio
from Models.Sorteo import Sorteo
from Models.CompruebaSorteo import CompruebaSorteo
import Helpers.JsonHelper as JsonHelper
import requests
from datetime import datetime
from py_linq import Enumerable 


    
class EuromillonRepository :

    def __init__(self):
        self.BaseUrl = "https://www.loteriasyapuestas.es/servicios/"

    def GetAll(self, desdeFecha, hastaFecha):
        sorteos = []
        hastaFecha = datetime.now() if hastaFecha == None else hastaFecha
       
        if desdeFecha == None:
            topeFecha = datetime(2004,2,13)
        else:
            topeFecha = datetime(2004,2,13) if desdeFecha < datetime(2004,2,13) else desdeFecha

        desdeFecha = desdeFecha if desdeFecha != None else datetime(hastaFecha.year, 1, 1)

        if(desdeFecha < topeFecha):
            desdeFecha = topeFecha

        ultimo_id = 0
        while hastaFecha >= topeFecha:
            route = "buscadorSorteos?game_id=EMIL&celebrados=true&fechaInicioInclusiva="+desdeFecha.strftime('%Y%m%d')+"&fechaFinInclusiva="+hastaFecha.strftime('%Y%m%d')
            response = requests.get(self.BaseUrl + route)

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

                    for escrutinio in item['escrutinio']:
                        escru = Escrutinio()
                        escru.tipo = escrutinio['tipo']
                        escru.categoria = int(escrutinio['categoria'])
                        escru.premio = float(escrutinio['premio'].replace(',','.'))
                        escru.ganadores = int(escrutinio['ganadores'])
                        escru.ganadores_eu = int(escrutinio['ganadores_eu'])
                        sorteo.escrutinio.append(escru)

                    if ultimo_id != sorteo.id :
                        sorteos.append(sorteo)

                    ultimo_id = sorteo.id

            if(hastaFecha <= topeFecha):
                break

            hastaFecha = desdeFecha
            desdeFecha = desdeFecha.replace(year=desdeFecha.year - 1)
        
        return sorteos

    def Check(self, numeros, estrellas, desdeFecha, hastaFecha):
        compruebas = []
        sorteos = self.GetAll(desdeFecha, hastaFecha)
        for sorteo in sorteos:
            comprueba = CompruebaSorteo(sorteo)
            escrutinioEnumerable = Enumerable(sorteo.escrutinio)

            for numero in sorteo.numeros():
                if numero in numeros: comprueba.Numeros.append(numero)
            
            for estrella in sorteo.estrellas():
                if estrella in estrellas : comprueba.Estrellas.append(estrella)

            if(len(comprueba.Numeros) == 5 and len(comprueba.Estrellas) == 2):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 1)
            elif(len(comprueba.Numeros) == 5 and len(comprueba.Estrellas) == 1):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 2)
            elif(len(comprueba.Numeros) == 5 and len(comprueba.Estrellas) == 0):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 3)
            elif(len(comprueba.Numeros) == 4 and len(comprueba.Estrellas) == 2):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 4)
            elif(len(comprueba.Numeros) == 4 and len(comprueba.Estrellas) == 1):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 5)
            elif(len(comprueba.Numeros) == 3 and len(comprueba.Estrellas) == 2):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 6)
            elif(len(comprueba.Numeros) == 4 and len(comprueba.Estrellas) == 0):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 7)
            elif(len(comprueba.Numeros) == 2 and len(comprueba.Estrellas) == 2):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 8)
            elif(len(comprueba.Numeros) == 3 and len(comprueba.Estrellas) == 1):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 9)
            elif(len(comprueba.Numeros) == 3 and len(comprueba.Estrellas) == 0):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 10)
            elif(len(comprueba.Numeros) == 1 and len(comprueba.Estrellas) == 2):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 11)
            elif(len(comprueba.Numeros) == 2 and len(comprueba.Estrellas) == 1):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 12)
            elif(len(comprueba.Numeros) == 2 and len(comprueba.Estrellas) == 0):
                comprueba.Escrutinio = escrutinioEnumerable.first_or_default(lambda p:p.categoria == 13)
            
            compruebas.append(comprueba)


        return compruebas

