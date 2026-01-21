"""
Niji 6 Illustrator Partner
Visual prompt builder for Midjourney's Niji 6.
"""

import streamlit as st
import random
from dataclasses import dataclass, field
from typing import Optional, List

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Niji 6 Illustrator Partner",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg-dark: #0a0a0f;
        --bg-card: #14141f;
        --accent: #e94560;
        --accent-secondary: #6b5ce7;
        --text-primary: #ffffff;
        --text-secondary: #9999bb;
        --border: #2a2a40;
    }
    
    .stApp {
        background: linear-gradient(180deg, var(--bg-dark) 0%, #12121f 100%);
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
    }
    
    h1 {
        background: linear-gradient(90deg, #e94560 0%, #ff8a80 50%, #6b5ce7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem !important;
    }
    
    .command-output {
        background: #080810;
        border: 1px solid var(--accent);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #00ff88;
        line-height: 1.7;
        word-break: break-word;
    }
    
    .info-panel {
        background: linear-gradient(135deg, rgba(107, 92, 231, 0.1) 0%, rgba(233, 69, 96, 0.05) 100%);
        border-left: 3px solid var(--accent-secondary);
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }
    
    .info-panel h5 {
        color: var(--text-primary);
        margin: 0 0 0.25rem 0;
        font-size: 1.1rem;
    }
    
    .info-panel p {
        color: var(--text-secondary);
        margin: 0;
        font-size: 0.9rem;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    .section-header .icon {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%);
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--border) 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    .rating-badge {
        display: inline-block;
        background: rgba(233, 69, 96, 0.15);
        color: var(--accent);
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    
    .stButton > button {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        border-radius: 10px;
    }
    
    .stTextInput input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--accent) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        color: var(--text-secondary);
        font-family: 'Outfit', sans-serif;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1a1525 0%, #201530 100%);
        border-color: var(--accent);
        color: var(--text-primary);
    }
    
    #MainMenu, footer, header {visibility: hidden;}
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
    icon: str
    description: str
    vibe: str
    base_prompt: str
    profile: str
    sref: Optional[str] = None
    sw: int = 30
    notes: str = ""
    rating: str = ""


# -----------------------------
# Preset Database
# -----------------------------
PRESETS = [
    # ACTION
    StylePreset(
        id="action_manga",
        name="Action Manga",
        category="Action",
        icon="⚡",
        description="High-energy panels",
        vibe="Anime character in action, manga panel energy, clean ink/tones",
        base_prompt="Black and white Manga Panel, perspective, dynamic pose, motion lines, dramatic foreshortening, expressive face, fine details",
        profile="xp1wzqg",
        sref="3334207109",
        sw=30,
        notes="PERFECT 4/4! Your 'easy button' for action scenes.",
        rating="4/4 ⭐"
    ),
    StylePreset(
        id="sketchbook_inoue",
        name="Inoue Sketch",
        category="Action",
        icon="✏️",
        description="Gritty graphite feel",
        vibe="Author sketch feel, less glossy, more human linework",
        base_prompt="In the style of Takehiko Inoue, manga panel, halftone, screentone, sketchbook aesthetic, graphite pencil and ink",
        profile="xp1wzqg",
        notes="Great for dramatic character close-ups.",
        rating="Favorite"
    ),
    StylePreset(
        id="artgerm_glamour",
        name="ArtGerm Glam",
        category="Action",
        icon="💎",
        description="Polished comic style",
        vibe="Magazine-quality finish, flattering lighting",
        base_prompt="Black and white Manga Panel, perspective, dynamic pose, clean shapes, flattering lighting, In the style of ArtGerm and J Scott Campbell",
        profile="xp1wzqg",
        sref="3334207109",
        sw=35,
        notes="Use --stylize 1000 for max detail.",
        rating="Powerful"
    ),
    
    # CINEMATIC
    StylePreset(
        id="movie_frame",
        name="Movie Frame",
        category="Cinematic",
        icon="🎬",
        description="Akira/Ghibli film stills",
        vibe="Anime film still, story moments, environment-first",
        base_prompt="Movie frame from Akira directed by Ghibli, wideshot, cinematic composition, atmospheric lighting, manga inspired",
        profile="xp1wzqg",
        notes="Rated 5/4! High-budget anime movie feel.",
        rating="5/4 🏆"
    ),
    StylePreset(
        id="painterly_cover",
        name="Painterly Cover",
        category="Cinematic",
        icon="🎨",
        description="Emotional book cover vibe",
        vibe="Cinematic portrait, painterly manga illustration",
        base_prompt="Painterly manga book cover, emotional atmosphere, detailed rendering, high contrast",
        profile="xp1wzqg",
        sref="2180084546",
        notes="Best sref for cover art and fantasy portraits.",
        rating="Best SREF"
    ),
    StylePreset(
        id="wlop_charming",
        name="WLOP Fantasy",
        category="Cinematic",
        icon="✨",
        description="High-end character design",
        vibe="Charming aesthetics, glamorous anime style",
        base_prompt="In the style of WLOP and SakiMiCham, charming girl, glamorous anime artstyle, cinematic, dramatic lights",
        profile="xp1wzqg",
        sref="2180084546",
        notes="Excellent for fantasy character concepts.",
        rating="High Level"
    ),
    
    # GRAPHIC
    StylePreset(
        id="single_line",
        name="Single-Line",
        category="Graphic",
        icon="〰️",
        description="Crisp, minimal lines",
        vibe="Simplified anime look, graphic clarity",
        base_prompt="Manga inspired, black and white, crisp single-line weight sketch, clean graphic style",
        profile="xp1wzqg",
        sref="3599646714::1",
        sw=35,
        notes="Excellent single line weight. Clean and minimal.",
        rating="Excellent"
    ),
    StylePreset(
        id="likeness_line",
        name="Likeness Line",
        category="Graphic",
        icon="👤",
        description="Better face fidelity",
        vibe="Clean line with character likeness",
        base_prompt="Black and white manga panel, crisp line",
        profile="xp1wzqg",
        sref="2033610796::1",
        notes="Does well with likeness even without cref.",
        rating="Good Likeness"
    ),
    StylePreset(
        id="horror_cover",
        name="Horror/Dark",
        category="Graphic",
        icon="👁️",
        description="Creepy, unsettling mood",
        vibe="Dark fantasy, psychological horror",
        base_prompt="In the style of Junji Ito, Gege Akutami, Kazuma Kaneko, manga cover, eerie mood, high-contrast black and white, unsettling detail",
        profile="xp1wzqg",
        notes="Really creepy... worth experimenting!",
        rating="Banger 🔥"
    ),
]

QUICK_MAP = {
    "⚡ Action Panel": "action_manga",
    "🎬 Movie Frame": "movie_frame", 
    "📖 Book Cover": "painterly_cover",
    "✏️ Sketchy": "sketchbook_inoue",
    "〰️ Clean Line": "single_line",
    "👁️ Horror": "horror_cover",
}

CATEGORIES = ["Action", "Cinematic", "Graphic"]


# -----------------------------
# Session State
# -----------------------------
if "selected_id" not in st.session_state:
    st.session_state.selected_id = "action_manga"
if "history" not in st.session_state:
    st.session_state.history = []
if "sexy_mode" not in st.session_state:
    st.session_state.sexy_mode = False
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "scene" not in st.session_state:
    st.session_state.scene = ""


# -----------------------------
# Helper Functions
# -----------------------------
def get_preset(preset_id: str) -> StylePreset:
    return next((p for p in PRESETS if p.id == preset_id), PRESETS[0])

def select_preset(preset_id: str):
    st.session_state.selected_id = preset_id

def randomize():
    st.session_state.selected_id = random.choice(PRESETS).id
    subjects = [
        "cyberpunk samurai, neon katana",
        "forest witch, ancient grimoire",
        "mech pilot, battle-damaged cockpit",
        "shadow assassin, moonlit rooftop",
        "space explorer, alien ruins",
        "rebel knight, shattered armor",
        "dream weaver, floating threads",
        "storm caller, lightning crown",
    ]
    st.session_state.subject = random.choice(subjects)

def build_command(preset: StylePreset, subject: str, scene: str, sw: int, stylize: int, ar: str, cref: str, cw: int, sexy_mode: bool) -> str:
    parts = [preset.base_prompt]
    if subject.strip():
        parts.append(subject.strip())
    if scene.strip():
        parts.append(scene.strip())
    prompt = ", ".join(parts)
    
    profile = "1vkrwxy elkd3fo pjmf3zg ulvca2i" if sexy_mode else preset.profile
    
    params = [f"--niji 6", f"--profile {profile}"]
    if preset.sref:
        params.append(f"--sref {preset.sref}")
    params.append(f"--sw {sw}")
    params.append(f"--stylize {stylize}")
    
    if cref.strip():
        params.append(f"--cref {cref.strip()}")
        params.append(f"--cw {cw}")
    
    if ar.strip():
        ar_val = ar.strip().replace("--ar ", "")
        params.append(f"--ar {ar_val}")
    
    return f"/imagine prompt: {prompt} {' '.join(params)}"


# -----------------------------
# App Layout
# -----------------------------

# Header
st.markdown("# 🎨 Niji 6 Illustrator Partner")
st.caption("Visual prompt builder for manga & anime styles")

# Quick Chooser
st.markdown('<div class="section-header"><div class="icon">⚡</div><h3>Quick Pick</h3></div>', unsafe_allow_html=True)

cols = st.columns(len(QUICK_MAP))
for i, (label, preset_id) in enumerate(QUICK_MAP.items()):
    with cols[i]:
        is_active = st.session_state.selected_id == preset_id
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"q_{preset_id}", use_container_width=True, type=btn_type):
            select_preset(preset_id)
            st.rerun()

