from datetime import datetime
import telebot
import os
import sys
from Repositories.EuromillonRepository import EuromillonRepository
from pyzbar.pyzbar import decode
import cv2
import shutil

TELEGRAM_TOKEN = "TELEGRAM_TOKEN"
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start"])
def sendMessage(message):
    bot.send_message(message.chat.id, "Bienvenido al comprobador de loterias. De momento solo disponemos de comprobador de euromillones pero muy pronto agregarémos más sorteos. \n\nSolo tiene que mandar una imagen donde se vea el código QR de tu boleto.\n\nSuerte!!")
    pass

@bot.message_handler(content_types=['photo'])
def photo(message):
    print('Image receive')
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    path = f'./tmp/{message.chat.id}image.jpg'
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    qr_value = read_qr_code(path)
    barcode_value = read_bar_code(path)

    if(qr_value != ""):                               
        result = analizar_codigo_euromillon(qr_value)
        for r in result:
            if(r.Escrutinio != None):
                bot.send_message(message.chat.id, f'Enhorabuena! has conseguido {r.Escrutinio.premio} con este boleto')
            else:
                bot.send_message(message.chat.id, f'No hay premio en este boleto')
    elif(barcode_value != ""):
        pass
    else:
        bot.send_message(message.chat.id, "No se ha detectado código");   

    os.remove(path)

def analizar_codigo_euromillon(codigo):
    #A=1170707020839990081910606758924095;P=7;S=05719JUL22:1;W=0;.1=062327242526273248:0612;T=27610-0;RI=11[S=05719JUL22:1,FPT27910-FPT28035];
   
    fechaSorteo = ""
    numeros = []  
    estrellas = [] 

    for item in codigo.split(';'):
        if(item.startswith("S=")):
            item = item.replace("S=","")
            numSorteo = item[0:3]
            dia = item[3:5]
            mes = mes_to_int(item[5:8])
            anio = '20' + item[8:10]
            fechaSorteo = datetime(int(anio), int(mes), int(dia))
        elif(item.startswith(".1")):
            item = item.replace(".1=", "")
            juego = item.split(':')
            i = 0; j = 0
            while(len(juego[0])>i):
                numeros.append(int(juego[0][i : i + 2]))
                i = i + 2
            while(len(juego[1]) > j):
                estrellas.append(int(juego[1][j : j + 2]))
                j = j + 2

    return EuromillonRepository().Check(numeros, estrellas, fechaSorteo, fechaSorteo)
   
    print(numeros, estrellas, fechaSorteo)        

def mes_to_int(mes):
    if(mes == 'ENE'):
        return 1
    elif (mes == 'FEB'):
        return 2
    elif (mes == 'MAR'):
        return 3
    elif (mes == 'ABR'):
        return 4
    elif (mes == 'MAY'):
        return 5
    elif (mes == 'JUN'):
        return 6
    elif (mes == 'JUL'):
        return 7
    elif (mes == 'AGO'):
        return 8
    elif (mes == 'SEP'):
        return 9
    elif (mes == 'OCT'):
        return 10
    elif (mes == 'NOV'):
        return 11
    elif (mes == 'DIC'):
        return 12
  
def read_qr_code(filename):
    """Read an image and read the QR code.
    
    Args:
        filename (string): Path to file
    
    Returns:
        qr (string): Value from QR code
    """
    
    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return

def read_bar_code(filename):
    """Read an image and read the bar code.
    
    Args:
        filename (string): Path to file
    
    Returns:
        barcode (string): Value from bar code
    """
    
    try:
        img = cv2.imread(filename)
        detect = decode(img)
        # If not detected then print the message
        if not detect:
            print("Barcode Not Detected or your barcode is blank/corrupted!")
        else:
        
            # Traverse through all the detected barcodes in image
            for barcode in detect: 
            
                # Locate the barcode position in image
                (x, y, w, h) = barcode.rect
                
                # Put the rectangle in image using
                # cv2 to heighlight the barcode
                cv2.rectangle(img, (x-10, y-10),
                            (x + w+10, y + h+10),
                            (255, 0, 0), 2)
        return barcode.data
    except:
        return

def main():
    if(not os.path.isdir("./tmp")):
        os.mkdir("./tmp")

    bot.polling()

    if(os.path.isdir("./tmp")):
        shutil.rmtree("./tmp")

if __name__ == "__main__":
    main() 