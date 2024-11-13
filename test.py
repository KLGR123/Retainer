from openai import OpenAI
import streamlit as st

OPENAI_API_KEY = st.secrets["openai_api_key"]

completion = OpenAI(api_key=OPENAI_API_KEY).images.generate(
    model="dall-e-3",
    prompt="Create an image: A complete historical pirate ship with a fully visible, weathered wooden hull and tattered sails. Show the ship in two views: frontal on the left, side on the right, with visible cannons along the side, a worn Jolly Roger flag, and ropes from tall masts. Ensure the entire ship body is within the frame without cropping any part. The ship can be relatively small in scale, ensuring all parts are included. Flat vector style, clean lines, solid colors, transparent background, and suitable for game assets.",
    size="1792x1024",
    quality="standard",
    n=1,
)
image_url = completion.data[0].url

import requests
response = requests.get(image_url)
if response.status_code == 200:
    with open("image.png", "wb") as f:
        f.write(response.content)