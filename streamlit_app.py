import streamlit as st
import random
import requests
import pandas as pd
from io import BytesIO

# Configuration
IMAGE_URLS_FILE = 'image_urls.csv'

# 1. Custom CSS for Masonry-Style Layout with Native Ratios
st.markdown("""
<style>
.image-grid {
    column-count: 3;
    column-gap: 15px;
    padding: 10px;
}
.image-item {
    break-inside: avoid;
    margin-bottom: 15px;
}
.image-item img {
    width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
    display: block;
}
.image-item img:hover {
    transform: scale(1.02);
}

/* Responsive adjustments */
@media (max-width: 900px) {
    .image-grid {
        column-count: 2;
    }
}
@media (max-width: 600px) {
    .image-grid {
        column-count: 1;
    }
}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache expires after 5 minutes
def get_image_urls():
    try:
        # Assuming your CSV has a column named 'url' or is just a list
        df = pd.read_csv(IMAGE_URLS_FILE, header=None)
        return df[0].tolist()
    except Exception as e:
        st.error(f"Error loading {IMAGE_URLS_FILE}: {e}")
        return []

st.title("🎨 Random Image Collection")

# Add cache clear button in sidebar
with st.sidebar:
    if st.button("🔄 Refresh Image List"):
        st.cache_data.clear()
        st.success("Cache cleared! New images will load.")
        st.rerun()

count = st.slider("How many images to show?", 1, 100, 5)

if st.button("Show Random Images"):
    urls = get_image_urls()
    
    if not urls:
        st.warning("No image URLs found in the CSV.")
    else:
        # Sample images
        num_to_sample = min(len(urls), count)
        chosen_urls = random.sample(urls, num_to_sample)
        
        # 2. Build the HTML Masonry Grid
        html_content = '<div class="image-grid">'
        for url in chosen_urls:
            html_content += f'<div class="image-item"><img src="{url}" alt="Random Image"></div>'
        html_content += '</div>'
        
        # 3. Render the grid
        st.markdown(html_content, unsafe_allow_html=True)
