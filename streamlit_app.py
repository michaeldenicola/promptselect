"""
Niji Library Browser - Enhanced Streamlit App
==============================================
A powerful image browser for your Midjourney/Nijijourney library.

Features:
- Random image with filters (source, model, date, prompt)
- Prompt search
- Statistics dashboard
- Metadata display
- Gallery view

Setup:
1. Run `python export_manifest.py` to upload manifest to S3
2. Deploy this app to Streamlit Cloud
3. Set secrets in Streamlit Cloud dashboard

Secrets required (in Streamlit Cloud):
    AWS_BUCKET = "inklungsbucket"
    AWS_REGION = "us-east-2"
    MANIFEST_URL = "https://inklungsbucket.s3.us-east-2.amazonaws.com/manifest/manifest.json.gz"
"""

import streamlit as st
import pandas as pd
import json
import gzip
import random
from datetime import datetime, timedelta
from io import BytesIO
from typing import Optional, List, Dict
import requests

# ============== CONFIG ============== #
# These can be overridden by Streamlit secrets
DEFAULT_BUCKET = "inklungsbucket"
DEFAULT_REGION = "us-east-2"
DEFAULT_MANIFEST_URL = f"https://{DEFAULT_BUCKET}.s3.{DEFAULT_REGION}.amazonaws.com/manifest/manifest.json.gz"

