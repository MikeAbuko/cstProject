# Week 9 - Home Page (Login/Register)
# This is the main entry point for the Streamlit web app

import streamlit as st
from app.services.user_service import login_user, register_user, validate_username, validate_password, get_user_by_username

# Page configuration
st.set_page_config(
    page_title="Intelligence Platform",
    page_icon="🔐",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Main app
st.markdown('<h1 class="main-header">🔐 Intelligence Platform</h1>', unsafe_allow_html=True)

# If already logged in, show welcome message
if st.session_state.logged_in:
    st.success(f"✅ Welcome back, {st.session_state.username}!")
    st.info("👈 Use the sidebar to navigate to different pages.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Available Pages")
        st.markdown("""
        - **Dashboard** - Overview and statistics
        - **Incidents** - Manage cyber incidents
        - **Datasets** - Manage datasets
        - **Tickets** - Manage IT tickets
        - **Analytics** - View charts and analysis
        """)
    
    with col2:
        st.markdown("### 🔓 Account")
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
else:
    # Show login/register tabs
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    # LOGIN TAB
    with tab1:
        st.markdown("### Login to your account")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("❌ Please fill in all fields.")
                else:
                    # Check credentials
                    user = get_user_by_username(username)
                    if user:
                        from app.services.user_service import verify_password
                        if verify_password(password, user[2]):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.success(f"✅ Welcome, {username}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid password.")
                    else:
                        st.error("❌ Username not found.")
    
    # REGISTER TAB
    with tab2:
        st.markdown("### Create a new account")
        
        with st.form("register_form"):
            new_username = st.text_input("Username", placeholder="Choose a username (3-20 characters)")
            new_password = st.text_input("Password", type="password", placeholder="Choose a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            submit_register = st.form_submit_button("Register", type="primary", use_container_width=True)
            
            if submit_register:
                # Validate inputs
                if not new_username or not new_password or not confirm_password:
                    st.error("❌ Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match.")
                else:
                    # Validate username
                    valid_user, user_msg = validate_username(new_username)
                    if not valid_user:
                        st.error(f"❌ {user_msg}")
                    else:
                        # Validate password
                        valid_pass, pass_msg = validate_password(new_password)
                        if not valid_pass:
                            st.error(f"❌ {pass_msg}")
                        else:
                            # Register user
                            if register_user(new_username, new_password):
                                st.success(f"✅ Account created successfully! You can now login.")
                            else:
                                st.error(f"❌ Username '{new_username}' already exists.")
        
        # Show password requirements
        with st.expander("ℹ️ Password Requirements"):
            st.markdown("""
            **Username:**
            - 3-20 characters
            - Alphanumeric only (no special characters)
            
            **Password:**
            - At least 6 characters
            - At least one digit
            - At least one uppercase letter
            - At least one lowercase letter
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>🎓 CST1510 - Multi-Domain Intelligence Platform</p>
    <p>Student: Mike Abuko (M01057708)</p>
</div>
""", unsafe_allow_html=True)
