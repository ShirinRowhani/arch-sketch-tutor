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

# 3. SET UP GEMINI API 
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
            "instructions": """Practice loose, relaxed straight lines, squares, and overlapping circles. Do not use a ruler! Move your whole arm.""",
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
            "instructions": """Trace 4 examples of 1-Point perspective. Notice how all lines lead back to the center Vanishing Point (VP).""",
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
            "instructions": """Trace 4 structural blocks fanning outward to a distinct Left Vanishing Point (LVP) and Right Vanishing Point (RVP).""",
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
            "instructions": """Trace the broad outer frame silhouette envelope of the house layout before worrying about any windows or detail blocks.""",
            "svg": f"""<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                {cottage_base_gray}
                <path d="M 100,220 L 100,150 L 155,80 L 255,60 L 310,90 L 310,190 L 210,240 L 100,220" fill="none" stroke="#FF00FF" stroke-width="4" stroke-dasharray="6,4"/>
                <line x1="210" y1="110" x2="210" y2="240" stroke="#FF00FF" stroke-width="3" stroke-dasharray="6,4"/>
            </svg>"""
        },
        "Practice 5: Placing Proportion Reference Dots (19:03)": {
            "timestamp": "19:03",
            "instructions": """Before sketching lines, trace and place these 6 critical spatial dots to lock in the absolute height and perspective layout.""",
            "svg": f"""<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                {cottage_base_gray}
                <circle cx="155" cy="80" r="8" fill="#1f77b4"/><text x="151" y="84" fill="#fff" font-size="10" font-weight="bold">1</text>
                <circle cx="100" cy="220" r="8" fill="#1f77b4"/><text x="96" y="224" fill="#fff" font-size="10" font-weight="bold">2</text>
                <circle cx="210" cy="240" r="8" fill="#1f77b4"/><text x="206" y="244" fill="#fff" font-size="10" font-weight="bold">3</text>
                <circle cx="310" cy="190" r="8" fill="#1f77b4"/><text x="306" y="194" fill="#fff" font-size="10" font-weight="bold">4</text>
                <circle cx="100" cy="150" r="8" fill="#1f77b4"/><text x="96" y="154" fill="#fff" font-size="10" font-weight="bold">5</text>
                <circle cx="310" cy="90" r="8" fill="#1f77b4"/><text x="306" y="94" fill="#fff" font-size="10" font-weight="bold">6</text>
            </svg>"""
        },
        "Practice 6: Building Front & Subdivisions (19:38)": {
            "timestamp": "19:38",
            "instructions": """Trace the building's front facade profile and section layouts, transitioning cleanly from big primary wall frames down to smaller openings.""",
            "svg": f"""<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                {cottage_base_gray}
                <path d="M 100,150 L 210,110 L 210,240 L 100,220 Z" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="6,4"/>
                <path d="M 100,150 L 155,80 L 210,110" fill="none" stroke="#FF5733" stroke-width="3" stroke-dasharray="6,4"/>
                <path d="M 135,175 L 175,162 L 175,227 L 135,223 Z" fill="none" stroke="#00FFFF" stroke-width="3"/>
            </svg>"""
        },
        "Practice 7: Detailed Cottage Masterclass (19:55)": {
            "timestamp": "19:55",
            "instructions": """Trace the entire compound architectural silhouette—including side wing expansions, roofs, chimneys, and fine hatching texturing paths.""",
            "svg": f"""<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                {cottage_base_gray}
                <path d="M 100,150 L 210,110 L 310,90 L 310,190 L 210,240 L 100,220 Z" fill="none" stroke="#FF5733" stroke-width="3" stroke-dasharray="5,3"/>
                <path d="M 155,80 L 255,60 L 310,90" fill="none" stroke="#FF5733" stroke-width="3" stroke-dasharray="5,3"/>
                <path d="M 250,75 L 250,35 L 275,32 L 275,68 Z" fill="none" stroke="#FFC300" stroke-width="3.5"/>
                <path d="M 235,145 L 285,135 L 285,185 L 235,195 Z" fill="none" stroke="#00FFFF" stroke-width="2.5"/>
            </svg>"""
        }
    }

    selected_level = st.selectbox("Choose Active Practice Milestone:", list(lessons.keys()))
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📺 Instructor Video Feed")
        st.video(st.session_state["course_video_url"])
        st.info(f"⏱️ **Video Target Timestamp:** Fast-forward near **{lessons[selected_level]['timestamp']}**. \n\n🎯 **Instructions:** {lessons[selected_level]['instructions']}")

    with col2:
        st.subheader("📱 Camera Tracing Overlays")
        opacity = st.slider("Template Transparency:", 0.0, 1.0, 0.6, 0.1)
        
        camera_html = f"""
        <div style="position: relative; width: 100%; max-width: 500px; height: 375px; background-color: #000; border-radius: 10px; overflow: hidden; margin: auto; touch-action: none;">
            <video id="webcam" autoplay playsinline style="width:100%; height:100%; object-fit:fill; z-index:1; position:absolute; top:0; left:0;"></video>
            <div style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:{opacity}; z-index:10; pointer-events:none;">
                {lessons[selected_level]['svg']}
            </div>
        </div>
        <script>
            navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: "environment" }} }}).then(s => {{ document.getElementById('webcam').srcObject = s; }});
        </script>
        """
        components.html(camera_html, height=400)
        
        st.write("---")
        st.subheader("🤖 Critique From AI Professor")
        uploaded_image = st.file_uploader("Upload your drawn paper sketch:", type=["jpg", "jpeg", "png"], key="course_upload")
        
        if uploaded_image and api_key and st.button("Submit Sketch for Evaluation"):
            with st.spinner("The Professor is evaluating your linework..."):
                try:
                    img = Image.open(uploaded_image)
                    prompt = f"Review this child's architectural line drawing for {selected_level}. Praise two details warmly (confidence, sketchiness), and give one gentle tip for improvement."
                    model = genai.GenerativeModel("models/gemini-1.5-flash")
                    response = model.generate_content([prompt, img])
                    st.success("📝 Professor's Feedback:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error communicating with AI: {e}")

