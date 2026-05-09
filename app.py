import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="AI Architecture Sketch Tutor", layout="wide")

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

# 4. GAME PROGRESSION STATE
if "current_level" not in st.session_state:
    st.session_state["current_level"] = 1

# Lesson Database
lessons = {
    1: {
        "title": "Level 1: The Wobbly Box & Circles",
        "timestamp": "06:29",
        "instructions": "Practice loose, wobbly lines with character. Avoid perfect straight edges. Average out a wobbly circle by drawing several overlapping strokes.",
        "svg": """
            <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                <path d="M 100,110 Q 95,180 100,220 Q 160,225 220,220 Q 225,180 220,110 Q 160,105 100,110" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="6,4"/>
                <path d="M 100,110 Q 130,65 160,60 Q 220,65 220,110" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="6,4"/>
                <path d="M 160,60 Q 165,130 160,175" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="6,4"/>
                <circle cx="310" cy="140" r="45" fill="none" stroke="#FFC300" stroke-width="2" stroke-dasharray="4,2"/>
                <path d="M 260,140 C 260,90 350,90 355,140 C 350,190 270,195 260,140" fill="none" stroke="#FFC300" stroke-width="2"/>
            </svg>
        """
    },
    2: {
        "title": "Level 2: Two-Point Perspective Box",
        "timestamp": "10:04",
        "instructions": "Draw the main vertical edge closest to you. Then, angle your top and bottom lines so they 'fan out' toward your imaginary Left and Right Vanishing Points on your Eye Line.",
        "svg": """
            <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                <line x1="10" y1="130" x2="390" y2="130" stroke="#00FFFF" stroke-width="2"/>
                <text x="15" y="120" fill="#00FFFF" font-size="10">EYE LINE / HORIZON</text>
                <circle cx="40" cy="130" r="5" fill="#FF00FF"/>
                <text x="30" y="150" fill="#FF00FF" font-size="10">LVP</text>
                <circle cx="360" cy="130" r="5" fill="#FF00FF"/>
                <text x="350" y="150" fill="#FF00FF" font-size="10">RVP</text>
                <line x1="200" y1="80" x2="200" y2="220" stroke="#FF5733" stroke-width="4"/>
                <line x1="200" y1="80" x2="40" y2="130" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/>
                <line x1="200" y1="220" x2="40" y2="130" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/>
                <line x1="200" y1="80" x2="360" y2="130" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/>
                <line x1="200" y1="220" x2="360" y2="130" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/>
                <line x1="110" y1="110" x2="110" y2="180" stroke="#FF5733" stroke-width="3"/>
                <line x1="290" y1="100" x2="290" y2="190" stroke="#FF5733" stroke-width="3"/>
            </svg>
        """
    },
    3: {
        "title": "Level 3: The 6-Dot Proportions Method",
        "timestamp": "19:50",
        "instructions": "Place exactly 6 dots on your paper first: High/Low points, and the left/right outer corners. This locks in the proportion before drawing the walls.",
        "svg": """
            <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                <circle cx="200" cy="50" r="8" fill="#1f77b4"/>
                <text x="195" y="54" fill="#fff" font-size="12" font-weight="bold">1</text>
                <text x="215" y="55" fill="#1f77b4" font-size="12">Peak Roof</text>
                
                <circle cx="200" cy="240" r="8" fill="#1f77b4"/>
                <text x="195" y="244" fill="#fff" font-size="12" font-weight="bold">2</text>
                <text x="215" y="245" fill="#1f77b4" font-size="12">Base Corner</text>
                
                <circle cx="100" cy="120" r="8" fill="#1f77b4"/>
                <text x="96" y="124" fill="#fff" font-size="12" font-weight="bold">3</text>
                <text x="50" y="125" fill="#1f77b4" font-size="12">Left Wall</text>
                
                <circle cx="300" cy="110" r="8" fill="#1f77b4"/>
                <text x="296" y="114" fill="#fff" font-size="12" font-weight="bold">4</text>
                <text x="315" y="115" fill="#1f77b4" font-size="12">Right Wall</text>
                
                <circle cx="100" cy="200" r="8" fill="#1f77b4"/>
                <text x="96" y="204" fill="#fff" font-size="12" font-weight="bold">5</text>
                
                <circle cx="300" cy="190" r="8" fill="#1f77b4"/>
                <text x="296" y="194" fill="#fff" font-size="12" font-weight="bold">6</text>
            </svg>
        """
    },
    4: {
        "title": "Level 4: The Cottage Silhouette",
        "timestamp": "20:54",
        "instructions": "Connect the structural points of your 6-dot grid to build the outline structure of the building. Keep your lines sketchy and loose.",
        "svg": """
            <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                <path d="M 100,120 L 200,80 L 200,220 L 100,200 Z" fill="none" stroke="#FF5733" stroke-width="4"/>
                <path d="M 200,110 L 300,90 L 300,180 L 200,200" fill="none" stroke="#FF5733" stroke-width="4"/>
                <line x1="90" y1="124" x2="205" y2="78" stroke="#33FF57" stroke-width="3"/>
                <line x1="200" y1="110" x2="310" y2="88" stroke="#33FF57" stroke-width="3"/>
            </svg>
        """
    },
    5: {
        "title": "Level 5: Architectural Details & Shading",
        "timestamp": "21:28",
        "instructions": "Place the doorway and window boxes. Add loose diagonal hatching lines to create shadow under the eaves and inside the doorway recess.",
        "svg": """
            <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0; z-index:10; pointer-events:none;">
                <path d="M 130,160 L 170,145 L 170,210 L 130,205 Z" fill="none" stroke="#FFC300" stroke-width="3"/>
                <path d="M 115,130 L 140,120 L 140,150 L 115,155 Z" fill="none" stroke="#FFC300" stroke-width="2"/>
                <path d="M 230,125 L 270,115 L 270,150 L 230,155 Z" fill="none" stroke="#FFC300" stroke-width="2"/>
                <line x1="105" y1="120" x2="115" y2="135" stroke="#888" stroke-width="1.5"/>
                <line x1="120" y1="115" x2="130" y2="130" stroke="#888" stroke-width="1.5"/>
                <line x1="135" y1="110" x2="145" y2="125" stroke="#888" stroke-width="1.5"/>
                <line x1="150" y1="105" x2="160" y2="120" stroke="#888" stroke-width="1.5"/>
                <line x1="135" y1="165" x2="145" y2="185" stroke="#888" stroke-width="1.5"/>
                <line x1="145" y1="160" x2="155" y2="180" stroke="#888" stroke-width="1.5"/>
            </svg>
        """
    }
}

