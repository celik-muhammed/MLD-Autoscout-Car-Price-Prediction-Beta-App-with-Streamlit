
import streamlit as st
import streamlit.components.v1 as components

from gtts import gTTS
import pyttsx3
import time

import pandas as pd
import numpy as np

# st.title("Car Price Prediction")
# st.header('This is a header')
# st.subheader('Car Price Prediction')
# st.text('This is some text.')
# st.write('Hello, *World!* :sunglasses:')
st.markdown("<h2 style='text-align:center; color:floralWhite;'>Car Price Prediction</h2>", unsafe_allow_html=True)

# st.success('This is a success message!')
# st.info('This is a purely informational message')
# st.error('This is an error')

# st.help(range)

col1, col2, col3 = st.columns([1,8,1]) 

#Image
try:
    # Some Code
    #read local image
    from PIL import Image
#     img1 = Image.open("images.jpeg")

    #image url
    url = "https://storage.googleapis.com/kaggle-datasets-images/383055/741735/4e7acec211a711b2669d91a771c0b4ca/dataset-cover.jpg"
    
    with col2:
        st.image(url, caption="Predicting the Prices of Cars")
        
#     #image read with imageio
#     from imageio.v2 import imread
#     img2 = imread(url)
    
#     #image read with requests
#     from urllib.request import urlopen
#     from requests import get
#     from io import BytesIO
#     response = get(url)
#     image_bytes = BytesIO(response.content)
#     img3 = Image.open(image_bytes)
    
except:
    # Executed if error in the
    # try block   
    components.html('''
    <script>
        alert("Image Not Loading!");
    </script>
    ''')
    st.text("Image Not Loading!")
    
else:
    # execute if no exception 
    pass
        
finally:
    # Some code .....(always executed)   
    pass


# read Dataset
df = pd.read_csv("final_scout.csv") #.drop(columns='price')

with col2:
    if st.checkbox('Show dataframe'):
        st.write(df)

# Creating side bar 
st.sidebar.subheader("Select the features you want for price estimation")

input_make_model = st.sidebar.selectbox('Name of the Car Model:', df['make_model'].unique())
input_gearing_type = st.sidebar.radio('Name of the Gearing Type:', df['gearing_type'].unique())
input_hp_kW	 = st.sidebar.slider('Horse Power(kW)', df["hp_kw"].min(), df["hp_kw"].max(), float(df["hp_kw"].mode()[0]), 1.0)
input_km = st.sidebar.slider('Kilometer(km)', 0.0, df["km"].max(), float(df["km"].mode()[0]), 1.0)
input_age = st.sidebar.slider('Car Age', 0.0, df["age"].max(), float(df["age"].mode()[0]), 1.0)
input_gears = st.sidebar.slider('Gears', df["gears"].min(), df["gears"].max(), float(df["gears"].mode()[0]), 1.0)

import pickle
model = pickle.load(open("final_model_scout", "rb"))

data = {"make_model" : input_make_model,
        "gearing_type" : input_gearing_type,
        "age" : input_age,
        "hp_kw" : input_hp_kW,
        "km" : input_km,
        "gears" : input_gears}
input_data = pd.DataFrame(data, index=[0])  

with col2:
    if st.checkbox('Show Selected Values', value=True):
        st.write(input_data.convert_dtypes())
        
# assign
video_html = """
<iframe width="0" height="0" 
src="https://www.youtube-nocookie.com/embed/t3217H8JppI?rel=0&amp;autoplay=1&mute=0&start=2860&amp;end=2866&controls=0&showinfo=0" 
allow="autoplay;"></iframe>
 """
audio_html = """    
<audio controls autoplay style="display: none">
<source src="https://ssl.gstatic.com/dictionary/static/pronunciation/2022-03-02/audio/pr/predicting_en_gb_1.mp3" type="audio/mpeg">
</audio>
""" 
if st.button('Make Prediction'):   
    sound = st.empty()
    sound.markdown(video_html, unsafe_allow_html=True)
    
    prediction = model.predict(input_data)
    prediction_text = model.predict(input_data)[0].round(2)
        
    audio = gTTS(text=str(prediction_text), lang="en", slow=False)
    audio.save("example.mp3")
    
    time.sleep(3.2)  # wait for 2 seconds to finish the playing of the audio
    sound.empty()  # optionally delete the element afterwards    
    st.success(f'Your Car price is:&emsp;${prediction_text}')
    pyttsx3.speak(prediction_text) 
    st.audio("example.mp3")   
    
    
html_temp = """
<div style="background-color:tomato;padding:1.5px">
<h1 style="color:white;text-align:center;">Single Customer </h1>
</div><br>"""
st.sidebar.markdown(html_temp,unsafe_allow_html=True)
