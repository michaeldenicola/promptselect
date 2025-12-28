import streamlit as st
import random
import requests
import pandas as pd
from io import BytesIO

# Configuration
IMAGE_URLS_FILE = 'image_urls.csv'

# 1. Custom CSS for a Fixed Grid with Consistent Image Sizes
st.markdown("""
<style>
.image-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: center;
}
.image-grid img {
    width: 200px !important;
    height: 200px !important;
    min-width: 200px;
    min-height: 200px;
    max-width: 200px;
    max-height: 200px;
    object-fit: cover;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
    flex-shrink: 0;
}
.image-grid img:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_image_urls():
    try:
        # Assuming your CSV has a column named 'url' or is just a list
        df = pd.read_csv(IMAGE_URLS_FILE, header=None)
        return df[0].tolist()
    except Exception as e:
        st.error(f"Error loading {IMAGE_URLS_FILE}: {e}")
        return []

st.title("🎨 Random Image Collection")
count = st.slider("How many images to show?", 1, 20, 5)

if st.button("Show Random Images"):
    urls = get_image_urls()
    
    if not urls:
        st.warning("No image URLs found in the CSV.")
    else:
        # Sample images
        num_to_sample = min(len(urls), count)
        chosen_urls = random.sample(urls, num_to_sample)
        
        # 2. Build the HTML Grid
        html_content = '<div class="image-grid">'
        for url in chosen_urls:
            html_content += f'<img src="{url}" alt="Random Image">'
        html_content += '</div>'
        
        # 3. Render the grid
        st.markdown(html_content, unsafe_allow_html=True)
