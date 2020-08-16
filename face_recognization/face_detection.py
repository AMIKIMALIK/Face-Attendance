import cv2
import sys
import os
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="attendance"
)

# cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier("face.xml")

def detect(var1, var2):
    # name = input("Enter Name:")
    var2=var2.lower()
    var2=var2.capitalize()
    name= var1
    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO cse_3rdyear_sectiona (name, roll) VALUES (%s, %s)"
        val = (var2, name)
        mycursor.execute(sql, val)
        mydb.commit()

    except:
        pass

    try:
        os.mkdir("malik")
    except:
        pass
    try:
        os.mkdir("malik"+"\\"+name)
    except:
        pass
    video_capture = cv2.VideoCapture(0)
    new_path = "malik"+"\\"+name
    i = 0
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            i=i+1
            cv2.imwrite(new_path+"\\"+name +'_'+ str(i) + ".jpg", gray[y:y+h,x:x+w])
            print("file_saved")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            print(i)
        # Display the resulting frame
        try:
            cv2.imshow('Video', frame)
        except:
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if i+1>50:
            break
    print(name1)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()