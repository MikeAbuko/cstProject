# Week 9 - Incidents Page (CRUD Operations)
# Create, Read, Update, Delete cyber security incidents

import streamlit as st
import pandas as pd
from datetime import datetime
# Import Week 8 functions
from app.data.incidents import (
    get_all_incidents,
    insert_incident,
    update_incident_status,
    delete_incident
)

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

# Main page
st.title("🚨 Cyber Incidents Management")
st.markdown("Create, view, update, and delete cybersecurity incidents")

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
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_severity = st.multiselect(
                    "Filter by Severity",
                    ["Low", "Medium", "High", "Critical"]
                )
            
            with col2:
                filter_status = st.multiselect(
                    "Filter by Status",
                    ["Open", "Investigating", "Resolved", "Closed"]
                )
            
            with col3:
                filter_type = st.multiselect(
                    "Filter by Type",
                    df['incident_type'].unique().tolist()
                )
            
            # Apply filters - start with all data
            filtered_df = df.copy()
            
            if filter_severity:
                filtered_df = filtered_df[filtered_df['severity'].isin(filter_severity)]
            
            if filter_status:
                filtered_df = filtered_df[filtered_df['status'].isin(filter_status)]
            
            if filter_type:
                filtered_df = filtered_df[filtered_df['incident_type'].isin(filter_type)]
            
            # Display table
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            st.success(f"Total incidents: {len(filtered_df)}")
            
            # Download button
            csv = filtered_df.to_csv(index=False)
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
    st.subheader("Report New Incident")
    
    with st.form("add_incident_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date", value=datetime.now())
            
            incident_type = st.selectbox(
                "Incident Type",
                ["Phishing", "Malware", "DDoS", "Data Breach", "Ransomware", 
                 "Insider Threat", "Social Engineering", "SQL Injection", "Other"]
            )
            
            severity = st.selectbox(
                "Severity",
                ["Low", "Medium", "High", "Critical"]
            )
        
        with col2:
            status = st.selectbox(
                "Status",
                ["Open", "Investigating", "Resolved", "Closed"]
            )
            
            reported_by = st.text_input(
                "Reported By",
                value=st.session_state.username
            )
        
        description = st.text_area(
            "Incident Description",
            placeholder="Describe the incident in detail..."
        )
        
        submit = st.form_submit_button("Report Incident", type="primary", use_container_width=True)
        
        if submit:
            if not description:
                st.error("❌ Description is required!")
            else:
                try:
                    id = insert_incident(
                        date=str(date),
                        incident_type=incident_type,
                        severity=severity,
                        status=status,
                        description=description,
                        reported_by=reported_by
                    )
                    st.success(f"✅ Incident #{id} reported successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error adding incident: {e}")

# TAB 3: Update Incident
with tab3:
    st.subheader("Update Incident Status")
    
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
                
                st.markdown("### Current Incident Details")
                st.write(f"**Type:** {incident['incident_type']}")
                st.write(f"**Severity:** {incident['severity']}")
                st.write(f"**Current Status:** {incident['status']}")
                st.write(f"**Date:** {incident['date']}")
                st.write(f"**Reported By:** {incident['reported_by']}")
                
                with st.form("update_incident_form"):
                    new_status = st.selectbox(
                        "New Status",
                        ["Open", "Investigating", "Resolved", "Closed"],
                        index=["Open", "Investigating", "Resolved", "Closed"].index(incident['status'])
                    )
                    
                    update_btn = st.form_submit_button("Update Status", type="primary", use_container_width=True)
                    
                    if update_btn:
                        try:
                            rows = update_incident_status(incident_id, new_status)
                            if rows > 0:
                                st.success(f"✅ Incident #{incident_id} updated to {new_status}!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update incident")
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
                    st.write(f"**ID:** {incident['id']}")
                    st.write(f"**Date:** {incident['date']}")
                    st.write(f"**Type:** {incident['incident_type']}")
                    st.write(f"**Severity:** {incident['severity']}")
                
                with col2:
                    st.write(f"**Status:** {incident['status']}")
                    st.write(f"**Reported By:** {incident['reported_by']}")
                
                st.write(f"**Description:** {incident['description']}")
                
                # Confirm deletion
                if st.button("🗑️ Delete This Incident", type="primary", use_container_width=True):
                    try:
                        rows = delete_incident(incident_id)
                        if rows > 0:
                            st.success(f"✅ Incident #{incident_id} deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete incident")
                    except Exception as e:
                        st.error(f"❌ Error deleting incident: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username}")