# --- MODE B: PLAYLIST HUB & TRACING LIBRARY ---
else:
    st.subheader("🎬 Playlist Hub & Tracing Library")
    st.write("Browse any video inside the active playlist window, or capture custom screenshots to match Scottie's frames perfectly!")

    col1, col2 = st.columns([1, 1])
    with col1:
        embed_url = f"https://www.youtube.com/embed/videoseries?list={st.session_state['playlist_id']}"
        components.html(
            f'<iframe width="100%" height="315" src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius:10px;"></iframe>',
            height=320
        )

    with col2:
        st.subheader("📱 Choose Your Tracing Template")
        library_choice = st.selectbox(
            "Select Library Template:",
            [
                "📸 [Custom Option] Upload Playlist Screenshot",
                "🏠 Library 1: Cozy Street Lamp",
                "🚪 Library 2: Classic Arched Doorway",
                "☕ Library 3: Cafe Window & Awning"
            ]
        )
        
        opacity = st.slider("Template Transparency:", 0.0, 1.0, 0.4, 0.1)

        library_svgs = {
            "🏠 Library 1: Cozy Street Lamp": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;"><line x1="50" y1="280" x2="350" y2="280" stroke="#FF5733" stroke-width="3"/><line x1="200" y1="280" x2="200" y2="100" stroke="#FF5733" stroke-width="4"/><rect x="140" y="120" width="60" height="40" rx="3" fill="none" stroke="#FFC300" stroke-width="2"/></svg>""",
            "🚪 Library 2: Classic Arched Doorway": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;"><path d="M 120,260 L 120,130 A 80,80 0 0,1 280,130 L 280,260" fill="none" stroke="#FF5733" stroke-width="4"/><path d="M 140,260 L 140,140 A 60,60 0 0,1 260,140 L 260,260" fill="none" stroke="#00FFFF" stroke-width="2.5"/></svg>""",
            "☕ Library 3: Cafe Window & Awning": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;"><rect x="130" y="110" width="140" height="130" fill="none" stroke="#FF5733" stroke-width="4"/><path d="M 110,110 L 130,60 L 270,60 L 290,110 Z" fill="none" stroke="#FFC300" stroke-width="3"/></svg>"""
        }

        overlay_html = ""
        if library_choice == "📸 [Custom Option] Upload Playlist Screenshot":
            custom_screenshot = st.file_uploader("📸 Upload Screenshot from any Playlist Video:", type=["jpg", "jpeg", "png"])
            if custom_screenshot:
                pil_img = Image.open(custom_screenshot)
                b64_img = get_image_base64(pil_img)
                overlay_html = f'<img src="{b64_img}" style="width:100%; height:100%; object-fit:fill; position:absolute; top:0; left:0;" />'
            else:
                overlay_html = '<div style="color:white; display:flex; align-items:center; justify-content:center; height:100%; border:2px dashed #444; border-radius:10px; margin: 10px;">Upload a video frame capture snapshot here to transform it into a live tracing template!</div>'
        else:
            overlay_html = library_svgs[library_choice]

        camera_html = f"""
        <div style="position: relative; width: 100%; max-width: 500px; height: 375px; background-color: #000; border-radius: 10px; overflow: hidden; margin: auto; touch-action: none;">
            <video id="webcam" autoplay playsinline style="width:100%; height:100%; object-fit:fill; z-index:1; position:absolute; top:0; left:0;"></video>
            <div style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:{opacity}; z-index:10; pointer-events:none;">
                {overlay_html}
            </div>
        </div>
        <script>
            navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: "environment" }} }}).then(s => {{ document.getElementById('webcam').srcObject = s; }});
        </script>
        """
        components.html(camera_html, height=400)

# --- 5. PARENT CONTROL PANEL ---
st.write("---")
with st.expander("⚙️ Parent Settings (Change Default Content Links)"):
    new_course_url = st.text_input("Course Mode Single Video Link:", value=st.session_state["course_video_url"])
    raw_playlist_input = st.text_input("Playlist ID or Playlist URL Link:", value=st.session_state["playlist_id"])
    extracted_id = raw_playlist_input.split("list=")[1].split("&")[0] if "list=" in raw_playlist_input else raw_playlist_input
    if st.button("Save New Default Links"):
        st.session_state["course_video_url"] = new_course_url
        st.session_state["playlist_id"] = extracted_id
        st.success("Links updated successfully!")
        st.rerun()
