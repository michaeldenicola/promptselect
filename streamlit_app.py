"""
Niji 6 Illustrator Partner
A visual prompt builder for Midjourney's Niji 6 with style presets and micro-tuning.
"""

import streamlit as st
import random
from dataclasses import dataclass, field
from typing import Optional, List
import pyperclip

# -----------------------------
# Page Config & Custom Styling
# -----------------------------
st.set_page_config(
    page_title="Niji 6 Illustrator Partner",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject dark manga-inspired CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        background: linear-gradient(90deg, #e94560, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Style cards */
    .style-card {
        background: linear-gradient(145deg, #1e1e2f, #2a2a40);
        border: 2px solid #333355;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        min-height: 140px;
    }
    
    .style-card:hover {
        border-color: #e94560;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3);
    }
    
    .style-card.selected {
        border-color: #e94560;
        background: linear-gradient(145deg, #2a1a2f, #3a2a45);
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.4);
    }
    
    .style-card h4 {
        font-family: 'Space Grotesk', sans-serif;
        color: #ffffff;
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }
    
    .style-card p {
        color: #aaaacc;
        font-size: 0.85rem;
        margin: 0;
        line-height: 1.4;
    }
    
    .style-card .tag {
        display: inline-block;
        background: rgba(233, 69, 96, 0.2);
        color: #e94560;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
        margin-top: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Command output box */
    .command-box {
        background: #0d0d15;
        border: 1px solid #e94560;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #00ff88;
        word-wrap: break-word;
        line-height: 1.6;
        margin: 1rem 0;
    }
    
    /* Quick chooser badges */
    .quick-badge {
        display: inline-block;
        background: linear-gradient(135deg, #e94560, #ff6b6b);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.8rem;
        margin: 0.3rem;
        cursor: pointer;
        font-family: 'Space Grotesk', sans-serif;
        transition: all 0.2s ease;
    }
    
    .quick-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
    }
    
    /* Randomizer button */
    .dice-btn {
        background: linear-gradient(135deg, #6b5ce7, #8b7cf7) !important;
        border: none !important;
        color: white !important;
        font-size: 1.2rem !important;
    }
    
    /* Section dividers */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #e94560, transparent);
        margin: 2rem 0;
    }
    
    /* Slider customization */
    .stSlider > div > div {
        background-color: #e94560 !important;
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(107, 92, 231, 0.1);
        border-left: 3px solid #6b5ce7;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.85rem;
        color: #ccccee;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #ff6b6b);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(233, 69, 96, 0.4);
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background: #1e1e2f;
        border: 1px solid #333355;
        color: #ffffff;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #e94560;
        box-shadow: 0 0 10px rgba(233, 69, 96, 0.3);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1e1e2f;
        border-radius: 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1e1e2f;
        border-radius: 8px 8px 0 0;
        color: #aaaacc;
        border: 1px solid #333355;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #2a1a2f, #3a2a45);
        border-color: #e94560;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Data Models
# -----------------------------
@dataclass
class StylePreset:
    id: str
    name: str
    category: str
    description: str
    vibe: str
    base_prompt: str
    profile: str
    sref: Optional[str] = None
    sw: int = 30
    notes: str = ""
    tags: List[str] = field(default_factory=list)
    rating: str = ""


# -----------------------------
# Preset Database (from your notes)
# -----------------------------
PRESETS = [
    # ACTION STACKS
    StylePreset(
        id="action_manga",
        name="Action Manga Panel",
        category="Action",
        description="Most consistent lane for high-energy scenes",
        vibe="Anime character in action, manga panel energy, clean ink/tones",
        base_prompt="Black and white Manga Panel, perspective, dynamic pose, motion lines, dramatic foreshortening, expressive face, fine details",
        profile="xp1wzqg",
        sref="3334207109",
        sw=30,
        notes="Rated PERFECT 4/4! Your 'easy button' for action.",
        tags=["panel", "action", "ink"],
        rating="4/4"
    ),
    StylePreset(
        id="sketchbook_inoue",
        name="Sketchbook (Inoue Lane)",
        category="Action",
        description="Rough graphite and textured hatching",
        vibe="Author sketch feel, less glossy, more human linework",
        base_prompt="In the style of Takehiko Inoue, manga panel, halftone, screentone, sketchbook aesthetic, graphite pencil and ink",
        profile="xp1wzqg",
        notes="Great for dramatic character close-ups and 'real' drawn feel.",
        tags=["sketch", "gritty", "pencil"],
        rating="Favorite"
    ),
    StylePreset(
        id="artgerm_glamour",
        name="ArtGerm/JSC Glamour",
        category="Action",
        description="Polished comic glamour with clean shapes",
        vibe="Magazine-quality finish, flattering lighting, punchy",
        base_prompt="Black and white Manga Panel, perspective, dynamic pose, clean shapes, flattering lighting, In the style of ArtGerm and J Scott Campbell",
        profile="xp1wzqg",
        sref="3334207109",
        sw=35,
        notes="Just as powerful in the manga panel lane. Use --stylize 1000 for max detail.",
        tags=["glamour", "comic", "polished"],
        rating="Powerful"
    ),
    
    # CINEMATIC STACKS
    StylePreset(
        id="movie_frame",
        name="Movie Frame (Akira/Ghibli)",
        category="Cinematic",
        description="High-budget film stills and wide compositions",
        vibe="Anime film still, story moments, environment-first",
        base_prompt="Movie frame from Akira directed by Ghibli, wideshot, cinematic composition, atmospheric lighting, manga inspired",
        profile="xp1wzqg",
        notes="Rated 5/4! Perfectly captures high-budget anime movie feel.",
        tags=["cinematic", "wideshot", "atmospheric"],
        rating="5/4"
    ),
    StylePreset(
        id="painterly_cover",
        name="Painterly Cover",
        category="Cinematic",
        description="Emotional and illustrative 'book cover' vibe",
        vibe="Cinematic portrait, painterly manga illustration",
        base_prompt="Painterly manga book cover, emotional atmosphere, detailed rendering, high contrast",
        profile="xp1wzqg",
        sref="2180084546",
        notes="Maybe best of the sref. Perfect for cover art and fantasy portraits.",
        tags=["cover", "painterly", "emotional"],
        rating="Best sref"
    ),
    StylePreset(
        id="wlop_charming",
        name="WLOP/SakiMiCham",
        category="Cinematic",
        description="High-end fantasy character design",
        vibe="Charming aesthetics, waifu-style, high level",
        base_prompt="In the style of WLOP and SakiMiCham, charming girl, glamorous anime artstyle, cinematic, dramatic lights",
        profile="xp1wzqg",
        sref="2180084546",
        notes="Excellent for character design and fantasy concepts.",
        tags=["fantasy", "charming", "character"],
        rating="High level"
    ),
    
    # GRAPHIC STACKS
    StylePreset(
        id="single_line",
        name="Clean Single-Line",
        category="Graphic",
        description="Crisp contour lines and graphic simplicity",
        vibe="Simplified anime look, graphic clarity",
        base_prompt="Manga inspired, black and white, crisp single-line weight sketch, clean graphic style",
        profile="xp1wzqg",
        sref="3599646714::1",
        sw=35,
        notes="Excellent single line weight. Clean and minimal.",
        tags=["clean", "minimal", "line"],
        rating="Excellent"
    ),
    StylePreset(
        id="likeness_line",
        name="Likeness-Friendly Line",
        category="Graphic",
        description="Better face/likeness preservation",
        vibe="Clean line with better character fidelity",
        base_prompt="Black and white manga panel, crisp line",
        profile="xp1wzqg",
        sref="2033610796::1",
        notes="Does well with likeness even without cref.",
        tags=["likeness", "clean", "fidelity"],
        rating="Good likeness"
    ),
    StylePreset(
        id="horror_cover",
        name="Horror/Unsettling",
        category="Graphic",
        description="Creepy, high-contrast, eerie mood",
        vibe="Dark fantasy, psychological horror, unsettling",
        base_prompt="In the style of Junji Ito, Gege Akutami, Kazuma Kaneko, manga cover, eerie mood, high-contrast black and white, unsettling detail",
        profile="xp1wzqg",
        notes="Really creepy... worth experimenting for dark themes!",
        tags=["horror", "creepy", "dark"],
        rating="Banger"
    ),
]

# Category groupings for display
CATEGORIES = {
    "Action": {"icon": "⚡", "color": "#e94560", "desc": "Dynamic poses, manga panels, movement"},
    "Cinematic": {"icon": "🎬", "color": "#6b5ce7", "desc": "Movie frames, covers, atmosphere"},
    "Graphic": {"icon": "✏️", "color": "#00d4aa", "desc": "Clean lines, minimal, graphic"}
}

# Quick chooser mapping
QUICK_CHOOSER = {
    "Action/Panel": "action_manga",
    "Wide Shot/Film": "movie_frame",
    "Book Cover": "painterly_cover",
    "Gritty/Sketch": "sketchbook_inoue",
    "Clean/Flat": "single_line",
    "Horror": "horror_cover",
    "Character Design": "wlop_charming",
}


# -----------------------------
# Session State Initialization
# -----------------------------
if "selected_preset_id" not in st.session_state:
    st.session_state.selected_preset_id = "action_manga"
if "history" not in st.session_state:
    st.session_state.history = []
if "sexy_jutsu" not in st.session_state:
    st.session_state.sexy_jutsu = False
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "scene" not in st.session_state:
    st.session_state.scene = ""


# -----------------------------
# Helper Functions
# -----------------------------
def get_preset_by_id(preset_id: str) -> StylePreset:
    return next((p for p in PRESETS if p.id == preset_id), PRESETS[0])

def select_preset(preset_id: str):
    st.session_state.selected_preset_id = preset_id

def randomize_selection():
    st.session_state.selected_preset_id = random.choice(PRESETS).id
    # Optionally randomize some fun subjects
    subjects = [
        "mysterious samurai, flowing robes",
        "cyberpunk hacker, neon tattoos",
        "dragon priestess, ancient temple",
        "space bounty hunter, chrome armor",
        "forest spirit, ethereal glow",
        "rebel mech pilot, battle-worn",
        "shadow assassin, moonlit rooftop",
        "arcane scholar, floating grimoires",
    ]
    st.session_state.subject = random.choice(subjects)

def build_command(preset: StylePreset, subject: str, scene: str, sw: int, stylize: int, ar: str, sexy_mode: bool) -> str:
    """Build the final Midjourney command."""
    # Build prompt text
    prompt_parts = [preset.base_prompt]
    if subject.strip():
        prompt_parts.append(subject.strip())
    if scene.strip():
        prompt_parts.append(scene.strip())
    prompt_text = ", ".join(prompt_parts)
    
    # Profile selection
    profile = "1vkrwxy elkd3fo pjmf3zg ulvca2i" if sexy_mode else preset.profile
    
    # Build params
    params = [f"--niji 6", f"--profile {profile}"]
    if preset.sref:
        params.append(f"--sref {preset.sref}")
    params.append(f"--sw {sw}")
    params.append(f"--stylize {stylize}")
    if ar.strip():
        ar_clean = ar.strip() if ar.strip().startswith("--ar") else f"--ar {ar.strip()}"
        params.append(ar_clean)
    
    return f"/imagine prompt: {prompt_text} {' '.join(params)}"

def copy_to_clipboard(text: str):
    """Copy text to clipboard (for local use)."""
    try:
        pyperclip.copy(text)
        return True
    except:
        return False


# -----------------------------
# UI Components
# -----------------------------
def render_style_card(preset: StylePreset, is_selected: bool) -> bool:
    """Render a clickable style card. Returns True if clicked."""
    selected_class = "selected" if is_selected else ""
    rating_badge = f'<span class="tag">{preset.rating}</span>' if preset.rating else ""
    
    card_html = f"""
    <div class="style-card {selected_class}">
        <h4>{preset.name}</h4>
        <p>{preset.description}</p>
        {rating_badge}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    return st.button(
        "Select" if not is_selected else "✓ Selected",
        key=f"btn_{preset.id}",
        disabled=is_selected,
        use_container_width=True
    )


# -----------------------------
# Main App Layout
# -----------------------------
st.markdown("# 🎨 Niji 6 Illustrator Partner")
st.markdown("*Visual prompt builder for manga & anime styles*")

# Quick 2-Second Chooser
st.markdown("### ⚡ Quick Chooser")
st.markdown('<p style="color: #888; margin-bottom: 0.5rem;">What are you making?</p>', unsafe_allow_html=True)

quick_cols = st.columns(len(QUICK_CHOOSER))
for i, (label, preset_id) in enumerate(QUICK_CHOOSER.items()):
    with quick_cols[i]:
        if st.button(label, key=f"quick_{preset_id}", use_container_width=True):
            select_preset(preset_id)

# Randomizer
col_rand, col_sexy, _ = st.columns([1, 1, 3])
with col_rand:
    if st.button("🎲 Randomize!", key="randomize"):
        randomize_selection()
        st.rerun()
with col_sexy:
    st.session_state.sexy_jutsu = st.toggle(
        "✨ Sexy Jutsu Mode",
        value=st.session_state.sexy_jutsu,
        help="Swaps profile for the multi-profile 'Lady Manga' mix"
    )

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Main content: Style selection and prompt building
left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.markdown("### 🎭 Pick Your Style")
    
    # Category tabs
    tabs = st.tabs([f"{v['icon']} {k}" for k, v in CATEGORIES.items()])
    
    for tab, (cat_name, cat_info) in zip(tabs, CATEGORIES.items()):
        with tab:
            st.markdown(f'<p style="color: #888; font-size: 0.85rem;">{cat_info["desc"]}</p>', unsafe_allow_html=True)
            
            cat_presets = [p for p in PRESETS if p.category == cat_name]
            
            for preset in cat_presets:
                is_selected = st.session_state.selected_preset_id == preset.id
                
                with st.container():
                    if render_style_card(preset, is_selected):
                        select_preset(preset.id)
                        st.rerun()

with right_col:
    st.markdown("### 🖌️ Build Your Prompt")
    
    current_preset = get_preset_by_id(st.session_state.selected_preset_id)
    
    # Show selected style info
    st.markdown(f"""
    <div class="info-box">
        <strong>Selected:</strong> {current_preset.name}<br>
        <em>{current_preset.vibe}</em>
    </div>
    """, unsafe_allow_html=True)
    
    if current_preset.notes:
        st.info(f"💡 {current_preset.notes}")
    
    # Subject and Scene inputs
    subject = st.text_input(
        "Subject / Character",
        value=st.session_state.subject,
        placeholder="e.g., cyberpunk heroine, superhero pose",
        key="subject_input"
    )
    st.session_state.subject = subject
    
    scene = st.text_input(
        "Scene / Camera / Setting",
        value=st.session_state.scene,
        placeholder="e.g., low-angle, neon rain, city alley",
        key="scene_input"
    )
    st.session_state.scene = scene
    
    # Micro-tuning
    with st.expander("⚙️ Micro-Tuning", expanded=True):
        col_sw, col_sty = st.columns(2)
        
        with col_sw:
            sw_help = """
            **Style Weight**
            - 30-35: Set-and-forget (default)
            - 40-65: Stronger manga dominance
            - 300-700: Lineweight bulldozer mode
            """
            sw = st.slider(
                "--sw (Style Weight)",
                min_value=0,
                max_value=1000,
                value=current_preset.sw,
                step=5,
                help=sw_help
            )
        
        with col_sty:
            stylize_help = """
            **Stylize**
            - 100: Normal
            - 1000: Maximum detail (magazine quality)
            """
            # Default higher stylize for ArtGerm preset
            default_stylize = 1000 if "ArtGerm" in current_preset.name else 100
            stylize = st.slider(
                "--stylize",
                min_value=0,
                max_value=1000,
                value=default_stylize,
                step=50,
                help=stylize_help
            )
        
        ar = st.text_input(
            "Aspect Ratio",
            value="2:3",
            placeholder="e.g., 2:3, 16:9, 1:1"
        )
    
    # Build and display command
    st.markdown("---")
    st.markdown("### 📋 Final Command")
    
    final_command = build_command(
        current_preset,
        subject,
        scene,
        sw,
        stylize,
        ar,
        st.session_state.sexy_jutsu
    )
    
    # Display command in styled box
    st.markdown(f'<div class="command-box">{final_command}</div>', unsafe_allow_html=True)
    
    # Action buttons
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("📋 Copy Command", use_container_width=True):
            st.code(final_command)
            st.success("Command displayed! Copy from above.")
    
    with btn_col2:
        if st.button("💾 Save to History", use_container_width=True):
            st.session_state.history.append({
                "preset": current_preset.name,
                "command": final_command
            })
            st.toast("Saved to history!", icon="✅")

# History section (collapsible)
if st.session_state.history:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    with st.expander(f"📜 Prompt History ({len(st.session_state.history)} saved)", expanded=False):
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
        
        for i, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f"**{i+1}. {item['preset']}**")
            st.code(item['command'], language=None)

# Footer with tips
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem; padding: 1rem;">
    <strong>Pro Tips:</strong> 
    If output looks too generic, raise --sw to 40-50 • 
    Swap --sref for instant look changes • 
    Use grayscale refs with --cref for best results
</div>
""", unsafe_allow_html=True)
