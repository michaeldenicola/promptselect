import streamlit as st
import random
import pandas as pd

# Configuration
IMAGE_URLS_FILE = 'image_urls.csv'

# 1. Custom CSS for Fixed-Width Masonry
st.markdown("""
<style>
.image-grid {
    /* column-width is the key: it keeps items at ~300px and adds columns as needed */
    column-width: 300px; 
    column-gap: 15px;
    width: 100%;
    max-width: 1200px; /* Optional: centers the gallery on ultra-wide screens */
    margin: 0 auto;
}

.image-item {
    display: inline-block; /* Required for column-width to work correctly */
    width: 100%;
    break-inside: avoid;
    margin-bottom: 15px;
}

.image-item img {
    width: 100%;
    height: auto; /* Maintains native aspect ratio */
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
    display: block;
}

.image-item img:hover {
    transform: scale(1.03);
}

/* Adjustments for smaller screens */
@media (max-width: 600px) {
    .image-grid {
        column-width: 100%; /* Spans full width on mobile */
    }
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_image_urls():
    try:
        df = pd.read_csv(IMAGE_URLS_FILE, header=None)
        return df[0].tolist()
    except Exception as e:
        st.error(f"Error loading {IMAGE_URLS_FILE}: {e}")
        return []

st.title("🎨 Random Image Collection")
count = st.slider("How many images to show?", 1, 30, 10)

if st.button("Show Random Images"):
    urls = get_image_urls()
    
    if not urls:
        st.warning("No image URLs found in the CSV.")
    else:
        num_to_sample = min(len(urls), count)
        chosen_urls = random.sample(urls, num_to_sample)
        
        # 2. Build the HTML Grid
        html_content = '<div class="image-grid">'
        for url in chosen_urls:
            html_content += f'<div class="image-item"><img src="{url}" alt="Random Image"></div>'
        html_content += '</div>'
        
        # 3. Render the grid
        st.markdown(html_content, unsafe_allow_html=True)
