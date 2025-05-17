import os, random
from PIL import Image
import streamlit as st

# Point this to your images folder
IMAGE_FOLDER = 'D:\\black\\Downloads\\images'

@st.cache_data
def get_image_paths():
    exts = {'.jpg','.jpeg','.png','.gif','.bmp','.tiff'}
    return [os.path.join(IMAGE_FOLDER, f)
            for f in os.listdir(IMAGE_FOLDER)
            if os.path.splitext(f)[1].lower() in exts]

st.title("Random Image Collection")
count = st.slider("How many images to show?", 1, 10, 5)

if st.button("Show Random Images"):
    paths = get_image_paths()
    chosen = random.sample(paths, count)
    cols = st.columns(count)
    for col, img_path in zip(cols, chosen):
        img = Image.open(img_path)
        col.image(img, caption=os.path.basename(img_path), use_column_width=True)
