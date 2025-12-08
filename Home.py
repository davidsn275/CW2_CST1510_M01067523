import streamlit as st
from pathlib import Path
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))



# Initialize services
db = DatabaseManager("DATA/intelligence_platform.db")
db.connect()
auth = AuthManager(db)

# Page setup
st.set_page_config(
    page_title="Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Styling
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling - clean and appealing */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 20px;
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-color: #667eea;
        color: white !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [aria-selected="false"] {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Button styling - appealing and clean */
    .stButton > button {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 500;
        transition: all 0.2s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Primary button (first column - Go to Dashboard) */
    div[data-testid="column"]:first-of-type .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border-color: #667eea !important;
    }
    
    div[data-testid="column"]:first-of-type .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd6, #6a3f8f) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Secondary button (second column - Log out) */
    div[data-testid="column"]:last-of-type .stButton > button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    div[data-testid="column"]:last-of-type .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for login tracking
if "username" not in st.session_state:
    st.session_state.username = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Page header
st.title("🛡️ Intelligence Platform")
st.caption("Secure access to your analytics dashboard")

# Show welcome screen if already logged in
if st.session_state.logged_in:
    st.write("👋 Welcome back!")
    st.write(f"Logged in as **{st.session_state.username}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Go to Dashboard"):
            st.switch_page("pages/1_Incidents _Dashboard.py")
    with col2:
        if st.button("🚪 Log out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    st.stop()


# Login and Register tabs
tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])

# Login form
with tab_login:
    login_username = st.text_input("Username", key="login_username", placeholder="Enter your username")
    login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
    
    if st.button("Sign In", type="primary"):
        if login_username and login_password:
            # Use AuthManager for login
            success, message, _ = auth.login_user(login_username, login_password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success(f"✅ {message}")
                st.switch_page("pages/1_Incidents _Dashboard.py")
            else:
                st.error(f"❌ {message}")
        else:
            st.warning("⚠️ Please enter username and password.")

# Register form
with tab_register:
    new_username = st.text_input("Choose a username", key="register_username", placeholder="Create a username")
    new_password = st.text_input("Choose a password", type="password", key="register_password", placeholder="Create a password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm", placeholder="Confirm your password")
    
    if st.button("Create Account"):
        if not new_username or not new_password:
            st.warning("⚠️ Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match.")
        else:
            try:
                # Use AuthManager for registration
                success, message = auth.register_user(new_username, new_password)
                if success:
                    st.success(f"✅ {message}")
                    st.info("💡 Switch to the Login tab to sign in.")
                else:
                    st.error(f"❌ {message}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# Footer
st.markdown("---")
st.caption("🔒 Secured with enterprise-grade encryption")
