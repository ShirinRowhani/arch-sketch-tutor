import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit.components.v1 as components
import base64
import io

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="AI Architecture Sketch Tutor", layout="wide")

# Helper to convert PIL image to base64 for custom overlays
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

# 4. INITIALIZE SESSION STATE FOR EDITABLE LINKS
if "course_video_url" not in st.session_state:
    # Default is the first Scottie video
    st.session_state["course_video_url"] = "https://youtu.be/yocInfqlYqw"

if "playlist_id" not in st.session_state:
    # Default is the 58-video playlist you provided
    st.session_state["playlist_id"] = "PL7oW-rwpz64J6PSsebDgsyElz6O99BkVq"

# 5. APP INTERFACE
st.title("🏡 Urban Sketching AI Studio")

# Studio Mode Selector
mode = st.radio(
    "Choose Your Studio Mode:", 
    ["🏆 Play the 5-Level Course", "🎨 Playlist Hub & Tracing Library"], 
    horizontal=True
)

# --- MODE A: 5-LEVEL COURSE ---
if mode == "🏆 Play the 5-Level Course":
    if "current_level" not in st.session_state:
        st.session_state["current_level"] = 1

    lessons = {
        1: {
            "title": "Level 1: The Wobbly Box & Circles",
            "timestamp": "06:29",
            "instructions": "Practice loose, wobbly lines with character. Avoid perfect straight edges. Draw overlapping wobbly circles.",
            "svg": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;"><path d="M 100,110 Q 95,180 100,220 Q 160,225 220,220 Q 225,180 220,110 Q 160,105 100,110" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="6,4"/><path d="M 100,110 Q 130,65 160,60 Q 220,65 220,110" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="6,4"/><path d="M 160,60 Q 165,130 160,175" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="6,4"/><circle cx="310" cy="140" r="45" fill="none" stroke="#FFC300" stroke-width="2" stroke-dasharray="4,2"/></svg>"""
        },
        2: {
            "title": "Level 2: Two-Point Perspective Box",
            "timestamp": "10:04",
            "instructions": "Draw your central vertical corner. Angle your top and bottom lines so they 'fan' toward your imaginary Left and Right Vanishing Points.",
            "svg": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;"><line x1="10" y1="130" x2="390" y2="130" stroke="#00FFFF" stroke-width="2"/><circle cx="40" cy="130" r="5" fill="#FF00FF"/><circle cx="360" cy="130" r="5" fill="#FF00FF"/><line x1="200" y1="80" x2="200" y2="220" stroke="#FF5733" stroke-width="4"/><line x1="200" y1="80" x2="40" y2="130" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/><line x1="200" y1="220" x2="40" y2="130" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/><line x1="200" y1="80" x2="360" y2="130" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/><line x1="200" y1="220" x2="360" y2="130" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/><line x1="110" y1="110" x2="110" y2="180" stroke="#FF5733" stroke-width="3"/><line x1="290" y1="100" x2="290" y2="190" stroke="#FF5733" stroke-width="3"/></svg>"""
        },
        3: {
            "title": "Level 3: The 6-Dot Proportions Method",
            "timestamp": "19:50",
            "instructions": "Place exactly 6 dots on your paper first to lock in the height, width, and perspective corners of the building structure.",
            "svg": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;"><circle cx="200" cy="50" r="8" fill="#1f77b4"/><circle cx="200" cy="240" r="8" fill="#1f77b4"/><circle cx="100" cy="120" r="8" fill="#1f77b4"/><circle cx="300" cy="110" r="8" fill="#1f77b4"/><circle cx="100" cy="200" r="8" fill="#1f77b4"/><circle cx="300" cy="190" r="8" fill="#1f77b4"/></svg>"""
        },
        4: {
            "title": "Level 4: The Cottage Silhouette",
            "timestamp": "20:54",
            "instructions": "Connect the structural points of your 6-dot grid to build the outline structure of the building. Keep your lines sketchy and loose.",
            "svg": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;"><path d="M 100,120 L 200,80 L 200,220 L 100,200 Z" fill="none" stroke="#FF5733" stroke-width="4"/><path d="M 200,110 L 300,90 L 300,180 L 200,200" fill="none" stroke="#FF5733" stroke-width="4"/><line x1="90" y1="124" x2="205" y2="78" stroke="#33FF57" stroke-width="3"/><line x1="200" y1="110" x2="310" y2="88" stroke="#33FF57" stroke-width="3"/></svg>"""
        },
        5: {
            "title": "Level 5: Architectural Details & Shading",
            "timestamp": "21:28",
            "instructions": "Place the doorway and window boxes. Add loose diagonal hatching lines to create shadow under the eaves and inside the doorway recess.",
            "svg": """<svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;"><path d="M 130,160 L 170,145 L 170,210 L 130,205 Z" fill="none" stroke="#FFC300" stroke-width="3"/><path d="M 115,130 L 140,120 L 140,150 L 115,155 Z" fill="none" stroke="#FFC300" stroke-width="2"/><path d="M 230,125 L 270,115 L 270,150 L 230,155 Z" fill="none" stroke="#FFC300" stroke-width="2"/></svg>"""
        }
    }

    current_lvl = st.session_state["current_level"]
    st.subheader(f"🏆 Active Level: {current_lvl} of 5 - {lessons[current_lvl]['title']}")
    st.progress(current_lvl / 5.0)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📺 Tutorial Video")
        # Uses the customizable course video link from session state
        st.video(st.session_state["course_video_url"])
        st.info(f"👉 Play video near timestamp **{lessons[current_lvl]['timestamp']}**. {lessons[current_lvl]['instructions']}")
        if st.button("Reset Course to Level 1"):
            st.session_state["current_level"] = 1
            st.rerun()

    with col2:
        st.subheader("📱 Camera Tracing Overlays")
        opacity = st.slider("Template Transparency:", 0.0, 1.0, 0.5, 0.1)
        
        camera_html = f"""
        <div style="position: relative; width: 100%; max-width: 500px; aspect-ratio: 4/3; background-color: #000; border-radius: 10px; overflow: hidden; margin: auto;">
            <video id="webcam" autoplay playsinline style="width:100%; height:100%; object-fit:cover; z-index:1; position:absolute; top:0; left:0;"></video>
            <div style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:{opacity}; z-index:10; pointer-events:none;">
                {lessons[current_lvl]['svg']}
            </div>
        </div>
        <script>
            navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: "environment" }} }}).then(s => {{ document.getElementById('webcam').srcObject = s; }});
        </script>
        """
        components.html(camera_html, height=400)
        
        st.write("---")
        st.subheader("🤖 Critique and Level Up")
        uploaded_image = st.file_uploader("Upload your physical sketch:", type=["jpg", "jpeg", "png"], key="course_upload")
        
        if uploaded_image and api_key and st.button("Submit Sketch for Level Up"):
            with st.spinner("The Professor is looking over your lines..."):
                img = Image.open(uploaded_image)
                prompt = f"Review this child's sketch for {lessons[current_lvl]['title']}. Praise 2 features, point out 1 adjustment warmly. End your output with exact phrase [PASS] if it's a genuine effort, or [RETRY]."
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([prompt, img])
                text = response.text
                st.write(text.replace("[PASS]", "").replace("[RETRY]", ""))
                if "[PASS]" in text:
                    st.balloons()
                    if current_lvl < 5:
                        st.session_state["current_level"] += 1
                        st.success("🎉 unlocked next level!")
                        st.button("Continue to Next Level 🚀", on_click=st.rerun)
                    else:
                        st.success("🎓 You graduated!")

