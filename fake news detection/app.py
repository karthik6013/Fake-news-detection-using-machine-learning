
import streamlit as st
import joblib
import os

# --- Custom CSS for background image and text area highlight ---
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://wallpapercave.com/wp/wp5709257.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .login-box {
        background: rgba(255,255,255,0.85);
        padding: 2rem;
        border-radius: 10px;
        max-width: 350px;
        margin: 5rem auto 2rem auto;
        box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    }
    textarea, .stTextArea textarea {
        background: #fffbe6 !important;
        border: 2px solid #f7b731 !important;
        border-radius: 8px !important;
        font-size: 1.1rem;
    }
    .detector-title {
        background: #f7b731;
        color: #222;
        font-weight: bold;
        font-size: 2.2rem;
        padding: 0.7rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- Simple signup/login authentication ---
if 'users' not in st.session_state:
    st.session_state.users = {"admin": "password123"}  # demo user
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def signup():
    st.markdown('<div class="detector-title">Fake News Detector</div>', unsafe_allow_html=True)
    st.header("Sign Up")
    new_username = st.text_input("Choose a Username", key="signup_user")
    new_password = st.text_input("Choose a Password", type="password", key="signup_pass")
    if st.button("Sign Up"):
        if new_username in st.session_state.users:
            st.error("Username already exists.")
        elif not new_username or not new_password:
            st.error("Please enter both username and password.")
        else:
            st.session_state.users[new_username] = new_password
            st.success("Signup successful! Please log in.")
            st.session_state.show_signup = False
            st.rerun()
    if st.button("Back to Login"):
        st.session_state.show_signup = False
        st.rerun()

def login():
    st.markdown('<div class="detector-title">Fake News Detector</div>', unsafe_allow_html=True)
    st.header("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
    if st.button("Sign Up"):
        st.session_state.show_signup = True
        st.rerun()

if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

if not st.session_state.logged_in:
    if st.session_state.show_signup:
        signup()
    else:
        login()
    st.stop()

# --- Main App ---
script_dir = os.path.dirname(os.path.abspath(__file__))
VECTORIZER_PATH = os.path.join(script_dir, "vectorizer.jb")
MODEL_PATH = os.path.join(script_dir, "lr_model.jb")

@st.cache_resource
def load_model_and_vectorizer():
    vectorizer = joblib.load(VECTORIZER_PATH)
    model = joblib.load(MODEL_PATH)
    return vectorizer, model

# --- User Profile Section with Logout ---
profile_col1, profile_col2 = st.columns([6,1])
with profile_col1:
    st.markdown(
        f"""
        <div style='background: rgba(255,255,255,0.85); padding: 1rem 2rem; border-radius: 10px; display: inline-block; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
            <b>👤 User:</b> {st.session_state.current_user}
        </div>
        """,
        unsafe_allow_html=True
    )
with profile_col2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

st.title("Fake News Detector")
st.write("Enter a News Article below to check whether it is Fake or Real.")

inputn = st.text_area("News Article:")

if st.button("Check News"):
    vectorizer, model = load_model_and_vectorizer()
    if inputn.strip():
        transform_input = vectorizer.transform([inputn])
        prediction = model.predict(transform_input)
        if prediction[0] == 1:
            st.markdown("""
<div style='background: #fff; padding: 1.5rem; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
    <span style='font-size:2.5rem; color:green; margin-right:1rem;'>&#10004;&#65039;</span>
    <span style='font-size:1.3rem; color:#222;'>The News is <b>Real!</b></span>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style='background: #fff; padding: 1.5rem; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
    <span style='font-size:2.5rem; color:red; margin-right:1rem;'>&#10060;</span>
    <span style='font-size:1.3rem; color:#222;'>The News is <b>Fake!</b></span>
</div>
""", unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to Analyze.")