# Randomize and toggle
col_r, col_s, _ = st.columns([1, 1, 4])
with col_r:
    if st.button("🎲 Randomize", use_container_width=True):
        randomize()
        st.rerun()
with col_s:
    st.session_state.sexy_mode = st.toggle("✨ Sexy Jutsu", st.session_state.sexy_mode, help="Multi-profile 'Lady Manga' mix")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Main: Style Library | Build Prompt
left, right = st.columns([1.3, 1])

with left:
    st.markdown('<div class="section-header"><div class="icon">🎭</div><h3>Style Library</h3></div>', unsafe_allow_html=True)
    
    cat_tabs = st.tabs([f"{'⚡' if c=='Action' else '🎬' if c=='Cinematic' else '✏️'} {c}" for c in CATEGORIES])
    
    for tab, category in zip(cat_tabs, CATEGORIES):
        with tab:
            cat_presets = [p for p in PRESETS if p.category == category]
            
            for preset in cat_presets:
                is_selected = st.session_state.selected_id == preset.id
                
                with st.container():
                    card_col, btn_col = st.columns([4, 1])
                    
                    with card_col:
                        status = "✓ " if is_selected else ""
                        st.markdown(f"**{status}{preset.icon} {preset.name}**")
                        st.caption(f"{preset.description}")
                        if preset.rating:
                            st.markdown(f'<span class="rating-badge">{preset.rating}</span>', unsafe_allow_html=True)
                    
                    with btn_col:
                        if st.button("Select" if not is_selected else "✓", key=f"sel_{preset.id}", disabled=is_selected):
                            select_preset(preset.id)
                            st.rerun()
                    
                    st.markdown("---")