# --- MODE B: PLAYLIST HUB & TRACING LIBRARY ---
else:
    st.subheader("🎬 Playlist Hub & Tracing Library")
    st.write("Browse the active playlist and select a pre-coded tracing overlay or upload your own!")

    col1, col2 = st.columns([1, 1])

    with col1:
        # Dynamic playlist embed using the ID stored in session state
        embed_url = f"https://www.youtube.com/embed/videoseries?list={st.session_state['playlist_id']}"
        
        components.html(
            f'<iframe width="100%" height="315" src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius:10px;"></iframe>',
            height=320
        )
        st.info("💡 **Tip:** Click the playlist icon in the top-right corner of the video player above to select a video tutorial!")

    with col2:
        st.subheader("📱 Choose Your Tracing Template")
        
        library_choice = st.selectbox(
            "Select Library Template:",
            [
                "🏠 Library 1: Cozy Street Lamp",
                "🚪 Library 2: Classic Arched Doorway",
                "☕ Library 3: Cafe Window & Awning",
                "🧱 Library 4: Chimney & Roof Shingles",
                "🌳 Library 5: Architectural Trees & Shrub",
                "📸 [Custom Option] Upload My Own Screenshot"
            ]
        )
        
        opacity = st.slider("Template Transparency:", 0.0, 1.0, 0.5, 0.1)

        library_svgs = {
            "🏠 Library 1: Cozy Street Lamp": """
                <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                    <line x1="50" y1="280" x2="350" y2="280" stroke="#FF5733" stroke-width="3"/>
                    <line x1="200" y1="280" x2="200" y2="100" stroke="#FF5733" stroke-width="4"/>
                    <path d="M 185,280 L 200,250 L 215,280 Z" fill="none" stroke="#FF5733" stroke-width="3"/>
                    <path d="M 200,100 Q 230,80 230,110" fill="none" stroke="#FF5733" stroke-width="3"/>
                    <path d="M 215,110 L 245,110 L 235,150 L 225,150 Z" fill="none" stroke="#FF5733" stroke-width="3"/>
                    <line x1="230" y1="110" x2="230" y2="150" stroke="#FF5733" stroke-dasharray="3,3"/>
                    <rect x="140" y="120" width="60" height="40" rx="3" fill="none" stroke="#FFC300" stroke-width="2"/>
                    <line x1="160" y1="120" x2="160" y2="160" stroke="#FFC300" stroke-width="1.5"/>
                </svg>
            """,
            "🚪 Library 2: Classic Arched Doorway": """
                <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                    <path d="M 120,260 L 120,130 A 80,80 0 0,1 280,130 L 280,260" fill="none" stroke="#FF5733" stroke-width="4"/>
                    <path d="M 140,260 L 140,140 A 60,60 0 0,1 260,140 L 260,260" fill="none" stroke="#00FFFF" stroke-width="2.5"/>
                    <line x1="200" y1="80" x2="200" y2="260" stroke="#00FFFF" stroke-width="2"/>
                    <line x1="200" y1="80" x2="200" y2="50" stroke="#FF5733" stroke-width="3"/>
                    <line x1="140" y1="140" x2="115" y2="130" stroke="#FF5733" stroke-width="3"/>
                    <line x1="260" y1="140" x2="285" y2="130" stroke="#FF5733" stroke-width="3"/>
                    <circle cx="190" cy="200" r="4" fill="#FFC300"/>
                    <circle cx="210" cy="200" r="4" fill="#FFC300"/>
                </svg>
            """,
            "☕ Library 3: Cafe Window & Awning": """
                <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                    <rect x="130" y="110" width="140" height="130" fill="none" stroke="#FF5733" stroke-width="4"/>
                    <line x1="200" y1="110" x2="200" y2="240" stroke="#FF5733" stroke-width="2"/>
                    <line x1="130" y1="170" x2="270" y2="170" stroke="#FF5733" stroke-width="2"/>
                    <path d="M 110,110 L 130,60 L 270,60 L 290,110 Z" fill="none" stroke="#FFC300" stroke-width="3"/>
                    <line x1="150" y1="60" x2="150" y2="110" stroke="#FFC300" stroke-dasharray="3,3"/>
                    <line x1="200" y1="60" x2="200" y2="110" stroke="#FFC300" stroke-dasharray="3,3"/>
                    <line x1="250" y1="60" x2="250" y2="110" stroke="#FFC300" stroke-dasharray="3,3"/>
                </svg>
            """,
            "🧱 Library 4: Chimney & Roof Shingles": """
                <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                    <line x1="50" y1="220" x2="350" y2="100" stroke="#FF5733" stroke-width="4"/>
                    <path d="M 230,148 L 230,70 L 280,70 L 280,128" fill="none" stroke="#FFC300" stroke-width="3"/>
                    <rect x="223" y="60" width="64" height="10" fill="none" stroke="#FFC300" stroke-width="3"/>
                    <line x1="230" y1="90" x2="280" y2="90" stroke="#FFC300" stroke-width="1.5"/>
                    <line x1="230" y1="110" x2="280" y2="110" stroke="#FFC300" stroke-width="1.5"/>
                    <path d="M 80,210 Q 90,205 100,210 Q 110,205 120,210" fill="none" stroke="#FF5733" stroke-width="1.5"/>
                    <path d="M 150,180 Q 160,175 170,180 Q 180,175 190,180" fill="none" stroke="#FF5733" stroke-width="1.5"/>
                </svg>
            """,
            "🌳 Library 5: Architectural Trees & Shrub": """
                <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                    <path d="M 150,260 Q 155,180 140,150 Q 160,180 160,260" fill="none" stroke="#FF5733" stroke-width="4"/>
                    <path d="M 100,140 Q 80,100 120,80 Q 160,50 180,90 Q 220,100 190,140 Q 150,170 100,140 Z" fill="none" stroke="#33FF57" stroke-width="3" stroke-dasharray="4,2"/>
                    <path d="M 250,260 Q 230,230 260,210 Q 290,190 310,220 Q 330,240 310,260 Z" fill="none" stroke="#33FF57" stroke-width="2.5"/>
                </svg>
            """
        }

        overlay_html = ""
        
        # Keep both the pre-coded library AND the screenshot upload option!
        if library_choice != "📸 [Custom Option] Upload My Own Screenshot":
            overlay_html = library_svgs[library_choice]
        else:
            custom_screenshot = st.file_uploader("📸 Upload Screenshot to Use as Tracing Template:", type=["jpg", "jpeg", "png"])
            if custom_screenshot:
                pil_img = Image.open(custom_screenshot)
                b64_img = get_image_base64(pil_img)
                overlay_html = f'<img src="{b64_img}" style="width:100%; height:100%; object-fit:contain; position:absolute; top:0; left:0;" />'
            else:
                overlay_html = '<div style="color:white; display:flex; align-items:center; justify-content:center; height:100%; border:2px dashed #444; border-radius:10px; margin: 10px;">Upload a screenshot to project overlay here</div>'

        # Live WebRTC video feed
        camera_html = f"""
        <div style="position: relative; width: 100%; max-width: 500px; aspect-ratio: 4/3; background-color: #000; border-radius: 10px; overflow: hidden; margin: auto;">
            <video id="webcam" autoplay playsinline style="width:100%; height:100%; object-fit:cover; z-index:1; position:absolute; top:0; left:0;"></video>
            <div style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:{opacity}; z-index:10; pointer-events:none;">
                {overlay_html}
            </div>
        </div>
        <script>
            navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: "environment" }} }}).then(s => {{ document.getElementById('webcam').srcObject = s; }});
        </script>
        """
        components.html(camera_html, height=400)
        
        st.write("---")
        st.subheader("🤖 Custom AI Critique")
        user_drawing = st.file_uploader("Upload your drawn paper sketch:", type=["jpg", "jpeg", "png"])
        
        if user_drawing and api_key and st.button("Ask Professor to Evaluate"):
            with st.spinner("Analyzing your drawing style..."):
                drawing_img = Image.open(user_drawing)
                
                prompt = f"""
                You are a supportive, warm architecture professor and sketching artist tutoring a child.
                They have drawn physical lines corresponding to: "{library_choice}".
                
                Please review their drawing:
                - Highlight two things they did exceptionally well (like confidence of wobbly lines or nice details).
                - Give one tiny, warm suggestion for their next drawing.
                - Keep the tone incredibly fun, simple, and encouraging for a child.
                """
                
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([prompt, drawing_img])
                st.success("📝 Professor's Feedback:")
                st.markdown(response.text)

# --- 7. PARENT CONTROL PANEL ---
st.write("---")
with st.expander("⚙️ Parent Settings (Change Videos and Playlists)"):
    st.write("Modify the default video or playlist loaded into the studio below. These updates will apply instantly!")
    
    # 1. Edit Course Video Link
    new_course_url = st.text_input(
        "Course Mode Video URL:", 
        value=st.session_state["course_video_url"]
    )
    
    # 2. Edit Playlist ID (extracts the ID if they paste a full link)
    raw_playlist_input = st.text_input(
        "Playlist Hub Link or Playlist ID:", 
        value=st.session_state["playlist_id"]
    )
    
    # Simple extraction logic in case they paste a whole URL
    extracted_playlist_id = raw_playlist_input
    if "list=" in raw_playlist_input:
        extracted_playlist_id = raw_playlist_input.split("list=")[1].split("&")[0]
        
    if st.button("Apply New Video Links"):
        st.session_state["course_video_url"] = new_course_url
        st.session_state["playlist_id"] = extracted_playlist_id
        st.success("Settings saved successfully! Loading updated videos...")
        st.rerun()
