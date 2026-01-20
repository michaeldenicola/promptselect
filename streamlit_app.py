import streamlit as st
import random
from dataclasses import dataclass, asdict
from typing import List, Optional

st.set_page_config(page_title="Niji Prompt Builder (Bare Bones)", layout="centered")

# -----------------------------
# Presets (edit these over time)
# -----------------------------
@dataclass
class Preset:
    name: str
    description: str
    base_prompt: str               # Prompt skeleton (no params)
    profile: str                   # --profile
    niji: str = "6"                # --niji 6
    sref: Optional[str] = None     # default --sref (can be overwritten)
    sw: Optional[int] = None       # default --sw
    stylize: Optional[int] = None  # optional --stylize
    notes: str = ""                # quick guidance

PRESETS: List[Preset] = [
    Preset(
        name="Action Manga Panel (Perspective, Half-body)",
        description="Reliable manga panel energy; dynamic pose, foreshortening, camera angle.",
        base_prompt=(
            "Black and white manga panel, half-body, dramatic perspective, dynamic pose, "
            "foreshortening, speed lines, expressive face, strong silhouette, {subject}"
            "{scene}"
        ),
        profile="xp1wzqg",
        sref="3334207109",
        sw=30,
        notes="If it doesn't look 'manga' enough, raise --sw to 35–50. Keep subject concise."
    ),
    Preset(
        name="Seductive Heroine Panel (Half-body)",
        description="Pose-forward pin-up energy while staying manga/ink.",
        base_prompt=(
            "Black and white manga panel, half-body, seductive confident pose, shoulder-forward angle, "
            "head tilt, sharp eyes, clean inking, subtle screentone shadows, {subject}"
            "{scene}"
        ),
        profile="xp1wzqg",
        sref="3334207109",
        sw=35,
        notes="If it gets too glam-rendered, drop --sw to 30. Add 'impact frame' for punch."
    ),
    Preset(
        name="Single Line Weight Sketch (Clean Graphic)",
        description="Crisp contour lines, minimal hatching, graphic simplicity.",
        base_prompt=(
            "Black and white single-line weight sketch, half-body portrait, clean contour lines, "
            "minimal hatching, confident strokes, manga influence, {subject}"
            "{scene}"
        ),
        profile="xp1wzqg",
        sref="3599646714::1",
        sw=30,
        notes="If line weight varies too much, raise --sw. Keep prompt short."
    ),
    Preset(
        name="Sketchbook Portrait (Inoue lane)",
        description="Rough graphite/ink sketchbook vibe; textured hatching and imperfection.",
        base_prompt=(
            "Takehiko Inoue sketchbook aesthetic, half-body portrait, graphite pencil and ink, "
            "loose sketch lines, crosshatching, screentone/halftone, imperfect strokes, {subject}"
            "{scene}"
        ),
        profile="xp1wzqg",
        sref=None,
        sw=None,
        notes="Use when you want drawn texture over polish. Works well without heavy params."
    ),
    Preset(
        name="Cinematic Cover (Painterly Manga)",
        description="Emotional cover illustration; cinematic lighting and atmosphere.",
        base_prompt=(
            "Painterly manga cover illustration, half-body, cinematic lighting, emotional atmosphere, "
            "high contrast, subtle texture, {subject}"
            "{scene}"
        ),
        profile="xp1wzqg",
        sref="2180084546",
        sw=None,
        notes="If it looks too generic, try --sw 20–40. Add mood words: 'noir', 'neon haze', etc."
    ),
    Preset(
        name="Horror Cover (Unsettling B&W)",
        description="Creepy manga cover; uncanny detail, heavy shadow, unsettling expression.",
        base_prompt=(
            "Black and white manga cover, half-body, unsettling expression, uncanny detail, "
            "heavy shadows, disturbing atmosphere, high contrast inks, {subject}"
            "{scene}"
        ),
        profile="xp1wzqg",
        sref=None,
        sw=None,
        notes="Toggle this when you want the vibe to go wrong (in a good way)."
    ),
]

FAVORITES = [
    # Keep this as short curated 'random favorite' prompts
    {
        "name": "Action Panel Default",
        "subject": "cyberpunk heroine, superhero pose, dynamic punch",
        "scene": " low-angle camera, city alley, rain, neon signage",
        "preset": "Action Manga Panel (Perspective, Half-body)",
        "overrides": {"sw": 30}
    },
    {
        "name": "Single Line Poster",
        "subject": "mysterious femme fatale, sharp eyes, confident smirk",
        "scene": " minimal background, strong silhouette",
        "preset": "Single Line Weight Sketch (Clean Graphic)",
        "overrides": {"sw": 40}
    },
]

def find_preset(name: str) -> Preset:
    for p in PRESETS:
        if p.name == name:
            return p
    return PRESETS[0]

def normalize_list_field(raw: str) -> List[str]:
    """
    Accepts newline or comma separated strings. Returns a list of non-empty trimmed items.
    """
    if not raw:
        return []
    parts = []
    for line in raw.replace(",", "\n").split("\n"):
        s = line.strip()
        if s:
            parts.append(s)
    return parts

