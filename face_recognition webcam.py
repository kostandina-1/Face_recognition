from tkinter import *
import sys
from tkinter import messagebox
import cv2
from xlwt import Workbook
import face_recognition as fr
import numpy as np
import tkinter
from PIL import ImageTk  # pip install pillow
from PIL import Image
class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1199x600+100+50")
        #Background image
        load = Image.open("faces/login.jpg")
        self.bg = ImageTk.PhotoImage(load)
        self.bg_img = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
    
        #Login Frame
        frame_login = Frame(self.root,bg= "white")
        frame_login.place(x=330, y=150, width=500, height=400)
        #Title and subtitle
        title =Label(frame_login, text= "Student recognition", font=("Impact", 30, "bold"), fg="indianred", bg="white").place(x=80, y=30)
        subtitle =Label(frame_login, text= "Fakulteti i Ekonomise", font=("Goudy old style", 15, "bold"), fg="darkslategray", bg="white").place(x=150, y=90)
        #Username
        lbl_user =Label(frame_login, text= "Emri i perdoruesit", font=("Goudy old style", 15, "bold"), fg="darkslategrey", bg="white").place(x=90, y=140)
        self.username =Entry(frame_login,  font=("Goudy old style", 15, "bold"), bg="#E7E6E6")
        self.username.place(x=90, y=170, width=320, height=35)
        #Password
        lbl_password =Label(frame_login, text= "Fjalkalimi", font=("Goudy old style", 15, "bold"), fg="darkslategrey", bg="white").place(x=90, y=210)
        self.password =Entry(frame_login,  font=("Goudy old style", 15, "bold"), bg="#E7E6E6")
        self.password.place(x=90, y=240, width=320, height=35)
        #Button
        forget=Button(Label(frame_login, text= "Harruat Fjalkalimin?",bd=0,cursor="hand2", font=("Goudy old style", 12), fg="orangered", bg="white").place(x=90, y=280))
        submit=Button(frame_login, cursor="hand2", command= self.check_function, text= "Kyçu",bd=0, font=("Goudy old style", 15), bg="indianred", fg="white").place(x=60, y=320, width=180, height=40)
        mbyll=Button(frame_login,cursor="hand2",command=sys.exit, text="Dil",bd=0,font=("Goudy old style", 15), bg="indianred", fg="white").place(x=250, y=320, width=180, height=40)
    def check_function(self):
        if self.username.get()=="" or self.password.get()=="":
           messagebox.showerror("Error", "Kerkohen te plotesohen te gjitha fushat!", parent=self.root)
        elif self.username.get()!="Admin" or self.password.get()!="12345":
            messagebox.showerror("Error", "Fjalkalimi ose Passwordi nuk jane te sakte!", parent=self.root)
        else:
            #where face_recognition beginns
            video_capture = cv2.VideoCapture(0)
            kostandina_image = fr.load_image_file( "faces\kostandina.jpg")
            kostandina_face_encoding = fr.face_encodings(kostandina_image)[0]
            known_face_encondings = [kostandina_face_encoding]
            known_face_names = ["kostandina Qirjazi"]
            H_image = fr.load_image_file("faces\H.jpeg")
            H_face_encoding = fr.face_encodings(H_image)[0]
            known_face_encondings = [H_face_encoding]
            known_face_names=["Harlindis"]
            Oliverta_image = fr.load_image_file( "faces\Oliverta.jpeg")
            Oliverta_face_encoding = fr.face_encodings(Oliverta_image)[0]
            known_face_encondings = [Oliverta_face_encoding]
            known_face_names = ["Oliverta "]
            known_face_encondings=[kostandina_face_encoding,H_face_encoding,Oliverta_face_encoding,R_face_encoding,B_face_encoding]
            known_face_names=["Kostandina","Oliverta ","Harlindis "]
            face_locations=[]
            face_encoding=[]
            face_names=[]
            process_this_frame=True

            while True:
                # Grab a single frame of video
                ret, frame = video_capture.read()
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]
                # Only process every other frame of video to save time
                if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                   face_locations = fr.face_locations(rgb_small_frame)
                   face_encodings = fr.face_encodings(rgb_small_frame, face_locations)
                   face_names = []
                   for face_encoding in face_encodings:

                # See if the face is a match for the known face(s)
                    matches = fr.compare_faces(known_face_encondings, face_encoding)
                    name = "IDENTIFYING"

                # use the known face with the smallest distance to the new face
                    face_distances = fr.face_distance(known_face_encondings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    face_names.append(name)
                process_this_frame = not process_this_frame
                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face,
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                #Writes to spreadsheet and GUI
        
                # Display the resulting image
                cv2.imshow('Video', frame)
   
                if cv2.waitKey(1) & 0xFF == ord('a'):
                    break
                    
            # Release handle to the webcam, Closes webcam
            video_capture.release()
            cv2.destroyAllWindows()
            print(known_face_names[best_match_index])    #it works , when i pressed a if it had found a name it would print the name in my case "KO" when the face was undetected it printet "finding face"
            list1=[2.34, 4.346, 4.234]
            wb= Workbook()
            sheet1=wb.add_sheet('listprezenca')
            sheet1.write(0,0,known_face_names[best_match_index])
            wb.save('listprezenca.xls')
            
            
root= Tk()
obj = Login(root)
root.mainloop()
quit()


