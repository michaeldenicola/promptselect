import random
from PIL import Image
import streamlit as st
import requests # To fetch images from URLs
from io import BytesIO # To handle image data in memory
import pandas as pd # Import pandas
import os # To help with caption

# This should be 'image_urls.csv' as per your description
IMAGE_URLS_FILE = 'image_urls.csv'

@st.cache_data
   

st.title("Random Image Collection")
st.write("This app displays random images from an S3 bucket collection of over 10,000 images.")

# Add some explanation 
with st.expander("About this app"):
    st.write("""
    This app randomly selects and displays images from an AWS S3 bucket containing artwork.
    Use the slider below to select how many images you'd like to see at once, then click the button.
    
    Note: Some images in the collection may not load correctly due to URL formatting issues.
    The app automatically filters out problematic URLs.
    """)

count = st.slider("How many images to show?", 1, 10, 5)

if st.button("Show Random Images"):
    with st.spinner("Loading images..."):
        urls = get_image_urls()
        if not urls:
            st.warning("No image URLs available to display.")
        else:
            if len(urls) < count:
                st.warning(f"Not enough images ({len(urls)}) to display {count}. Displaying all available.")
                chosen_urls = urls
            else:
                chosen_urls = random.sample(urls, count)

            # Use st.columns instead of st.beta_columns (which is deprecated)
            cols = st.columns(min(len(chosen_urls), 3))  # Max 3 images per row for better layout
            
            for i, img_url in enumerate(chosen_urls):
                col = cols[i % len(cols)]  # Wrap around to new rows
                
                try:
                    response = requests.get(img_url, timeout=5)  # Add timeout to prevent hanging
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    img = Image.open(BytesIO(response.content))
                    
                    # Extract filename from URL for caption (basic)
                    caption = os.path.basename(img_url.split('?')[0])
                    
                    # Display the image
                    col.image(img, caption=caption, use_column_width=True)
                    
                except requests.exceptions.RequestException as e:
                    col.error(f"Error fetching image: {type(e).__name__}")
                    col.write(f"URL: {img_url.split('/')[-1]}")
                except Exception as e:
                    col.error(f"Error: {type(e).__name__}")
                    col.write(f"URL: {img_url.split('/')[-1]}")
