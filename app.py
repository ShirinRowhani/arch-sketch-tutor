import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit.components.v1 as components
import base64
import io

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="AI Architecture Sketch Tutor", layout="wide")

# Helper to convert PIL image to base64 for custom screenshot overlays
def get_image_base64(pil_img):
    buffered = io.BytesIO()
    pil_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# 2. PASSWORD PROTECTION
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    if st.session_state["authenticated"]:
        return True
    
    st.markdown("<h2 style='text-align: center;'>🔒 Architect Studio Login</h2>", unsafe_allow_html=True)
    cols = st.columns([1, 2, 1])
    with cols[1]:
        correct_password = st.secrets.get("app_password", "sketch2026")
        user_password = st.text_input("Enter Student Password:", type="password")
        if st.button("Unlock Studio", use_container_width=True):
            if user_password == correct_password:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect Password! Please try again.")
    return False

if not check_password():
    st.stop()

# 3. SET UP GEMINI API (Fixed with explicit pathing models/prefix)
api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("⚠️ Gemini API key is missing. The critique feature will be disabled.")

if "course_video_url" not in st.session_state:
    st.session_state["course_video_url"] = "https://youtu.be/yocInfqlYqw"
if "playlist_id" not in st.session_state:
    st.session_state["playlist_id"] = "PL7oW-rwpz64J6PSsebDgsyElz6O99BkVq"

# 4. APP INTERFACE
st.title("🏡 Urban Sketching AI Studio")

mode = st.radio(
    "Choose Your Studio Mode:", 
    ["🏆 Play the 7-Level Course", "🎨 Playlist Hub & Tracing Library"], 
    horizontal=True
)

# --- REUSABLE ARCHITECTURAL LAYERS FOR THE ADVANCED COTTAGE STEPS ---
cottage_base_gray = """
    <path d="M 100,150 L 210,110 L 210,240 L 100,220 Z" fill="none" stroke="#D3D3D3" stroke-width="2"/>
    <path d="M 210,110 L 310,90 L 310,190 L 210,240" fill="none" stroke="#D3D3D3" stroke-width="2"/>
    <path d="M 100,150 L 155,80 L 210,110" fill="none" stroke="#D3D3D3" stroke-width="2"/>
    <path d="M 155,80 L 255,60 L 310,90" fill="none" stroke="#D3D3D3" stroke-width="2"/>
    <path d="M 250,75 L 250,35 L 275,32 L 275,68" fill="none" stroke="#D3D3D3" stroke-width="1.5"/>
    <rect x="246" y="30" width="30" height="5" fill="none" stroke="#D3D3D3" stroke-width="1.5"/>
    <path d="M 135,175 L 175,162 L 175,227 L 135,223 Z" fill="none" stroke="#D3D3D3" stroke-width="1.5"/>
    <path d="M 235,145 L 285,135 L 285,185 L 235,195 Z" fill="none" stroke="#D3D3D3" stroke-width="1.5"/>
    <path d="M 145,120 L 175,110 L 175,135 L 145,140 Z" fill="none" stroke="#D3D3D3" stroke-width="1"/>
"""

