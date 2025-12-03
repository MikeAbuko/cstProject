# Week 9 - Dashboard Page
# Shows overview statistics and welcome message

import streamlit as st
from app.data.db import connect_database

# Page configuration
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please login first!")
    st.info("👈 Go to Home page to login")
    st.stop()

# Get statistics from database
def get_stats():
    conn = connect_database()
    cursor = conn.cursor()
    
    # Count records in each table
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM cyber_incidents")
    incidents_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM datasets_metadata")
    datasets_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM it_tickets")
    tickets_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'users': users_count,
        'incidents': incidents_count,
        'datasets': datasets_count,
        'tickets': tickets_count
    }

# Main dashboard
st.title("📊 Dashboard")
st.markdown(f"### Welcome, {st.session_state.username}! 👋")

st.markdown("---")

# Get and display statistics
try:
    stats = get_stats()
    
    # Display stats in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Users",
            value=stats['users']
        )
    
    with col2:
        st.metric(
            label="🚨 Cyber Incidents",
            value=stats['incidents']
        )
    
    with col3:
        st.metric(
            label="📁 Datasets",
            value=stats['datasets']
        )
    
    with col4:
        st.metric(
            label="🎫 IT Tickets",
            value=stats['tickets']
        )
    
    st.markdown("---")
    
    # Quick links section
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🚨 Incidents")
        st.markdown("Manage cyber security incidents")
        if st.button("Go to Incidents", key="incidents", use_container_width=True):
            st.switch_page("pages/Incidents.py")
    
    with col2:
        st.markdown("#### 📁 Datasets")
        st.markdown("Manage dataset metadata")
        if st.button("Go to Datasets", key="datasets", use_container_width=True):
            st.switch_page("pages/Datasets.py")
    
    with col3:
        st.markdown("#### 🎫 Tickets")
        st.markdown("Manage IT support tickets")
        if st.button("Go to Tickets", key="tickets", use_container_width=True):
            st.switch_page("pages/Tickets.py")
    
    st.markdown("---")
    
    # Recent activity section
    st.markdown("### 📈 System Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🎯 Platform Features:**
        - User authentication and authorization
        - Cyber incident tracking
        - Dataset metadata management
        - IT ticket system
        - Analytics and visualization
        """)
    
    with col2:
        st.success("""
        **✅ Current Status:**
        - All systems operational
        - Database connected
        - User authenticated
        - Ready for operations
        """)

except Exception as e:
    st.error(f"❌ Error loading dashboard: {e}")
    st.info("Make sure the database is initialized. Run `python main.py` first.")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username}")
