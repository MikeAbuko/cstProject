# Week 9 - Tickets Page (CRUD Operations)
# Create, Read, Update, Delete IT support tickets

import streamlit as st
import pandas as pd
from app.data.db import connect_database
from datetime import datetime

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

# Database functions
def get_all_tickets():
    """Fetch all tickets from database"""
    conn = connect_database()
    query = "SELECT * FROM it_tickets ORDER BY created_date DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_ticket(ticket_subject, priority, status, requester, description, created_date):
    """Add new ticket to database"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets (ticket_subject, priority, status, requester, description, created_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ticket_subject, priority, status, requester, description, created_date))
    conn.commit()
    conn.close()

def update_ticket(ticket_id, ticket_subject, priority, status, requester, description, created_date):
    """Update existing ticket"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE it_tickets 
        SET ticket_subject=?, priority=?, status=?, requester=?, description=?, created_date=?
        WHERE id=?
    """, (ticket_subject, priority, status, requester, description, created_date, ticket_id))
    conn.commit()
    conn.close()

def delete_ticket(ticket_id):
    """Delete ticket from database"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE id=?", (ticket_id,))
    conn.commit()
    conn.close()

# Main page
st.title("🎫 IT Support Tickets Management")
st.markdown("Create, view, update, and delete IT support tickets")

# Tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "➕ Add New", "✏️ Update", "🗑️ Delete"])

# TAB 1: View All Tickets
with tab1:
    st.subheader("All IT Tickets")
    
    try:
        df = get_all_tickets()
        
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
            ticket_subject = st.text_input("Ticket Subject", placeholder="Brief description of the issue")
            
            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High", "Urgent"]
            )
            
            status = st.selectbox(
                "Status",
                ["Open", "In Progress", "Resolved", "Closed"]
            )
        
        with col2:
            requester = st.text_input("Requester", placeholder="Name or email of the person requesting")
            
            created_date = st.date_input("Created Date", value=datetime.now())
        
        description = st.text_area("Description", placeholder="Detailed description of the issue or request...")
        
        submit = st.form_submit_button("Create Ticket", type="primary", use_container_width=True)
        
        if submit:
            if not ticket_subject or not description:
                st.error("❌ Subject and description are required!")
            else:
                try:
                    add_ticket(
                        ticket_subject,
                        priority,
                        status,
                        requester,
                        description,
                        str(created_date)
                    )
                    st.success("✅ Ticket created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error creating ticket: {e}")

# TAB 3: Update Ticket
with tab3:
    st.subheader("Update Existing Ticket")
    
    try:
        df = get_all_tickets()
        
        if df.empty:
            st.info("No tickets to update.")
        else:
            # Select ticket to update
            ticket_options = {f"ID {row['id']}: {row['ticket_subject']} - {row['status']}": row['id'] 
                             for _, row in df.iterrows()}
            selected = st.selectbox("Select Ticket to Update", list(ticket_options.keys()))
            
            if selected:
                ticket_id = ticket_options[selected]
                ticket = df[df['id'] == ticket_id].iloc[0]
                
                with st.form("update_ticket_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_subject = st.text_input("Ticket Subject", value=ticket['ticket_subject'])
                        
                        new_priority = st.selectbox(
                            "Priority",
                            ["Low", "Medium", "High", "Urgent"],
                            index=["Low", "Medium", "High", "Urgent"].index(ticket['priority'])
                        )
                        
                        new_status = st.selectbox(
                            "Status",
                            ["Open", "In Progress", "Resolved", "Closed"],
                            index=["Open", "In Progress", "Resolved", "Closed"].index(ticket['status'])
                        )
                    
                    with col2:
                        new_requester = st.text_input("Requester", value=ticket['requester'])
                        
                        new_date = st.date_input("Created Date", value=pd.to_datetime(ticket['created_date']))
                    
                    new_description = st.text_area("Description", value=ticket['description'])
                    
                    update_btn = st.form_submit_button("Update Ticket", type="primary", use_container_width=True)
                    
                    if update_btn:
                        if not new_subject or not new_description:
                            st.error("❌ Subject and description are required!")
                        else:
                            try:
                                update_ticket(
                                    ticket_id,
                                    new_subject,
                                    new_priority,
                                    new_status,
                                    new_requester,
                                    new_description,
                                    str(new_date)
                                )
                                st.success("✅ Ticket updated successfully!")
                                st.rerun()
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
            ticket_options = {f"ID {row['id']}: {row['ticket_subject']} - {row['status']}": row['id'] 
                             for _, row in df.iterrows()}
            selected = st.selectbox("Select Ticket to Delete", list(ticket_options.keys()))
            
            if selected:
                ticket_id = ticket_options[selected]
                ticket = df[df['id'] == ticket_id].iloc[0]
                
                # Show ticket details
                st.markdown("### Ticket Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Subject:** {ticket['ticket_subject']}")
                    st.write(f"**Priority:** {ticket['priority']}")
                    st.write(f"**Status:** {ticket['status']}")
                with col2:
                    st.write(f"**Requester:** {ticket['requester']}")
                    st.write(f"**Created:** {ticket['created_date']}")
                
                st.write(f"**Description:** {ticket['description']}")
                
                # Confirm deletion
                if st.button("🗑️ Delete This Ticket", type="primary", use_container_width=True):
                    try:
                        delete_ticket(ticket_id)
                        st.success("✅ Ticket deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting ticket: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username}")
