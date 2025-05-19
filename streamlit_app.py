import random
from PIL import Image
import streamlit as st
import requests # To fetch images from URLs
from io import BytesIO # To handle image data in memory
import pandas as pd # Import pandas
import os # To help with caption

# OPTION 1: Store URLs in a file within your GitHub repo (e.g., image_urls.txt)
# Make sure this file is in your GitHub repository
IMAGE_URLS_FILE = 'image_urls.csv'

# OPTION 2: Or, if the list isn't too massive, embed it directly (less scalable)
# IMAGE_URLS = [
#     "https://your-bucket-name.s3.your-region.amazonaws.com/image1.jpg",
#     "https://your-bucket-name.s3.your-region.amazonaws.com/image2.png",
#     # ... add all 10,000 URLs here (can be cumbersome)
# ]

@st.cache_data
def get_image_urls():
    # If using a file:
    try:
        with open(IMAGE_URLS_FILE, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        return urls
    except FileNotFoundError:
        st.error(f"{IMAGE_URLS_FILE} not found. Please create it and add your image URLs.")
        return []
    # If using an embedded list:
    # return IMAGE_URLS

st.title("Random Image Collection")
count = st.slider("How many images to show?", 1, 10, 5)

if st.button("Show Random Images"):
    urls = get_image_urls()
    if not urls:
        st.warning("No image URLs found.")
    else:
        if len(urls) < count:
            st.warning(f"Not enough images available to display {count}. Displaying all {len(urls)}.")
            chosen_urls = urls
        else:
            chosen_urls = random.sample(urls, count)

        cols = st.columns(len(chosen_urls))
        for col, img_url in zip(cols, chosen_urls):
            try:
                response = requests.get(img_url)
                response.raise_for_status() # Raise an exception for HTTP errors
                img = Image.open(BytesIO(response.content))
                # Extract filename from URL for caption
                caption = img_url.split('/')[-1].split('?')[0] # Basic way to get filename
                col.image(img, caption=caption, use_column_width=True)
            except requests.exceptions.RequestException as e:
                col.error(f"Error fetching: {img_url.split('/')[-1]}\n{e}")
            except Exception as e:
                col.error(f"Error opening: {img_url.split('/')[-1]}\n{e}")