def build_prompt_and_params(
    preset: Preset,
    subject: str,
    scene: str,
    image_prompt_urls: List[str],
    cref_urls: List[str],
    sref_value: Optional[str],
    sw_value: Optional[int],
    cw_value: Optional[int],
    iw_value: Optional[float],
    stylize_value: Optional[int],
    extra_params: str,
) -> (str, str):
    scene_block = ""
    if scene.strip():
        scene_block = f", {scene.strip()}"

    prompt_body = preset.base_prompt.format(subject=subject.strip(), scene=scene_block)

    # Image prompt URLs go at the front of the prompt (classic MJ behavior)
    prefix = ""
    if image_prompt_urls:
        prefix = " ".join(image_prompt_urls) + " "

    full_prompt = (prefix + prompt_body).strip()

    params = []
    # Core model
    params.append(f"--niji {preset.niji}")
    if preset.profile:
        params.append(f"--profile {preset.profile}")

    # Style ref
    if sref_value:
        params.append(f"--sref {sref_value}")

    # Style weight
    if sw_value is not None:
        params.append(f"--sw {sw_value}")

    # Character refs
    if cref_urls:
        params.append(f"--cref " + " ".join(cref_urls))
    if cw_value is not None and cref_urls:
        params.append(f"--cw {cw_value}")

    # Image influence
    if iw_value is not None and image_prompt_urls:
        # MJ expects number; keep as provided
        params.append(f"--iw {iw_value}")

    # Stylize
    if stylize_value is not None:
        params.append(f"--stylize {stylize_value}")

    # Extra params (raw)
    if extra_params.strip():
        params.append(extra_params.strip())

    return full_prompt, " ".join(params)

# -----------------------------
# UI
# -----------------------------
st.title("Niji 6 Prompt Builder (Bare-bones, text-only)")
st.caption("Pick a preset → type subject → optionally add refs and tweak weights → copy prompt.")

# Random favorite
colA, colB = st.columns([1, 1])
with colA:
    if st.button("🎲 Random Favorite"):
        fav = random.choice(FAVORITES)
        st.session_state["preset_name"] = fav["preset"]
        st.session_state["subject"] = fav["subject"]
        st.session_state["scene"] = fav["scene"]
        st.session_state["fav_overrides"] = fav.get("overrides", {})
        st.toast(f"Loaded: {fav['name']}", icon="🎲")

with colB:
    st.write("")  # spacing

preset_names = [p.name for p in PRESETS]
preset_name = st.selectbox(
    "Choose a Look / Lane",
    preset_names,
    index=preset_names.index(st.session_state.get("preset_name", preset_names[0]))
    if st.session_state.get("preset_name") in preset_names else 0
)
preset = find_preset(preset_name)

st.markdown(f"**What it’s for:** {preset.description}")
if preset.notes:
    st.info(preset.notes)

subject = st.text_input(
    "Subject (what you want to see)",
    value=st.session_state.get("subject", "seductive cyberpunk heroine, superhero pose")
)

scene = st.text_input(
    "Scene / Camera (optional)",
    value=st.session_state.get("scene", "low-angle camera, neon rain, city alley")
)

with st.expander("Advanced (Refs + Weights + Params)", expanded=True):
    st.markdown("**Refs**")
    st.caption("Tip: For --cref tests, your notes prefer using grayscale character refs to improve fidelity.")

    image_urls_raw = st.text_area(
        "Image prompt URL(s) (optional) — goes at the FRONT of prompt. One per line or comma-separated.",
        height=90,
        value=""
    )
    image_prompt_urls = normalize_list_field(image_urls_raw)

    cref_raw = st.text_area(
        "Character reference URL(s) for --cref (optional). One per line or comma-separated.",
        height=90,
        value=""
    )
    cref_urls = normalize_list_field(cref_raw)

    st.markdown("**Style ref + weights**")
    default_sref = preset.sref or ""
    sref_value = st.text_input("Style ref (--sref)", value=default_sref)

    # Apply favorite overrides if present
    fav_overrides = st.session_state.get("fav_overrides", {})
    sw_default = fav_overrides.get("sw", preset.sw)
    cw_default = fav_overrides.get("cw", 20)
    iw_default = fav_overrides.get("iw", 1.0)

    sw_value = st.slider("Style weight (--sw)", 0, 200, int(sw_default) if sw_default is not None else 0)
    # If user sets sw to 0, treat as "unset" unless they intentionally want 0
    sw_enabled = st.checkbox("Enable --sw", value=(preset.sw is not None or "sw" in fav_overrides))
    if not sw_enabled:
        sw_value_out = None
    else:
        sw_value_out = sw_value

    cw_enabled = st.checkbox("Enable --cw (only applies if --cref provided)", value=False)
    cw_value = st.slider("Character weight (--cw)", 0, 100, int(cw_default)) if cw_enabled else None

    iw_enabled = st.checkbox("Enable --iw (only applies if image prompt URLs provided)", value=False)
    iw_value = st.slider("Image weight (--iw)", 0.0, 3.0, float(iw_default), 0.1) if iw_enabled else None

    stylize_enabled = st.checkbox("Enable --stylize", value=False)
    stylize_value = st.slider("--stylize", 0, 1000, 100) if stylize_enabled else None

    extra_params = st.text_input("Extra params (raw)", value="")  # e.g., --ar 2:3 --seed 123

full_prompt, params_str = build_prompt_and_params(
    preset=preset,
    subject=subject,
    scene=scene,
    image_prompt_urls=image_prompt_urls,
    cref_urls=cref_urls,
    sref_value=sref_value.strip() if sref_value.strip() else None,
    sw_value=sw_value_out,
    cw_value=cw_value,
    iw_value=iw_value,
    stylize_value=stylize_value,
    extra_params=extra_params,
)

st.subheader("Output")
st.text_area("Full Prompt (copy/paste into Midjourney)", value=f"{full_prompt} {params_str}".strip(), height=140)

col1, col2 = st.columns(2)
with col1:
    st.text_area("Prompt only", value=full_prompt, height=120)
with col2:
    st.text_area("Params only", value=params_str, height=120)

st.caption("Workflow suggestion: Start with a preset → only touch --sw first → then add refs if needed.")
