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
def get_image_urls():
    try:
        # Read the CSV file using pandas
        # Assuming your URLs are in the first column (index 0)
        # and your CSV might or might not have a header.
        # If it HAS a header, and the column name is, for example, 'url_column':
        # df = pd.read_csv(IMAGE_URLS_FILE)
        # urls = df['url_column'].dropna().tolist()

        # If it has NO header, and URLs are in the first column:
        # df = pd.read_csv(IMAGE_URLS_FILE, header=None)
        # urls = df[0].dropna().tolist()

        # A more robust way, trying to guess if there's a header for the first column:
        df = pd.read_csv(IMAGE_URLS_FILE, header=None) # Read without assuming header first
        
        # Check if the first row, first column looks like a URL (basic check)
        # If your CSV definitely has a header row, e.g. the first row is "image_url_header",
        # then use: df = pd.read_csv(IMAGE_URLS_FILE)
        # And then:  urls = df["image_url_header"].dropna().astype(str).tolist()

        # For now, let's assume the most common cases:
        # Case 1: CSV has a header, and the URL column is named (e.g., 'url', 'image_url')
        # Case 2: CSV has no header, URLs are in the first column.

        try:
            # Try reading with header first
            df_with_header = pd.read_csv(IMAGE_URLS_FILE)
            # Attempt to find a column that likely contains URLs (simple check for 'http')
            url_column = None
            for col in df_with_header.columns:
                if df_with_header[col].astype(str).str.contains('http', case=False).any():
                    url_column = col
                    break
            
            if url_column:
                urls = df_with_header[url_column].dropna().astype(str).tolist()
                st.info(f"Reading URLs from column '{url_column}' with header.")
            else: # Fallback to no header, first column
                df_no_header = pd.read_csv(IMAGE_URLS_FILE, header=None)
                urls = df_no_header[0].dropna().astype(str).tolist()
                st.info("Reading URLs from the first column, assuming no header.")

        except Exception as e_pandas:
            st.error(f"Pandas error reading CSV: {e_pandas}. Trying basic read of first column.")
            # Fallback to a very simple read if pandas has complex issues (less likely for this problem)
            df_no_header = pd.read_csv(IMAGE_URLS_FILE, header=None)
            urls = df_no_header[0].dropna().astype(str).tolist()


        # Clean up any leading/trailing whitespace from URLs
        urls = [str(url).strip() for url in urls if str(url).strip().startswith('http')]
        
        if not urls:
            st.error(f"No valid URLs found in {IMAGE_URLS_FILE} after parsing.")
        return urls

    except FileNotFoundError:
        st.error(f"Error: The file {IMAGE_URLS_FILE} was not found. Make sure it's in your GitHub repository root.")
        return []
    except pd.errors.EmptyDataError:
        st.error(f"Error: The file {IMAGE_URLS_FILE} is empty.")
        return []
    except Exception as e:
        st.error(f"An error occurred while reading image URLs: {e}")
        return []

st.title("Random Image Collection")
count = st.slider("How many images to show?", 1, 10, 5)

if st.button("Show Random Images"):
    urls = get_image_urls()
    if not urls:
        st.warning("No image URLs available to display.")
    else:
        if len(urls) < count:
            st.warning(f"Not enough images ({len(urls)}) to display {count}. Displaying all available.")
            chosen_urls = urls
        else:
            chosen_urls = random.sample(urls, count)

        # Dynamically adjust columns based on how many images are actually chosen
        cols = st.columns(len(chosen_urls))
        for i, img_url in enumerate(chosen_urls):
            col = cols[i] # Assign to the correct column
            if not isinstance(img_url, str) or not img_url.startswith('http'):
                col.error(f"Invalid URL format: {img_url}")
                continue
            try:
                response = requests.get(img_url)
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                img = Image.open(BytesIO(response.content))
                # Extract filename from URL for caption (basic)
                caption = os.path.basename(img_url.split('?')[0])
                col.image(img, caption=caption, use_column_width=True)
            except requests.exceptions.MissingSchema:
                col.error(f"Error: Invalid URL (Missing schema http/https): {img_url.split('/')[-1]}")
            except requests.exceptions.ConnectionError:
                col.error(f"Error: Could not connect to: {img_url.split('/')[-1]}")
            except requests.exceptions.RequestException as e:
                col.error(f"Error fetching: {img_url.split('/')[-1]}\n{type(e).__name__}")
            except Exception as e:
                col.error(f"Error opening: {img_url.split('/')[-1]}\n{type(e).__name__}")
