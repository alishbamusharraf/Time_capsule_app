import streamlit as st
from datetime import datetime, date, time
import os
from capsule import Capsule  # Importing the Capsule class

# Secret Key for session management
st.set_page_config(page_title="Time Capsule App", layout="centered")
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

VALID_USERNAME = 'GIAIC'
VALID_PASSWORD = 'Giaic@123'

capsules = []  # List to hold Capsule objects

# Session check (login required)
if 'username' not in st.session_state:
    st.session_state['username'] = None

def login_required():
    if st.session_state['username'] is None:
        st.warning("You must be logged in to access this page.")
        st.stop()

# Login function
def login(username, password):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        st.session_state['username'] = username
        st.success("Logged in successfully!")
    else:
        st.error("Invalid credentials!")

# Logout function
def logout():
    st.session_state['username'] = None
    st.success("Logged out successfully!")

# Home page function
def home():
    login_required()

    st.title("Time Capsule")
    for idx, capsule in enumerate(capsules):
        st.subheader(capsule.title)
        st.write(f"Message: {capsule.message}")
        st.write(f"Unlock Date: {capsule.unlock_date}")
        st.write(f"Unlocked: {'Yes' if capsule.is_unlocked() else 'No'}")
        if capsule.media_filename:
            st.image(os.path.join(UPLOAD_FOLDER, capsule.media_filename))
        if st.button(f"Delete Capsule {idx + 1}", key=f"delete{idx}"):
            capsules.pop(idx)
            st.rerun()

# Create page function
def create():
    login_required()

    st.title("Create a Capsule")

    title = st.text_input("Capsule Title", value=f"Capsule {len(capsules) + 1}")
    message = st.text_area("Message")
    unlock_date_str = st.date_input("Unlock Date")
    unlock_time_str = st.time_input("Unlock Time", value=datetime.now().time())
    media_file = st.file_uploader("Upload Media", type=["jpg", "png", "jpeg", "gif", "mp4"])

    if st.button("Save Capsule"):
        if unlock_date_str:
            try:
                unlock_datetime = datetime.combine(unlock_date_str, unlock_time_str)
                media_filename = None
                if media_file is not None:
                    media_filename = f"{datetime.now().timestamp()}_{media_file.name}"
                    media_path = os.path.join(UPLOAD_FOLDER, media_filename)
                    with open(media_path, "wb") as f:
                        f.write(media_file.getbuffer())

                new_capsule = Capsule(
                    title=title,
                    message=message,
                    unlock_date=unlock_datetime,
                    media_filename=media_filename
                )

                capsules.append(new_capsule)
                st.success("Capsule created successfully!")
            except ValueError as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please select an unlock date.")

# Login page function
def login_page():
    if 'username' in st.session_state and st.session_state['username'] is not None:
        st.warning("You are already logged in.")
        st.stop()

    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login(username, password)

# Logout page function
def logout_page():
    logout()

# Main function to manage app navigation
def main():
    page = st.sidebar.selectbox("Select Page", ["Login", "Home", "Create", "Logout"])

    if page == "Home":
        home()
    elif page == "Create":
        create()
    elif page == "Login":
        login_page()
    elif page == "Logout":
        logout_page()

if __name__ == "__main__":
    main()
