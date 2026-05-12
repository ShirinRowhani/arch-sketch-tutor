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
    ["🏆 Play the 5-Level Course", "🎨 Playlist Hub & Tracing Library"], 
    horizontal=True
)

# --- DETAILED ARCHITECTURAL MASTER DRAWING (COMMON BACKGROUND LAYER) ---
# This builds a full, detailed cottage sketch in faint light gray (#D3D3D3)
cottage_bg = """
    <path d="M 100,140 L 220,100 L 220,240 L 100,220 Z" fill="none" stroke="#D3D3D3" stroke-width="2"/>
    <path d="M 220,130 L 320,110 L 320,200 L 220,220" fill="none" stroke="#D3D3D3" stroke-width="2"/>
    <path d="M 100,140 L 160,70 L 220,100" fill="none" stroke="#D3D3D3" stroke-width="2"/>
    <path d="M 160,70 L 260,50 L 320,110 L 220,100 Z" fill="none" stroke="#D3D3D3" stroke-width="2"/>
    <path d="M 250,75 L 250,35 L 275,32 L 275,68" fill="none" stroke="#D3D3D3" stroke-width="1.5"/>
    <rect x="246" y="30" width="33" height="6" fill="none" stroke="#D3D3D3" stroke-width="1.5"/>
    <path d="M 135,170 L 175,157 L 175,227 L 135,223 Z" fill="none" stroke="#D3D3D3" stroke-width="1.5"/>
    <path d="M 245,145 L 295,135 L 295,185 L 245,195 Z" fill="none" stroke="#D3D3D3" stroke-width="1.5"/>
    <path d="M 145,115 L 175,105 L 175,130 L 145,135 Z" fill="none" stroke="#D3D3D3" stroke-width="1"/>
"""

