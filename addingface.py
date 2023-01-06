import numpy as np
import face_recognition
import pymongo

def add_face(path,name,ph):
    client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    print(client)
    mydb=client['Faces']

    information=mydb.faces

    image = face_recognition.load_image_file(path)
    face_encoding = face_recognition.face_encodings(image)[0]
    print(name)
    record={
        "name":name,
        'number':ph,
        "face_encoding":face_encoding.tolist(),
    }
    information.insert_one(record)
    return 1