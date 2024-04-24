# alle nötigen bibliotheken importieren
import cv2  # opencv für kamera handling & bildverarbeitung
import face_recognition  # Machine learning packet welches gesichter im bild sucht
import RPi.GPIO as GPIO # Raspberry Pi output pins
import time # Zeit
import pygame # modul zum  mp3 dateien abzuspielen


Relay_pin = 23 # GPIO pin 23 


# Funktionen für unterschiedliche Personen


def action_for_person1():
    print("Hallo Person 1")
    
    GPIO.output(Relay_pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(Relay_pin, GPIO.LOW)
    
    #pygame.mixer.music.load('ramiz.mp3')
    #pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy():  
        #pygame.time.Clock().tick(10)

def action_for_person2():
    print("Hallo Person 2")
    
    GPIO.output(Relay_pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(Relay_pin, GPIO.LOW)
    
    #pygame.mixer.music.load('ramiz.mp3')
    #pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy():  
        #pygame.time.Clock().tick(10)





GPIO.setwarnings(False) # Deaktiviert warnungen
GPIO.setmode(GPIO.BCM) # GPIO pin nummerierung auf BCM (unterschiedliche nummerierung falls anderer "modus"


GPIO.setup(Relay_pin, GPIO.OUT) # Realy_pin(GPIO 23) wird als output gesetzt
GPIO.output(Relay_pin, GPIO.LOW) # setzt ppin 23 auf aus (LOW)



# Person1
MY_PICTURE = face_recognition.load_image_file("person1.jpg") # bild wird geladen
MY_PICTURE_PROCESS = face_recognition.face_encodings(MY_PICTURE)[0] # bild in Daten verarbeiten

# Person2
PERSON1_PICTURE = face_recognition.load_image_file("person2.jpg")
PERSON1_PICTURE_PROCESS = face_recognition.face_encodings(PERSON1_PICTURE)[0]



# liste von daten der Bilder, Liste der Namen der jeweiligen "Daten"
PICTURE_PROCESS_DATA = [MY_PICTURE_PROCESS, PERSON1_PICTURE_PROCESS]
MY_NAMES = ["Person1", "Person2"]



# Kamera aktivieren mit der jeweiligen grösse des Bildschirms
cap = cv2.VideoCapture(0)
cap.set(3,640) #Kameraauflösung
cap.set(4,480)

C = 0 # Frame zähler

while True:
    
    # Bilder von Kamera werden in while schleife ausgelesen
    ret, frame = cap.read()
    
    if C % 10 == 0: # alle 10 Frames wird diese schleifen initialisiert
        
        
        
        POS_FACE = face_recognition.face_locations(frame) # sucht ein gesicht im kamerabild
        POS_FACE_PROCESS = face_recognition.face_encodings(frame, POS_FACE) # verarbeitet das gesicht im live feed in daten
    

    # BELOW CODE LINES USED TO START MATCHING PROCESS whether the current FACE matches with the loaded image data or not
    
        for (top, right, bottom, left), face_encoding in zip(POS_FACE, POS_FACE_PROCESS): # gesichtserkennung über Face Recognition bibliothek

            REC_PROCESS = face_recognition.compare_faces(PICTURE_PROCESS_DATA, face_encoding)

            ID = "keine Registrierte Person erkannt"

        # IF statement u zu prüfen ob gesicht erkannt wird
            if True in REC_PROCESS:
                
            
            # gefundenes gesicht vergleichen
                USER_FND = REC_PROCESS.index(True)
                ID = MY_NAMES[USER_FND]
                print(f"Registrierte Person {ID} wurde erkannt") # falls nicht übereinstimmt
                
                if ID == "Ramiz": # jeweilige benutzer
                    action_for_ramiz()
                elif ID == "Nick":
                    action_for_nick()
                
            

        # projeziert rechteck & namen auf den live screen
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, ID, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
 
    
    # bildschirm zum live screen zeigen
        cv2.imshow('LIVE GEESICHTSERKENNUNG', frame)
    C = C+1 # zähler wird nach jedem bildframe +1 hinzugefügt
    if cv2.waitKey(1) & 0xFF == ord('q'): # abbrechen mit der taste "q"
        break

# close the application
cap.release()
cv2.destroyAllWindows()


