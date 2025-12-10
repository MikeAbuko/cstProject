# Week 9 - Tickets Page (CRUD Operations)
# Create, Read, Update, Delete IT support tickets

import streamlit as st
import pandas as pd
from datetime import datetime
# Import Week 8 functions
from app.data.tickets import (
    get_all_tickets,
    insert_ticket,
    update_ticket_status,
    delete_ticket
)

# Page configuration
st.set_page_config(
    page_title="IT Tickets",
    page_icon="🎫",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please login first!")
    st.info("👈 Go to Home page to login")
    st.stop()

# Main page
st.title("🎫 IT Support Tickets Management")
st.markdown("Create, view, update, and delete IT support tickets")

# Tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "➕ Add New", "✏️ Update", "🗑️ Delete"])

# TAB 1: View All Tickets
with tab1:
    st.subheader("All IT Tickets")
    
    try:
        df = get_all_tickets()  # Uses function from app/data/tickets.py
        
        if df.empty:
            st.info("No tickets found. Add some tickets using the 'Add New' tab.")
        else:
            # Filter by status
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_status = st.multiselect(
                    "Filter by Status",
                    ["Open", "In Progress", "Resolved", "Closed"],
                    default=["Open", "In Progress", "Resolved", "Closed"]
                )
            
            # Apply filter
            if filter_status:
                filtered_df = df[df['status'].isin(filter_status)]
            else:
                filtered_df = df
            
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            st.success(f"Total tickets: {len(filtered_df)}")
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="it_tickets.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Error loading tickets: {e}")

# TAB 2: Add New Ticket
with tab2:
    st.subheader("Create New Ticket")
    
    with st.form("add_ticket_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            ticket_id = st.text_input("Ticket ID", placeholder="e.g., TKT-001")
            
            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High", "Critical"]
            )
            
            status = st.selectbox(
                "Status",
                ["Open", "In Progress", "Resolved", "Closed"]
            )
            
            category = st.selectbox(
                "Category",
                ["Hardware", "Software", "Network", "Security", "Other"]
            )
        
        with col2:
            subject = st.text_input("Subject", placeholder="Brief description")
            
            assigned_to = st.text_input("Assigned To (optional)")
            
            created_date = st.date_input("Created Date", value=datetime.now())
        
        description = st.text_area("Description", placeholder="Detailed description...")
        
        submit = st.form_submit_button("Create Ticket", type="primary", use_container_width=True)
        
        if submit:
            if not ticket_id or not subject:
                st.error("❌ Ticket ID and Subject are required!")
            else:
                try:
                    # Use insert_ticket function
                    id = insert_ticket(
                        ticket_id=ticket_id,
                        priority=priority,
                        status=status,
                        category=category,
                        subject=subject, 
                        description=description,
                        created_date=str(created_date),
                        assigned_to=assigned_to if assigned_to else None
                    )
                    st.success(f"✅ Ticket {ticket_id} created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error creating ticket: {e}")

# TAB 3: Update Ticket
with tab3:
    st.subheader("Update Ticket Status")
    
    try:
        df = get_all_tickets()
        
        if df.empty:
            st.info("No tickets to update.")
        else:
            # Select ticket to update
            ticket_options = {f"ID {row['id']}: {row['ticket_id']} - {row['subject']}": row['id'] 
                             for _, row in df.iterrows()}
            selected = st.selectbox("Select Ticket to Update", list(ticket_options.keys()))
            
            if selected:
                ticket_db_id = ticket_options[selected]
                ticket = df[df['id'] == ticket_db_id].iloc[0]
                
                st.markdown("### Current Ticket Details")
                st.write(f"**Ticket ID:** {ticket['ticket_id']}")
                st.write(f"**Subject:** {ticket['subject']}")
                st.write(f"**Current Status:** {ticket['status']}")
                st.write(f"**Priority:** {ticket['priority']}")
                
                with st.form("update_ticket_form"):
                    new_status = st.selectbox(
                        "New Status",
                        ["Open", "In Progress", "Resolved", "Closed"],
                        index=["Open", "In Progress", "Resolved", "Closed"].index(ticket['status'])
                    )
                    
                    update_btn = st.form_submit_button("Update Status", type="primary", use_container_width=True)
                    
                    if update_btn:
                        try:
                            # Use update_ticket_status function
                            rows = update_ticket_status(ticket_db_id, new_status)
                            if rows > 0:
                                st.success(f"✅ Ticket {ticket['ticket_id']} updated to {new_status}!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update ticket")
                        except Exception as e:
                            st.error(f"❌ Error updating ticket: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# TAB 4: Delete Ticket
with tab4:
    st.subheader("Delete Ticket")
    st.warning("⚠️ This action cannot be undone!")
    
    try:
        df = get_all_tickets()
        
        if df.empty:
            st.info("No tickets to delete.")
        else:
            # Select ticket to delete
            ticket_options = {f"ID {row['id']}: {row['ticket_id']} - {row['subject']}": row['id'] 
                             for _, row in df.iterrows()}
            selected = st.selectbox("Select Ticket to Delete", list(ticket_options.keys()))
            
            if selected:
                ticket_db_id = ticket_options[selected]
                ticket = df[df['id'] == ticket_db_id].iloc[0]
                
                # Show ticket details
                st.markdown("### Ticket Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Ticket ID:** {ticket['ticket_id']}")
                    st.write(f"**Subject:** {ticket['subject']}")
                    st.write(f"**Priority:** {ticket['priority']}")
                    st.write(f"**Status:** {ticket['status']}")
                with col2:
                    st.write(f"**Category:** {ticket['category']}")
                    st.write(f"**Created:** {ticket['created_date']}")
                    st.write(f"**Assigned To:** {ticket.get('assigned_to', 'Unassigned')}")
                
                st.write(f"**Description:** {ticket['description']}")
                
                # Confirm deletion
                if st.button("🗑️ Delete This Ticket", type="primary", use_container_width=True):
                    try:
                        # Use delete_ticket function
                        rows = delete_ticket(ticket_db_id)
                        if rows > 0:
                            st.success(f"✅ Ticket {ticket['ticket_id']} deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete ticket")
                    except Exception as e:
                        st.error(f"❌ Error deleting ticket: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username}")
