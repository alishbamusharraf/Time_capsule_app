import streamlit as st
from datetime import datetime
import os

# --- App Configuration ---
st.set_page_config(page_title="📦 Time Capsule App", layout="centered")
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Credentials ---
VALID_USERNAME = 'GIAIC'
VALID_PASSWORD = 'Giaic@123'

# --- Initialize session state ---
if 'username' not in st.session_state:
    st.session_state['username'] = None

if 'capsules' not in st.session_state:
    st.session_state['capsules'] = []

# --- Helper Functions ---
def login_required():
    if st.session_state['username'] is None:
        st.warning("🚨 You must be logged in to access this page.")
        st.stop()

def login(username, password):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        st.session_state['username'] = username
        st.success(f"🎉 Logged in successfully as {username}!")
    else:
        st.error("❌ Invalid credentials! Please try again.")

def logout():
    st.session_state['username'] = None
    st.session_state['capsules'] = []
    st.success("👋 Logged out successfully!")

# --- Pages ---
def home():
    login_required()
    st.title("🏠 Your Time Capsules")

    if len(st.session_state['capsules']) == 0:
        st.info("You have no capsules yet. Create one!")
    else:
        for idx, capsule in enumerate(st.session_state['capsules']):
            with st.container():
                st.subheader(f"📦 {capsule['title']}")
                st.write(f"📝 **Message:** {capsule['message']}")
                st.write(f"📅 **Unlock Date:** {capsule['unlock_date']}")
                # Check if capsule is unlocked
                unlock_datetime = datetime.strptime(capsule['unlock_date'], "%Y-%m-%d %H:%M")
                is_unlocked = unlock_datetime <= datetime.now()
                st.write(f"🔓 **Unlocked:** {'Yes' if is_unlocked else 'No'}")
                
                # Only show media if the capsule is unlocked
                if is_unlocked and capsule['media_filename']:
                    file_path = f"static/uploads/{capsule['media_filename']}"
                    # Display image or video
                    if capsule['media_filename'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        st.image(file_path, width=300)
                    elif capsule['media_filename'].lower().endswith('.mp4'):
                        st.video(file_path)
                    
                    # Add a download button for media
                    with open(file_path, "rb") as media_file:
                        media_bytes = media_file.read()
                        st.download_button(
                            label="Download Media",
                            data=media_bytes,
                            file_name=capsule['media_filename'],
                            mime="image/jpeg" if capsule['media_filename'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif')) else "video/mp4"
                        )
                
                if st.button(f"🗑️ Delete Capsule {idx + 1}", key=f"delete{idx}"):
                    st.session_state['capsules'].pop(idx)
                    st.success("Capsule deleted!")
                    st.rerun()

def create():
    login_required()
    st.title("📝 Create a New Capsule")

    title = st.text_input("Title", value=f"Capsule {len(st.session_state['capsules']) + 1}")
    message = st.text_area("Message")
    unlock_date = st.date_input("Unlock Date", min_value=datetime.today())
    unlock_time = st.time_input("Unlock Time", value=datetime.now().time())
    media_file = st.file_uploader("Upload Media (optional)", type=["jpg", "png", "jpeg", "gif", "mp4"])

    if st.button("💾 Save Capsule"):
        if not title or not message:
            st.error("❌ Title and Message are required.")
        else:
            try:
                unlock_datetime = datetime.combine(unlock_date, unlock_time)
                media_filename = None
                if media_file is not None:
                    media_filename = f"{datetime.now().timestamp()}_{media_file.name}"
                    media_path = os.path.join(UPLOAD_FOLDER, media_filename)
                    with open(media_path, "wb") as f:
                        f.write(media_file.getbuffer())

                st.session_state['capsules'].append({
                    'title': title,
                    'message': message,
                    'unlock_date': unlock_datetime.strftime("%Y-%m-%d %H:%M"),
                    'media_filename': media_filename
                })
                st.success("🎉 Capsule created successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def login_page():
    if st.session_state['username'] is not None:
        st.warning(f"⚡ You are already logged in as {st.session_state['username']}.")
        return

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("🔓 Login"):
        login(username, password)

# --- Main ---
def main():
    st.sidebar.title("📚 Navigation")
    page = st.sidebar.selectbox("Select Page", ["Login", "Home", "Create", "Logout"])

    if page == "Home":
        home()
    elif page == "Create":
        create()
    elif page == "Login":
        login_page()
    elif page == "Logout":
        logout()

if __name__ == "__main__":
    main()
