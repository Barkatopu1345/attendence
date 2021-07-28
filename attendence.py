import cv2
import numpy as np
import face_recognition
import os
import time
import xlsxwriter
import csv
from datetime import datetime



 
path = 'img'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

now = datetime.now()
dtString = now.strftime('%H:%M:%S')
print("encoding starting time " + dtString)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def timeInterval(s1,s2):

    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    if tdelta>2:
        return True
    else: return False    


def markAttendance(name,result):
    with open('Book1.csv','r+',encoding='utf-8-sig',newline='') as f:
        myDataList = f.readlines()
        nameList = []
        time = []

        for line in myDataList:
            # print(line)
            entry = line.split(',')
            # if entry.startswith('\ufeff'):
            #     entry = entry.encode('utf8')[3:].decode('utf8')

            # print(entry[0])

            nameList.append(entry[0])
            time.append(entry[2])
            print(time)
        
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S') 
        result = str(result)+'\n' 

        if ("\ufeff "+name) not in nameList:

            f.write(f' {name},{dtString},{result} ')
            
            #f.writelines(f'{name},{dtString}')

            print('Name: '+ name + '\n' + 'Date: ' + dtString)
        elif  ("\ufeff "+name) in nameList:
            if  timeInterval(time in entry[2] ,now) == True:
                f.write(f' {name},{dtString},{result} ')
                print('Name: '+ name + '\n' + 'Date: ' + dtString)

        f.close() 
        
             
           
 
encodeListKnown = findEncodings(images)
now = datetime.now()
dtString = now.strftime('%H:%M:%S')
print('Encoding Complete' + dtString)
 
cap = cv2.VideoCapture(0)
 
while True:
    success, img = cap.read()
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis)

        print(faceDis[matchIndex])
        if(faceDis[matchIndex]<0.50):
            result = faceDis[matchIndex]*100
            result = 100 - float(result)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                show = 'Matching = ' + str(int(result)) + '%  ' +name 
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img, show,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),2)

                
                #time.sleep(2)
                markAttendance(name,result)
                
                # testing(name,result)
    cv2.imshow('Webcam',img)
    if cv2.waitKey(2) == 27:
        break