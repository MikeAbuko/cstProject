# Week 9 - Incidents Page (CRUD Operations)
# Create, Read, Update, Delete cyber incidents

import streamlit as st
import pandas as pd
from app.data.db import connect_database
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Cyber Incidents",
    page_icon="🚨",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please login first!")
    st.info("👈 Go to Home page to login")
    st.stop()

# Database functions
def get_all_incidents():
    """Fetch all incidents from database"""
    conn = connect_database()
    query = "SELECT * FROM cyber_incidents ORDER BY date DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_incident(incident_type, severity, description, incident_date, affected_systems):
    """Add new incident to database"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents (incident_type, severity, description, incident_date, affected_systems)
        VALUES (?, ?, ?, ?, ?)
    """, (incident_type, severity, description, incident_date, affected_systems))
    conn.commit()
    conn.close()

def update_incident(incident_id, incident_type, severity, description, incident_date, affected_systems):
    """Update existing incident"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cyber_incidents 
        SET incident_type=?, severity=?, description=?, incident_date=?, affected_systems=?
        WHERE id=?
    """, (incident_type, severity, description, incident_date, affected_systems, incident_id))
    conn.commit()
    conn.close()

def delete_incident(incident_id):
    """Delete incident from database"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id=?", (incident_id,))
    conn.commit()
    conn.close()

# Main page
st.title("🚨 Cyber Incidents Management")
st.markdown("Create, view, update, and delete cyber security incidents")

# Tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "➕ Add New", "✏️ Update", "🗑️ Delete"])

# TAB 1: View All Incidents
with tab1:
    st.subheader("All Cyber Incidents")
    
    try:
        df = get_all_incidents()
        
        if df.empty:
            st.info("No incidents found. Add some incidents using the 'Add New' tab.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.success(f"Total incidents: {len(df)}")
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="cyber_incidents.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Error loading incidents: {e}")

# TAB 2: Add New Incident
with tab2:
    st.subheader("Add New Incident")
    
    with st.form("add_incident_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            incident_type = st.selectbox(
                "Incident Type",
                ["Malware", "Phishing", "Data Breach", "DDoS Attack", "Unauthorized Access", "Other"]
            )
            
            severity = st.selectbox(
                "Severity",
                ["Low", "Medium", "High", "Critical"]
            )
        
        with col2:
            incident_date = st.date_input("Incident Date", value=datetime.now())
            affected_systems = st.text_input("Affected Systems", placeholder="e.g., Server-01, Database-Main")
        
        description = st.text_area("Description", placeholder="Describe the incident in detail...")
        
        submit = st.form_submit_button("Add Incident", type="primary", use_container_width=True)
        
        if submit:
            if not description:
                st.error("❌ Description is required!")
            else:
                try:
                    add_incident(
                        incident_type,
                        severity,
                        description,
                        str(incident_date),
                        affected_systems
                    )
                    st.success("✅ Incident added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error adding incident: {e}")

# TAB 3: Update Incident
with tab3:
    st.subheader("Update Existing Incident")
    
    try:
        df = get_all_incidents()
        
        if df.empty:
            st.info("No incidents to update.")
        else:
            # Select incident to update
            incident_options = {f"ID {row['id']}: {row['incident_type']} - {row['severity']}": row['id'] 
                               for _, row in df.iterrows()}
            selected = st.selectbox("Select Incident to Update", list(incident_options.keys()))
            
            if selected:
                incident_id = incident_options[selected]
                incident = df[df['id'] == incident_id].iloc[0]
                
                with st.form("update_incident_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_type = st.selectbox(
                            "Incident Type",
                            ["Malware", "Phishing", "Data Breach", "DDoS Attack", "Unauthorized Access", "Other"],
                            index=["Malware", "Phishing", "Data Breach", "DDoS Attack", "Unauthorized Access", "Other"].index(incident['incident_type'])
                        )
                        
                        new_severity = st.selectbox(
                            "Severity",
                            ["Low", "Medium", "High", "Critical"],
                            index=["Low", "Medium", "High", "Critical"].index(incident['severity'])
                        )
                    
                    with col2:
                        new_date = st.date_input("Incident Date", value=pd.to_datetime(incident['incident_date']))
                        new_systems = st.text_input("Affected Systems", value=incident['affected_systems'])
                    
                    new_description = st.text_area("Description", value=incident['description'])
                    
                    update_btn = st.form_submit_button("Update Incident", type="primary", use_container_width=True)
                    
                    if update_btn:
                        try:
                            update_incident(
                                incident_id,
                                new_type,
                                new_severity,
                                new_description,
                                str(new_date),
                                new_systems
                            )
                            st.success("✅ Incident updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error updating incident: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# TAB 4: Delete Incident
with tab4:
    st.subheader("Delete Incident")
    st.warning("⚠️ This action cannot be undone!")
    
    try:
        df = get_all_incidents()
        
        if df.empty:
            st.info("No incidents to delete.")
        else:
            # Select incident to delete
            incident_options = {f"ID {row['id']}: {row['incident_type']} - {row['severity']}": row['id'] 
                               for _, row in df.iterrows()}
            selected = st.selectbox("Select Incident to Delete", list(incident_options.keys()))
            
            if selected:
                incident_id = incident_options[selected]
                incident = df[df['id'] == incident_id].iloc[0]
                
                # Show incident details
                st.markdown("### Incident Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Type:** {incident['incident_type']}")
                    st.write(f"**Severity:** {incident['severity']}")
                with col2:
                    st.write(f"**Date:** {incident['incident_date']}")
                    st.write(f"**Systems:** {incident['affected_systems']}")
                
                st.write(f"**Description:** {incident['description']}")
                
                # Confirm deletion
                if st.button("🗑️ Delete This Incident", type="primary", use_container_width=True):
                    try:
                        delete_incident(incident_id)
                        st.success("✅ Incident deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting incident: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username}")