with right:
    st.markdown('<div class="section-header"><div class="icon">🖌️</div><h3>Build Prompt</h3></div>', unsafe_allow_html=True)
    
    current = get_preset(st.session_state.selected_id)
    
    st.markdown(f"""
    <div class="info-panel">
        <h5>{current.icon} {current.name}</h5>
        <p>{current.vibe}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if current.notes:
        st.info(f"💡 {current.notes}")
    
    subject = st.text_input(
        "Subject / Character",
        value=st.session_state.subject,
        placeholder="e.g., cyberpunk heroine, superhero pose",
        key="subject_in"
    )
    st.session_state.subject = subject
    
    scene = st.text_input(
        "Scene / Camera",
        value=st.session_state.scene,
        placeholder="e.g., low-angle, neon rain, rooftop",
        key="scene_in"
    )
    st.session_state.scene = scene
    
    with st.expander("⚙️ Micro-Tuning", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            sw = st.slider(
                "--sw (Style Weight)",
                0, 1000, current.sw, 5,
                help="30-35: Default • 40-65: Stronger manga • 300+: Lineweight bulldozer"
            )
        with c2:
            default_sty = 1000 if "ArtGerm" in current.name else 100
            stylize = st.slider("--stylize", 0, 1000, default_sty, 50, help="1000 = max detail")
        
        ar = st.text_input("Aspect Ratio", "2:3", help="e.g., 2:3, 16:9, 1:1")
        
        st.markdown("##### Character Reference (Optional)")
        cref_col1, cref_col2 = st.columns([3, 1])
        with cref_col1:
            cref = st.text_input("--cref URL", "", placeholder="Grayscale image URL", label_visibility="collapsed")
        with cref_col2:
            cw = st.number_input("--cw", 0, 100, 20, help="Character weight")
    
    # Command output
    st.markdown("### 📋 Command")
    
    cmd = build_command(current, subject, scene, sw, stylize, ar, cref, cw, st.session_state.sexy_mode)
    
    st.markdown(f'<div class="command-output">{cmd}</div>', unsafe_allow_html=True)
    
    # Copyable code block
    st.code(cmd, language=None)
    
    # Save button
    if st.button("💾 Save to History", use_container_width=True):
        st.session_state.history.append({"name": current.name, "cmd": cmd})
        st.toast("Saved!", icon="✅")

# History
if st.session_state.history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    with st.expander(f"📜 History ({len(st.session_state.history)})", expanded=False):
        if st.button("🗑️ Clear All"):
            st.session_state.history = []
            st.rerun()
        for i, h in enumerate(reversed(st.session_state.history)):
            st.markdown(f"**{i+1}. {h['name']}**")
            st.code(h['cmd'], language=None)

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem; padding: 1rem;">
    <strong>Tips:</strong> Raise --sw if output looks generic • Use grayscale refs with --cref • 
    Swap --sref for instant style changes
</div>
""", unsafe_allow_html=True)