# ============== PAGE CONFIG ============== #
st.set_page_config(
    page_title="Niji Library Browser",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== CUSTOM CSS ============== #
st.markdown("""
<style>
    .main-image {
        max-height: 70vh;
        width: auto;
        margin: 0 auto;
        display: block;
    }
    .metadata-box {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .stat-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .thumbnail-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ============== DATA LOADING ============== #
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_manifest() -> pd.DataFrame:
    """Load manifest from S3."""
    # Get URL from secrets or use default
    manifest_url = st.secrets.get("MANIFEST_URL", DEFAULT_MANIFEST_URL)
    
    try:
        response = requests.get(manifest_url, timeout=30)
        response.raise_for_status()
        
        # Decompress if gzipped
        if manifest_url.endswith('.gz'):
            data = gzip.decompress(response.content)
            manifest = json.loads(data.decode('utf-8'))
        else:
            manifest = response.json()
        
        # Convert to DataFrame
        df = pd.DataFrame(manifest['images'])
        
        # Parse dates
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            df['month'] = df['created_at'].dt.to_period('M').astype(str)
        
        return df
        
    except Exception as e:
        st.error(f"Failed to load manifest: {e}")
        return pd.DataFrame()


def filter_images(
    df: pd.DataFrame,
    source: Optional[str] = None,
    model: Optional[str] = None,
    prompt_search: Optional[str] = None,
    date_range: Optional[tuple] = None
) -> pd.DataFrame:
    """Apply filters to the image dataframe."""
    filtered = df.copy()
    
    if source and source != "All":
        filtered = filtered[filtered['source'] == source.lower()]
    
    if model and model != "All":
        filtered = filtered[filtered['model_version'] == model]
    
    if prompt_search:
        # Case-insensitive search in prompt
        mask = filtered['prompt'].fillna('').str.lower().str.contains(
            prompt_search.lower(), regex=False
        )
        filtered = filtered[mask]
    
    if date_range:
        start_date, end_date = date_range
        if start_date:
            filtered = filtered[filtered['created_at'] >= pd.Timestamp(start_date)]
        if end_date:
            filtered = filtered[filtered['created_at'] <= pd.Timestamp(end_date)]
    
    return filtered


# ============== PAGES ============== #
def page_random():
    """Random image viewer with filters."""
    st.title("🎲 Random Image")
    
    df = load_manifest()
    if df.empty:
        st.warning("No images loaded. Make sure the manifest is uploaded to S3.")
        return
    
    # Sidebar filters
    with st.sidebar:
        st.header("Filters")
        
        source_options = ["All"] + sorted(df['source'].dropna().unique().tolist())
        selected_source = st.selectbox("Source", source_options)
        
        model_options = ["All"] + sorted(df['model_version'].dropna().unique().tolist())
        selected_model = st.selectbox("Model", model_options)
        
        prompt_search = st.text_input("Prompt contains", "")
        
        st.subheader("Date Range")
        use_date_filter = st.checkbox("Filter by date")
        date_range = None
        if use_date_filter:
            min_date = df['created_at'].min().date() if not df['created_at'].isna().all() else datetime.now().date()
            max_date = df['created_at'].max().date() if not df['created_at'].isna().all() else datetime.now().date()
            date_range = st.date_input(
                "Select range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
    
    # Apply filters
    filtered_df = filter_images(
        df,
        source=selected_source,
        model=selected_model,
        prompt_search=prompt_search,
        date_range=date_range if use_date_filter else None
    )
    
    st.caption(f"Showing from {len(filtered_df):,} images (filtered from {len(df):,} total)")
    
    # Random button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 Get Random Image", use_container_width=True, type="primary"):
            st.session_state.random_seed = random.randint(0, 999999)
    
    # Initialize or get random seed
    if 'random_seed' not in st.session_state:
        st.session_state.random_seed = random.randint(0, 999999)
    
    if filtered_df.empty:
        st.warning("No images match your filters.")
        return
    
    # Select random image
    random.seed(st.session_state.random_seed)
    selected_idx = random.randint(0, len(filtered_df) - 1)
    image_data = filtered_df.iloc[selected_idx]
    
    # Display image
    st.image(image_data['url'], use_container_width=True)
    
    # Metadata
    with st.expander("📋 Image Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Source:** {image_data.get('source', 'N/A')}")
            st.markdown(f"**Platform:** {image_data.get('platform', 'N/A')}")
            st.markdown(f"**Model:** {image_data.get('model_version', 'N/A')}")
        
        with col2:
            st.markdown(f"**Date:** {image_data.get('created_at', 'N/A')}")
            st.markdown(f"**Seed:** {image_data.get('seed', 'N/A')}")
            st.markdown(f"**Aspect:** {image_data.get('aspect_ratio', 'N/A')}")
        
        if image_data.get('prompt'):
            st.markdown("**Prompt:**")
            st.code(image_data['prompt'], language=None)
            
            if st.button("📋 Copy Prompt"):
                st.write("Prompt copied to clipboard!")
                st.session_state.clipboard = image_data['prompt']


def page_search():
    """Search images by prompt."""
    st.title("🔍 Search by Prompt")
    
    df = load_manifest()
    if df.empty:
        return
    
    search_query = st.text_input("Search prompts", "", placeholder="e.g., cyberpunk samurai")
    
    if search_query:
        results = filter_images(df, prompt_search=search_query)
        
        st.caption(f"Found {len(results):,} images")
        
        if not results.empty:
            # Display as grid
            cols = st.columns(4)
            for idx, (_, row) in enumerate(results.head(20).iterrows()):
                with cols[idx % 4]:
                    st.image(row['url'], use_container_width=True)
                    if row.get('prompt'):
                        st.caption(row['prompt'][:50] + "..." if len(str(row['prompt'])) > 50 else row['prompt'])
            
            if len(results) > 20:
                st.info(f"Showing first 20 of {len(results):,} results")


def page_stats():
    """Statistics dashboard."""
    st.title("📊 Library Statistics")
    
    df = load_manifest()
    if df.empty:
        return
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Images", f"{len(df):,}")
    
    with col2:
        likes_count = len(df[df['source'] == 'likes'])
        st.metric("Liked", f"{likes_count:,}")
    
    with col3:
        created_count = len(df[df['source'] == 'created'])
        st.metric("Created", f"{created_count:,}")
    
    with col4:
        models = df['model_version'].nunique()
        st.metric("Models Used", models)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Images by Month")
        if 'month' in df.columns:
            monthly = df.groupby('month').size().reset_index(name='count')
            monthly = monthly.sort_values('month')
            st.bar_chart(monthly.set_index('month'))
    
    with col2:
        st.subheader("Images by Source")
        source_counts = df['source'].value_counts()
        st.bar_chart(source_counts)
    
    # Model breakdown
    st.subheader("Images by Model")
    model_counts = df['model_version'].value_counts().head(10)
    st.bar_chart(model_counts)
    
    # Recent images
    st.subheader("Most Recent Images")
    recent = df.nlargest(8, 'created_at')
    cols = st.columns(4)
    for idx, (_, row) in enumerate(recent.iterrows()):
        with cols[idx % 4]:
            st.image(row['url'], use_container_width=True)


def page_gallery():
    """Browse all images in a gallery view."""
    st.title("🖼️ Gallery")
    
    df = load_manifest()
    if df.empty:
        return
    
    # Filters in sidebar
    with st.sidebar:
        st.header("Filters")
        
        source_options = ["All"] + sorted(df['source'].dropna().unique().tolist())
        selected_source = st.selectbox("Source", source_options, key="gallery_source")
        
        if 'month' in df.columns:
            month_options = ["All"] + sorted(df['month'].dropna().unique().tolist(), reverse=True)
            selected_month = st.selectbox("Month", month_options)
        else:
            selected_month = "All"
    
    # Apply filters
    filtered = df.copy()
    if selected_source != "All":
        filtered = filtered[filtered['source'] == selected_source.lower()]
    if selected_month != "All":
        filtered = filtered[filtered['month'] == selected_month]
    
    st.caption(f"Showing {len(filtered):,} images")
    
    # Pagination
    images_per_page = 20
    total_pages = max(1, len(filtered) // images_per_page + (1 if len(filtered) % images_per_page else 0))
    
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    
    start_idx = (page - 1) * images_per_page
    end_idx = start_idx + images_per_page
    page_images = filtered.iloc[start_idx:end_idx]
    
    # Display grid
    cols = st.columns(4)
    for idx, (_, row) in enumerate(page_images.iterrows()):
        with cols[idx % 4]:
            st.image(row['url'], use_container_width=True)
            if st.button("View", key=f"view_{row['job_id']}"):
                st.session_state.selected_image = row.to_dict()
    
    st.caption(f"Page {page} of {total_pages}")


# ============== MAIN APP ============== #
def main():
    # Navigation
    st.sidebar.title("🎨 Niji Library")
    
    page = st.sidebar.radio(
        "Navigate",
        ["Random", "Search", "Gallery", "Stats"],
        label_visibility="collapsed"
    )
    
    # Render selected page
    if page == "Random":
        page_random()
    elif page == "Search":
        page_search()
    elif page == "Gallery":
        page_gallery()
    elif page == "Stats":
        page_stats()
    
    # Footer
    st.sidebar.divider()
    st.sidebar.caption("Built with ❤️ for AI art collectors")
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()


if __name__ == "__main__":
    main()
