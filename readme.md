# Time Capsule Web App

A simple, interactive web app where users can create "time capsules" containing messages and media (images, videos). The capsules are set to unlock at a future date and time, and users can view and download the media once unlocked.

## Features

- **Login System**: Secure login using a valid username and password.
- **Create Time Capsules**: Users can create time capsules with a title, message, unlock date & time, and media (optional).
- **View Time Capsules**: Users can view their created capsules and see if they are unlocked or not.
- **Download Media**: Once the capsule is unlocked, users can download the media (image/video).
- **Delete Capsules**: Users can delete any time capsule they no longer need.

## Requirements

- Python 3.x
- Streamlit (`streamlit`)


## Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd Time-Capsule-Web-App
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:

    ```bash
    streamlit run app.py
    ```

## How to Use

1. **Login**:
   - Enter your username and password to log in.
   - The default username is `GIAIC` and the password is `Giaic@123`.

2. **Create a Capsule**:
   - Provide a title, message, and an unlock date/time.
   - Optionally, upload an image or video (e.g., `.jpg`, `.png`, `.mp4`).
   - Click **Save Capsule** to store it.

3. **View Capsules**:
   - After logging in, you can view your time capsules.
   - Unlocked capsules will show the media (image/video) and a **Download** button.
   - You can delete any capsule by clicking **Delete Capsule**.

4. **Logout**:
   - You can log out at any time by selecting **Logout** from the sidebar.

***Run in your browser*
- https://rtek6dpke2odc2p2kpd3vc.streamlit.app/



