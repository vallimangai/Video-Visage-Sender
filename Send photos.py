import face_recognition
import cv2
import numpy as np
import pymongo
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep


chrome_options = Options()
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument('--user-data-dir=C:/Temp/ChromeProfile')
    #chrome_options.add_argument("user-data-dir=C:\\Users\\ADIL\\AppData\\Local\\Google\\Chrome\\UserData")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://web.whatsapp.com/')
driver.implicitly_wait(300)
client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
print(client)


# Get a reference to webcam #0 (the default one)
cap = cv2.VideoCapture('video1.mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")

# Read until video is completed





# Create arrays of known face encodings and their names
mydb=client['Faces']
known_face_encodings = []
known_face_names = []
information=mydb.faces
for record in information.find({}):
    known_face_names.append(record['name'])
    known_face_encodings.append(np.fromiter(record['face_encoding'],dtype=np.float64))

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
fi=0
while (cap.isOpened()):
    # Grab a single frame of video
    ret, frame = cap.read()
    fi=fi+1
    if(fi%3==0):
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame
        numbers=[]
        cv2.imwrite('my_video_frame.png', frame)
        for i in face_names:
            numbers.append(information.find_one({'name':i})['number'])
        if len(numbers)>0:
            print("next ")
            for num in numbers:
                ele = driver.find_element(By.CSS_SELECTOR, "._13NKt")
                ele.send_keys(num)

                ele.send_keys(Keys.ENTER)
                sleep(2)

                ele1 = driver.find_element(By.XPATH, '//span[@data-testid="clip"]')
                ele1.click()
                sleep(2)

                ele3 = driver.find_elements(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"][@type="file"]')[0]

                print(ele3)

                ele3.send_keys("G:/videosends/my_video_frame.png")
                # ele4 = driver.find_element(By.XPATH,
                #                            "//body/div[@id='app']/div[1]/div[1]/div[2]/div[2]/span[1]/div[1]/span[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/p[1]")
                # ele4.send_keys("Automatically sent....")

                send_arg = '//span[@data-testid="send"]'
                send = driver.find_element(By.XPATH, send_arg)
                send.click()


        # Display the results
        # for (top, right, bottom, left), name in zip(face_locations, face_names):
        #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        #     top *= 4
        #     right *= 4
        #     bottom *= 4
        #     left *= 4
        #
        #     # Draw a box around the face
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        #
        #     # Draw a label with a name below the face
        #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #     font = cv2.FONT_HERSHEY_DUPLEX
        #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()