# --- MODE A: 7-LEVEL COURSE MATCHING TIMESTAMPS ---
if mode == "🏆 Play the 7-Level Course":
    
    lessons = {
        "Practice 1: Linework Basics (04:43)": {
            "timestamp": "04:43",
            "instructions": "Practice loose, relaxed straight lines, squares, and overlapping circles. Do not use a ruler! Move your whole arm.",
            "svg": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                <line x1="40" y1="50" x2="160" y2="50" stroke="#FF5733" stroke-width="3" stroke-dasharray="6,4"/>
                <line x1="40" y1="70" x2="160" y2="70" stroke="#FF5733" stroke-width="3" stroke-dasharray="6,4"/>
                <line x1="40" y1="90" x2="160" y2="90" stroke="#FF5733" stroke-width="3" stroke-dasharray="6,4"/>
                <rect x="230" y="40" width="50" height="50" fill="none" stroke="#FF5733" stroke-width="3" stroke-dasharray="5,4"/>
                <rect x="300" y="40" width="50" height="50" fill="none" stroke="#FF5733" stroke-width="3" stroke-dasharray="5,4"/>
                <circle cx="100" cy="190" r="40" fill="none" stroke="#00FFFF" stroke-width="2.5" stroke-dasharray="4,2"/>
                <circle cx="270" cy="190" r="35" fill="none" stroke="#00FFFF" stroke-width="2.5" stroke-dasharray="4,2"/>
            </svg>"""
        },
        "Practice 2: 1-Point Perspective (07:37)": {
            "timestamp": "07:37",
            "instructions": "Trace 4 examples of 1-Point perspective. Notice how all lines lead back to the center Vanishing Point (VP).",
            "svg": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                <line x1="20" y1="150" x2="380" y2="150" stroke="#D3D3D3" stroke-width="2"/>
                <circle cx="200" cy="150" r="5" fill="#FF00FF"/>
                <rect x="40" y="40" width="50" height="40" fill="none" stroke="#FF5733" stroke-width="3" stroke-dasharray="5,3"/>
                <line x1="90" y1="80" x2="200" y2="150" stroke="#00FFFF" stroke-width="1.5" stroke-dasharray="3,3"/>
                
                <rect x="300" y="40" width="50" height="40" fill="none" stroke="#FF5733" stroke-width="3" stroke-dasharray="5,3"/>
                <line x1="300" y1="80" x2="200" y2="150" stroke="#00FFFF" stroke-width="1.5" stroke-dasharray="3,3"/>
                
                <rect x="40" y="220" width="50" height="40" fill="none" stroke="#FF5733" stroke-width="3" stroke-dasharray="5,3"/>
                <line x1="90" y1="220" x2="200" y2="150" stroke="#00FFFF" stroke-width="1.5" stroke-dasharray="3,3"/>
                
                <rect x="300" y="220" width="50" height="40" fill="none" stroke="#FF5733" stroke-width="3" stroke-dasharray="5,3"/>
                <line x1="300" y1="220" x2="200" y2="150" stroke="#00FFFF" stroke-width="1.5" stroke-dasharray="3,3"/>
            </svg>"""
        },
        "Practice 3: 2-Point Perspective (07:42)": {
            "timestamp": "07:42",
            "instructions": "Trace 4 structural blocks fanning outward to a distinct Left Vanishing Point (LVP) and Right Vanishing Point (RVP).",
            "svg": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                <line x1="10" y1="140" x2="390" y2="140" stroke="#D3D3D3" stroke-width="1.5"/>
                <circle cx="30" cy="140" r="4" fill="#FF00FF"/><circle cx="370" cy="140" r="4" fill="#FF00FF"/>
                <line x1="200" y1="40" x2="200" y2="90" stroke="#FF5733" stroke-width="3"/>
                <line x1="200" y1="40" x2="30" y2="140" stroke="#00FFFF" stroke-width="1.5" stroke-dasharray="4,2"/>
                <line x1="200" y1="40" x2="370" y2="140" stroke="#00FFFF" stroke-width="1.5" stroke-dasharray="4,2"/>
                <line x1="100" y1="180" x2="100" y2="240" stroke="#FF5733" stroke-width="3"/>
                <line x1="100" y1="180" x2="30" y2="140" stroke="#00FFFF" stroke-width="1.5" stroke-dasharray="4,2"/>
                <line x1="100" y1="180" x2="370" y2="140" stroke="#00FFFF" stroke-width="1.5" stroke-dasharray="4,2"/>
                <path d="M 280,160 L 320,150 L 320,210 L 280,225 Z" fill="none" stroke="#FF5733" stroke-width="2" stroke-dasharray="4,2"/>
                <path d="M 280,160 L 250,152 L 250,210 L 280,225 Z" fill="none" stroke="#FF5733" stroke-width="2" stroke-dasharray="4,2"/>
            </svg>"""
        },
        "Practice 4: Framing & Silhouette Outlines (18:34)": {
            "timestamp": "18:34",
            "instructions": "Trace the
