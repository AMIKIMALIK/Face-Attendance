import cv2
import pickle
import mysql.connector
import datetime


def predict():
	#get current date and time
	date= datetime.datetime.now()
	#get date in MM/DD/YY format
	name= str(date.strftime("%x"))
	#changing the date format from MM/DD/YY to DD_MM_YY using string sclicing so mysql can understand
	a= ""+name[3:5]+"_"+name[:2]+"_"+name[6:]
	#connect to mysql database
	mydb= mysql.connector.Connect( host="localhost", user="root", password="root", database="attendance")
	#create daily new column for attendance
	try:
		mycursor = mydb.cursor()
		mycursor.execute(f"ALTER TABLE cse_3rdyear_sectiona ADD {a} varchar(255);")
	except:
		pass

	def store(labels):
		mycursor = mydb.cursor()
		mycursor.execute(f"UPDATE cse_3rdyear_sectiona SET {a} = 'P' WHERE roll = {labels}")
		mydb.commit()
		# for x in labels:
		#
		#     mycursor.execute(f"UPDATE cse_3rdyear_sectiona SET {a} = 'P' WHERE roll = {x}")
		#     mydb.commit()
	# def get_name(roll):
	# 	mycursor= mydb.cursor()
	# 	gt=mycursor.execute(f"SELECT name FROM cse_3rdyear_sectiona WHERE roll={roll}")
	# 	return gt
	def get(labels):
		mycursor = mydb.cursor()
		mycursor.execute(f"SELECT name FROM cse_3rdyear_sectiona WHERE roll={labels}")
		myresult= mycursor.fetchall()
		mystr=str(myresult)
		mystr=mystr[3:-4]
		return mystr


	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read('trainer\\trainer.yml')
	cascadePath = "face.xml"
	faceCascade = cv2.CascadeClassifier(cascadePath)
	nbr_predicted, conf=0,0
	with open("trainer\\trained_faces.pkl",'rb') as f:
		face_dict = pickle.load(f)
	# face_dict=load_obj("trainer\\tr, ained_faces")

	cam = cv2.VideoCapture(0)
	i1=0
	i2=0
	# check=[]
	while True:
		ret, im = cam.read()
		gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
		for(x,y,w,h) in faces:
			nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
			print(round(100 - conf, 2))
			cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)

			label = face_dict[nbr_predicted]
			if(round(100 - conf, 2)>40):
				# check.append(label)
				store(label)
				name = get(label)

				# lab=get_name(label)
				cv2.putText(im,str(name),(x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)
				i1=i1+1
			else :
				cv2.putText(im,str("UNKNOWN"),(x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)



			# cv2.putText(im,"press esc to exit",(x-45,y-40),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,0),2)


		cv2.imshow('im',im)
		k = cv2.waitKey(100) & 0xff
		if k == 27:
			break

	cam.release()
	cv2.destroyAllWindows()
	if(i1>0):
		return ("Attendance Marked")
	if(i1==0):
		return ("No Attendance Marked")