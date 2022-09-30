
import streamlit as st
import streamlit_nested_layout
import streamlit.components.v1 as components

import pandas as pd
import numpy as np
import pickle

from requests import get
from io import BytesIO
from PIL import Image
from gtts import gTTS
import pyttsx3
import time

# st.title("Car Price Prediction")
# st.header('This is a header')
# st.subheader('Car Price Prediction')
# st.text('This is some text.')
# st.write('Hello, *World!* :sunglasses:')
# st.success('This is a success message!')
# st.info('This is a purely informational message')
# st.error('This is an error')
# st.help(range)

# read Dataset
df = pd.read_csv("final_scout.csv") #.drop(columns='price')

model = pickle.load(open("final_model_scout", "rb"))

st.markdown("<h2 style='text-align:center; color:floralWhite;'>Car Price Prediction</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,8,1]) 
#Image
try:
    # Some Code
    #read local image
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
    st.text("Image Not Loading!")
    components.html('''
    <script>
        alert("Image Not Loading!");
    </script>
    ''')
    
else:
    # execute if no exception 
    pass
        
finally:
    # Some code .....(always executed)   
    pass

with col2:
    # Show dataframe
    if st.checkbox('Show dataframe'):
        st.write(df)


def user_input_data():
    make_model = st.sidebar.selectbox('Name of the Car Model:', df['make_model'].unique())
    gearing_type = st.sidebar.radio('Name of the Gearing Type:', df['gearing_type'].unique())
    hp_kW = st.sidebar.slider('Horse Power(kW)', df["hp_kw"].min(), df["hp_kw"].max(), float(df["hp_kw"].mode()[0]), 1.0)
    km = st.sidebar.slider('Kilometer(km)', 0.0, df["km"].max(), float(df["km"].mode()[0]), 1.0)
    age = st.sidebar.slider('Car Age', 0.0, df["age"].max(), float(df["age"].mode()[0]), 1.0)
    gears = st.sidebar.slider('Gears', df["gears"].min(), df["gears"].max(), float(df["gears"].mode()[0]), 1.0)
    
    html_tomato = """
    <div style="background-color:tomato; padding:1.5px;">
    <h1 style="color:white; text-align:center;">Single Customer</h1>
    </div><br>"""
    st.sidebar.markdown(html_tomato, unsafe_allow_html=True)
    
    data = {
        "make_model" : make_model,
        "gearing_type" : gearing_type,
        "hp_kw" : hp_kW,
        "km" : km,
        "age" : age,
        "gears" : gears,
    }
    input_df = pd.DataFrame(data, index=[0])  

    return input_df

# Creating side bar 
st.sidebar.header("User Input parameter")
input_df = user_input_data()


# Predicting side bar 
col1, col2 = st.columns([7,3]) 

# Show input data
with col2:
    if st.checkbox('Show User Inputs', value=True):
        st.write(input_df.rename({0:'User_Input'}).T)
        
def show_pred_img(input_df):
    pred = input_df['make_model'].unique()[0]
    
    try:
        # Some Code        
        if 'Audi' in pred:
            url = "https://mediaservice.audi.com/media/live/50900/fly1400x601n1/8yaar/2021.png?imwidth=500"
        elif 'Opel' in pred:
            url = "https://www.opel.de/content/dam/opel/germany/fahrzeuge/corsa-f/bbc/DE_opel_corsa_elegance_my22C_960x540.jpg?imwidth=500"
        elif 'Renault' in pred:
            url = "https://www.renault.co.uk/agg/vn/unique/ONE_DACIA_PP_LARGE_DENSITY1/r_brandSite_carPicker_1.png?uri=https%3A%2F%2Fuk.co.rplug.renault.com%2Fproduct%2Fmodel%2FCL5%2Fclio%2Fc%2FA-ENS_0MDL2P1NIVEQPT6_"
        
        st.image(url, caption=f"model of car: {pred}")
    
    except:
        # Executed if error in the
        # try block   
        st.text("Image Not Loading!")  

with col1:
    if st.button('Make Prediction'):   
        sound = st.empty()
        # assign video or audio
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
        sound.markdown(video_html, unsafe_allow_html=True)

        prediction = model.predict(input_df)[0].round(2)        
        audio = gTTS(text=str(prediction), lang="en", slow=False)
        audio.save("example.mp3")

        time.sleep(3.2)  # wait for 2 seconds to finish the playing of the audio
        sound.empty()  # optionally delete the element afterwards  

        left, right = st.columns([5,6]) 
        left.success(f'Your Car price is:&emsp;${prediction}')
        right.markdown("<h6>", unsafe_allow_html=True)
        right.audio("example.mp3")  
        show_pred_img(input_df)
        pyttsx3.speak(prediction)  