# 5. HEADER INFORMATION
current_lvl = st.session_state["current_level"]
st.subheader(f"🏆 Active Studio Level: {current_lvl} of 5")
st.progress(current_lvl / 5.0)

col1, col2 = st.columns([1, 1])

# --- LEFT COLUMN: YouTube Lessons & Active Info ---
with col1:
    st.subheader("📺 Instructor Video Feed")
    st.video("https://youtu.be/yocInfqlYqw")
    
    st.markdown(f"""
    ### ✏️ Current Objective: {lessons[current_lvl]['title']}
    * **Video Timestamp:** Play and watch around **{lessons[current_lvl]['timestamp']}**.
    * **Instructions:** {lessons[current_lvl]['instructions']}
    """)
    
    # Dev bypass / Reset game
    if st.button("Reset Game to Level 1", type="secondary"):
        st.session_state["current_level"] = 1
        st.rerun()

# --- RIGHT COLUMN: AR Tracing Camera ---
with col2:
    st.subheader("📱 AR Tracing Camera")
    st.write("Place your phone in the stand, look at the screen, and trace the guidelines on your physical paper!")

    opacity = st.slider("Template Transparency:", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    # Clean template rendering
    current_template = lessons[current_lvl]["svg"]

    camera_html = f"""
    <div style="position: relative; width: 100%; max-width: 500px; aspect-ratio: 4/3; background-color: #000; border-radius: 10px; overflow: hidden; margin: auto;">
        <video id="webcam" autoplay playsinline style="width: 100%; height: 100%; object-fit: cover; z-index: 1; position: absolute; top:0; left:0;"></video>
        <div id="svg-overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; opacity: {opacity}; z-index: 10;">
            {current_template}
        </div>
    </div>
    
    <script>
        const video = document.getElementById('webcam');
        navigator.mediaDevices.getUserMedia({{ 
            video: {{ facingMode: "environment" }} 
        }})
        .then(stream => {{
            video.srcObject = stream;
        }})
        .catch(err => {{
            console.error("Camera access error: ", err);
            navigator.mediaDevices.getUserMedia({{ video: true }})
            .then(stream => {{ video.srcObject = stream; }});
        }});
    </script>
    """
    
    components.html(camera_html, height=400)
    
    st.write("---")
    st.write("### 🤖 Level Evaluation & Unlock")
    st.write("Ready to advance? Take a photo of your paper sketch, upload it below, and let the AI Professor check your work!")
    
    uploaded_image = st.file_uploader("Upload a photo of your sketch:", type=["jpg", "jpeg", "png"], key=f"upload_lvl_{current_lvl}")
    
    if uploaded_image and api_key:
        if st.button("Submit Sketch to AI Professor"):
            with st.spinner("The Professor is reviewing your lines..."):
                try:
                    img = Image.open(uploaded_image)
                    prompt = f"""
                    You are a friendly, encouraging professional urban sketching artist and architecture tutor.
                    A student has just completed {lessons[current_lvl]['title']}.
                    Here is a photo of their physical sketch on paper.
                    
                    Please review their drawing and write a brief critique:
                    1. Praise two specific details they did beautifully (like their loose line quality, attempt at perspective, or confidence).
                    2. Point out one small, helpful thing they can adjust or keep in mind for the next level.
                    3. Keep your language warm, constructive, and simple enough for a young student. Use bullet points for easy reading.
                    
                    CRITICAL INSTRUCTION:
                    If the sketch shows a genuine, brave attempt at the task (even if wobbly, loose, or imperfect, since we embrace mistakes!), end your critique with the exact word [PASS].
                    If the image is not a sketch or completely missed the lesson concept, end your critique with the exact word [RETRY].
                    """
                    
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content([prompt, img])
                    feedback_text = response.text
                    
                    # Clean up and display feedback
                    display_text = feedback_text.replace("[PASS]", "").replace("[RETRY]", "")
                    st.success("📝 Professor's Feedback:")
                    st.markdown(display_text)
                    
                    if "[PASS]" in feedback_text:
                        st.balloons()
                        if current_lvl < 5:
                            st.session_state["current_level"] += 1
                            st.success(f"🎉 LEVEL COMPLETE! You've unlocked {lessons[current_lvl + 1]['title']}!")
                            st.button("Advance to Next Level 🚀", on_click=st.rerun)
                        else:
                            st.success("🎓 CONGRATULATIONS! You have graduated from the AI Urban Sketching Studio! You are officially an Urban Sketcher!")
                    else:
                        st.warning("⚠️ Great effort! The Professor wants you to touch up your lines a tiny bit and try uploading again to unlock the next level!")
                        
                except Exception as e:
                    st.error(f"Error calling the AI model: {e}")
