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
        # Looks for 'password' in Streamlit Secrets. If not set yet, defaults to 'sketch2026'
        correct_password = st.secrets.get("app_password", "sketch2026")
        user_password = st.text_input("Enter Student Password:", type="password")
        if st.button("Unlock Studio", use_container_width=True):
            if user_password == correct_password:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect Password! Please try again.")
    return False

# Stop execution if not logged in
if not check_password():
    st.stop()

# 3. SET UP GEMINI API
# Retrieves the key securely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("⚠️ Gemini API key is missing. The critique feature will be disabled until you add it in Streamlit Secrets.")

# 4. APP INTERFACE (Once logged in)
st.title("🏡 Urban Sketching AI Studio")
st.write("Follow the video tutorial on the left, and use your phone to trace or check your progress on the right!")

col1, col2 = st.columns([1, 1])

# --- LEFT COLUMN: YouTube Lessons ---
with col1:
    st.subheader("📺 Tutorial Video")
    # Embedded Sketching Scottie tutorial
    st.video("https://youtu.be/yocInfqlYqw")
    
    st.markdown("""
    ### 🎯 Today's Lessons & Milestones:
    * **Lesson 1: The Wobbly Box (06:29)** - Practice loose, confident lines. Do not use a ruler!
    * **Lesson 2: Two-Point Perspective Box (10:04)** - Learn to align angles toward imaginary vanishing points on your eye-line.
    """)

# --- RIGHT COLUMN: AR Tracing & Capture ---
with col2:
    st.subheader("📱 AR Tracing Camera")
    
    # Lesson selector to update the overlay
    lesson = st.selectbox(
        "Choose Your Tracing Template:",
        ["Lesson 1: The Wobbly Box", "Lesson 2: Two-Point Perspective"]
    )
    
    # Preset SVG outlines for tracing to avoid manual scraping!
    templates = {
        "Lesson 1: The Wobbly Box": """
            <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0;">
                <path d="M 120,100 Q 115,180 120,220 Q 180,225 240,220 Q 245,180 240,100 Q 180,95 120,100" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="5,5"/>
                <path d="M 120,100 Q 150,55 180,50 Q 240,55 240,100" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="5,5"/>
                <path d="M 180,50 Q 185,120 180,170" fill="none" stroke="#FF5733" stroke-width="4" stroke-dasharray="5,5"/>
                <line x1="120" y1="100" x2="350" y2="150" stroke="#00FF00" stroke-width="1.5" stroke-dasharray="2,2"/>
                <line x1="240" y1="100" x2="350" y2="150" stroke="#00FF00" stroke-width="1.5" stroke-dasharray="2,2"/>
            </svg>
        """,
        "Lesson 2: Two-Point Perspective": """
            <svg viewBox="0 0 400 300" style="width:100%; height:100%; position:absolute; top:0; left:0;">
                <line x1="10" y1="150" x2="390" y2="150" stroke="#00FFFF" stroke-width="2"/>
                <text x="15" y="140" fill="#00FFFF" font-size="12">EYE LINE / HORIZON</text>
                <circle cx="40" cy="150" r="5" fill="#FF00FF"/>
                <text x="30" y="170" fill="#FF00FF" font-size="10">LVP</text>
                <circle cx="360" cy="150" r="5" fill="#FF00FF"/>
                <text x="350" y="170" fill="#FF00FF" font-size="10">RVP</text>
                <line x1="200" y1="100" x2="200" y2="240" stroke="#FF5733" stroke-width="4"/>
                <line x1="200" y1="100" x2="40" y2="150" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/>
                <line x1="200" y1="240" x2="40" y2="150" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/>
                <line x1="200" y1="100" x2="360" y2="150" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/>
                <line x1="200" y1="240" x2="360" y2="150" stroke="#FF5733" stroke-width="2" stroke-dasharray="3,3"/>
                <line x1="100" y1="125" x2="100" y2="200" stroke="#FF5733" stroke-width="3"/>
                <line x1="300" y1="115" x2="300" y2="210" stroke="#FF5733" stroke-width="3"/>
            </svg>
        """
    }
    
    current_template = templates[lesson].replace('\n', '').replace('"', '\\"')

    # Opacity control
    opacity = st.slider("Template Transparency:", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    # Pure HTML5/JS Live Camera view with Transparent Tracing Layer
    # This renders beautifully on Safari/Chrome iOS browsers because it's client-side!
    camera_html = f"""
    <div style="position: relative; width: 100%; max-width: 500px; aspect-ratio: 4/3; background-color: #000; border-radius: 10px; overflow: hidden; margin: auto;">
        <video id="webcam" autoplay playsinline style="width: 100%; height: 100%; object-fit: cover;"></video>
        <div id="svg-overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; opacity: {opacity};">
            {current_template}
        </div>
    </div>
    
    <script>
        const video = document.getElementById('webcam');
        // Request access specifically to the rear-facing camera for desk-drawing
        navigator.mediaDevices.getUserMedia({{ 
            video: {{ facingMode: "environment" }} 
        }})
        .then(stream => {{
            video.srcObject = stream;
        }})
        .catch(err => {{
            console.error("Camera access blocked: ", err);
            // Fallback to any camera if rear camera is not detected
            navigator.mediaDevices.getUserMedia({{ video: true }})
            .then(stream => {{ video.srcObject = stream; }});
        }});
    </script>
    """
    
    # Embed the custom tracking screen
    components.html(camera_html, height=400)
    
    st.write("---")
    st.write("### 🤖 Submit for Professor Critique")
    st.write("Take a snapshot of your drawing paper with your phone, upload it, and get structural advice.")
    
    # Streamlit file uploader to feed the AI
    uploaded_image = st.file_uploader("Upload a photo of your paper sketch:", type=["jpg", "jpeg", "png"])
    
    if uploaded_image and api_key:
        if st.button("Critique My Drawing!"):
            with st.spinner("The Professor is evaluating your linework..."):
                try:
                    img = Image.open(uploaded_image)
                    
                    # Create the prompt matching the style of Scotty
                    prompt = f"""
                    You are a friendly, encouraging professional urban sketching artist and architecture tutor.
                    A beginner child is following the video tutorial for "{lesson}".
                    Here is a photo of their hand-drawn sketch on paper.
                    
                    Please review their drawing and write a brief critique:
                    1. Praise two specific details they did beautifully (like their loose line quality, attempt at perspective, or confidence).
                    2. Point out one constructive alignment or perspective adjustment they can make to match the tutorial style.
                    3. Keep your language warm, constructive, and simple enough for a young student. Use bullet points for easy reading.
                    """
                    
                    # Call Gemini 1.5 Flash
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content([prompt, img])
                    
                    st.success("📝 Professor's Feedback:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error calling the AI model: {e}")
