import streamlit as st
import numpy as np
import face_recognition
import pymongo
from addingface import add_face

st.set_page_config(
    page_title="Video Visage Sender",
    page_icon=":)"
)

st.title('Photo Uploader')
a=0
def save_uploadedfile(uploadedfile):
    with open( "img.png", "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("File uploaded successfully👍"+uploadedfile.name)

with st.form("my_form"):
# File upload
    name=st.text_input(label="Name")
    print(name)
    ph = st.text_input(label="Phone")

    uploaded_file = st.file_uploader('Choose your image ', type=["png","jpg"])
    if uploaded_file is not None:
        # print(type(uploaded_file))
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}

        save_uploadedfile(uploaded_file)
    sum=st.form_submit_button("Submit")
    if sum:
        a=add_face("img.png",name,ph)
if(a):
    st.success("Uploaded wait for a Photos")