# --- MODE A: 5-LEVEL COURSE ---
if mode == "🏆 Play the 5-Level Course":
    
    # 5 Levels featuring Grayed background + bold custom highlighted dash lines
    lessons = {
        "Level 1: Structural Volumes (Wobbly Line Confidence)": {
            "timestamp": "06:29",
            "instructions": "Trace the primary 3D boxes of the house framework. Keep your pen lines intentionally loose and sketchy—no rulers!",
            "svg": f"""<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                {cottage_bg}
                <path d="M 100,140 L 220,100 L 220,240 L 100,220 Z" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="6,4"/>
                <path d="M 220,130 L 320,110 L 320,200 L 220,220" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="6,4"/>
            </svg>"""
        },
        "Level 2: Roof Planes & Angles": {
            "timestamp": "10:04",
            "instructions": "Practice matching structural roof slants. Focus on how parallel roof planes slant downward toward the same hidden vanishing points.",
            "svg": f"""<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                {cottage_bg}
                <path d="M 100,140 L 160,70 L 220,100 Z" fill="none" stroke="#00FFFF" stroke-width="4" stroke-dasharray="6,4"/>
                <path d="M 160,70 L 260,50 L 320,110 L 220,100 Z" fill="none" stroke="#00FFFF" stroke-width="4" stroke-dasharray="6,4"/>
            </svg>"""
        },
        "Level 3: The 6-Dot Proportions Method": {
            "timestamp": "19:50",
            "instructions": "Before drawing shapes, place these 6 critical boundary tracking dots on your physical paper to perfectly lock in your architecture scale.",
            "svg": f"""<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                {cottage_bg}
                <circle cx="160" cy="70" r="7" fill="#1f77b4"/><text x="156" y="74" fill="#fff" font-size="10" font-weight="bold">1</text>
                <circle cx="100" cy="220" r="7" fill="#1f77b4"/><text x="96" y="224" fill="#fff" font-size="10" font-weight="bold">2</text>
                <circle cx="220" cy="240" r="7" fill="#1f77b4"/><text x="216" y="244" fill="#fff" font-size="10" font-weight="bold">3</text>
                <circle cx="320" cy="200" r="7" fill="#1f77b4"/><text x="316" y="204" fill="#fff" font-size="10" font-weight="bold">4</text>
                <circle cx="100" cy="140" r="7" fill="#1f77b4"/><text x="96" y="144" fill="#fff" font-size="10" font-weight="bold">5</text>
                <circle cx="320" cy="110" r="7" fill="#1f77b4"/><text x="316" y="114" fill="#fff" font-size="10" font-weight="bold">6</text>
            </svg>"""
        },
        "Level 4: Windows & Doors Placement": {
            "timestamp": "20:54",
            "instructions": "Trace the structural window cavities and front entry archways. Make sure your vertical window lines stay perfectly upright.",
            "svg": f"""<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                {cottage_bg}
                <path d="M 135,170 L 175,157 L 175,227 L 135,223 Z" fill="none" stroke="#FF00FF" stroke-width="4" stroke-dasharray="5,3"/>
                <path d="M 245,145 L 295,135 L 295,185 L 245,195 Z" fill="none" stroke="#FF00FF" stroke-width="4" stroke-dasharray="5,3"/>
                <path d="M 145,115 L 175,105 L 175,130 L 145,135 Z" fill="none" stroke="#FF00FF" stroke-width="3" stroke-dasharray="5,3"/>
            </svg>"""
        },
        "Level 5: Shading, Textures & Details": {
            "timestamp": "21:28",
            "instructions": "Time for finishing details! Trace the chimney stack on the roof and add clean, parallel cross-hatching stroke paths for shadows.",
            "svg": f"""<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                {cottage_bg}
                <path d="M 250,75 L 250,35 L 275,32 L 275,68 Z" fill="none" stroke="#FFC300" stroke-width="3" stroke-dasharray="4,2"/>
                <line x1="110" y1="145" x2="110" y2="155" stroke="#FFC300" stroke-width="2"/>
                <line x1="125" y1="140" x2="125" y2="150" stroke="#FFC300" stroke-width="2"/>
                <line x1="140" y1="135" x2="140" y2="145" stroke="#FFC300" stroke-width="2"/>
                <line x1="155" y1="130" x2="155" y2="140" stroke="#FFC300" stroke-width="2"/>
                <line x1="235" y1="120" x2="235" y2="135" stroke="#FFC300" stroke-width="2"/>
                <line x1="255" y1="115" x2="255" y2="130" stroke="#FFC300" stroke-width="2"/>
            </svg>"""
        }
    }

    selected_level = st.selectbox("Select Your Lesson Level:", list(lessons.keys()))
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📺 Tutorial Video")
        st.video(st.session_state["course_video_url"])
        st.info(f"👉 Watch near **{lessons[selected_level]['timestamp']}**. {lessons[selected_level]['instructions']}")

    with col2:
        st.subheader("📱 Camera Tracing Overlays")
        opacity = st.slider("Template Transparency:", 0.0, 1.0, 0.6, 0.1)
        
        # FIXED CAMERA WRAPPER: object-fit: fill + user-action control locks elements perfectly together
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
        uploaded_image = st.file_uploader("Upload your physical sketch:", type=["jpg", "jpeg", "png"], key="course_upload")
        
        if uploaded_image and api_key and st.button("Submit Sketch for Feedback"):
            with st.spinner("The Professor is looking over your lines..."):
                try:
                    img = Image.open(uploaded_image)
                    prompt = f"Review this child's sketch for {selected_level}. Praise 2 features, point out 1 adjustment warmly. Keep it simple and encouraging."
                    model = genai.GenerativeModel("models/gemini-1.5-flash") # Explicit Model Path Fix applied
                    response = model.generate_content([prompt, img])
                    st.success("📝 Professor's Feedback:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error getting feedback: {e}")

# --- MODE B: PLAYLIST HUB & TRACING LIBRARY ---
else:
    st.subheader("🎬 Playlist Hub & Tracing Library")
    st.write("Browse Scottie's full playlist and choose a preset pattern or upload a custom tracking screenshot!")

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
        
        opacity = st.slider("Template Transparency:", 0.0, 1.0, 0.5, 0.1)

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
                overlay_html = '<div style="color:white; display:flex; align-items:center; justify-content:center; height:100%; border:2px dashed #444; border-radius:10px; margin: 10px;">Pause your video, snap a screenshot, and drop it here to trace!</div>'
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
