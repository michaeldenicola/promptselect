import streamlit as st
import random
from dataclasses import dataclass, asdict
from typing import List, Optional

st.set_page_config(page_title="Niji 6 Pro Builder", layout="wide")

# -----------------------------
# Core Data from Notes
# -----------------------------
@dataclass
class Preset:
    name: str
    description: str
    base_prompt: str
    profile: str
    sref: Optional[str] = None
    sw: Optional[int] = None
    notes: str = ""

# Presets accurately mapped to your "Default Stacks" [cite: 84, 86, 87]
PRESETS = {
    "Action": [
        Preset(
            name="Action Manga Panel (Easy Button)",
            description="Your most consistent lane for high-energy scenes[cite: 88].",
            base_prompt="Black and white Manga Panel, perspective, dynamic pose, motion lines, dramatic foreshortening, expressive face, fine details, {subject}, {scene}",
            profile="xp1wzqg",
            sref="3334207109",
            sw=30,
            notes="Rated PERFECT 4/4! Use for character action and clean ink/tones."
        ),
        Preset(
            name="Sketchbook (Inoue Lane)",
            description="Rough graphite and textured hatching[cite: 91].",
            base_prompt="In the style of Takehiko Inoue, manga panel, halftone, screentone, sketchbook aesthetic, graphite pencil and ink, {subject}, {scene}",
            profile="xp1wzqg",
            notes="Author sketch feel. Great for 'human' linework and human expressions[cite: 91]."
        ),
    ],
    "Cinematic": [
        Preset(
            name="Movie Frame (Akira/Ghibli)",
            description="High-budget film stills and wide compositions[cite: 90].",
            base_prompt="Movie frame from Akira directed by Ghibli, wideshot, cinematic composition, atmospheric lighting, manga inspired, {scene}, {subject}",
            profile="xp1wzqg",
            notes="Your 5/4 rated lane. Excellent for world-building[cite: 90, 101]."
        ),
        Preset(
            name="Painterly Cover",
            description="Emotional and illustrative 'book cover' vibe[cite: 86, 92].",
            base_prompt="Painterly manga book cover, emotional atmosphere, detailed rendering, high contrast, {subject}, {scene}",
            profile="xp1wzqg",
            sref="2180084546",
            notes="Best of the SREFs for a polished, fantasy illustration look[cite: 65, 86]."
        ),
    ],
    "Graphic": [
        Preset(
            name="Clean Single-Line",
            description="Crisp contour lines and graphic simplicity[cite: 87].",
            base_prompt="Manga inspired, black and white, crisp single-line weight sketch, clean graphic style, {subject}, {scene}",
            profile="xp1wzqg",
            sref="3599646714::1",
            sw=35,
            notes="Excellent single line weight for a simplified anime look[cite: 87]."
        ),
        Preset(
            name="Horror/Unsettling Cover",
            description="Creepy, high-contrast, eerie mood.",
            base_prompt="In the style of Junji Ito, Gege Akutami, Kazuma Kaneko, manga cover, eerie mood, high-contrast black and white, unsettling detail, {subject}",
            profile="xp1wzqg",
            notes="Flagged as 'really creepy'—worth experimenting for dark themes[cite: 92, 99]."
        ),
    ]
}

# -----------------------------
# Sidebar Chooser & Logic
# -----------------------------
with st.sidebar:
    st.title("🎯 2-Second Chooser")
    st.markdown("""
    **Quick Guide[cite: 94]:**
    - **Action/Panel?** → Action Stack
    - **Wide Shot/Film?** → Cinematic Stack
    - **Book Cover?** → Painterly
    - **Gritty/Sketch?** → Inoue Lane
    - **Clean/Flat?** → Single-Line
    """)
    st.divider()
    
    # Sexy Jutsu Toggle 
    sexy_jutsu = st.toggle("✨ Sexy Jutsu Moodboard", help="Swaps default profile for the multi-profile 'Lady Manga' mix.")
    moodboard_profile = "1vkrwxy elkd3fo pjmf3zg ulvca2i" if sexy_jutsu else None

# -----------------------------
# Main UI
# -----------------------------
st.title("Niji 6 Illustrator Partner")

tab1, tab2, tab3 = st.tabs(["Action Stacks", "Cinematic Stacks", "Graphic Stacks"])

def render_preset_ui(presets: List[Preset]):
    selected_name = st.selectbox("Choose a Look", [p.name for p in presets])
    selected_preset = next(p for p in presets if p.name == selected_name)
    
    st.caption(f"**Vibe:** {selected_preset.description}")
    if selected_preset.notes:
        st.info(selected_preset.notes)
    
    col1, col2 = st.columns(2)
    with col1:
        subj = st.text_input("Subject", "cyberpunk heroine, superhero pose")
    with col2:
        scn = st.text_input("Scene/Camera", "low-angle, neon rain, city alley")
        
    # Parameters
    with st.expander("Micro-Tuning Knobs", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            sw_val = st.slider("Style Weight (--sw)", 0, 1000, selected_preset.sw if selected_preset.sw else 30)
        with c2:
            stylize = st.slider("Stylize", 0, 1000, 100 if "ArtGerm" not in selected_name else 1000)
        with c3:
            ar = st.text_input("Aspect Ratio", "--ar 2:3")

    # Build Prompt
    final_subject = subj.strip()
    final_scene = f", {scn.strip()}" if scn.strip() else ""
    prompt_text = selected_preset.base_prompt.format(subject=final_subject, scene=final_scene)
    
    # Params
    profile = moodboard_profile if moodboard_profile else selected_preset.profile
    sref = f"--sref {selected_preset.sref}" if selected_preset.sref else ""
    
    full_command = f"/imagine prompt: {prompt_text} --niji 6 --profile {profile} {sref} --sw {sw_val} --stylize {stylize} {ar}".replace("  ", " ")
    
    st.subheader("Final Command")
    st.code(full_command)

with tab1: render_preset_ui(PRESETS["Action"])
with tab2: render_preset_ui(PRESETS["Cinematic"])
with tab3: render_preset_ui(PRESETS["Graphic"])
