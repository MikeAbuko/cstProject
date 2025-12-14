# Week 9 + 11 - Tickets Page (CRUD Operations - OOP Version)
# Create, Read, Update, Delete IT support tickets using OOP

import streamlit as st
import pandas as pd
from datetime import datetime
# Week 11 - Import OOP classes
from app.services.database_manager import DatabaseManager
from models.it_ticket import ITTicket

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

# Week 11 - Create OOP instance
db_manager = DatabaseManager()

# Main page
st.title("🎫 IT Support Tickets Management")
st.markdown("Create, view, update, and delete IT support tickets")

# Tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "➕ Add New", "✏️ Update", "🗑️ Delete"])

# TAB 1: View All Tickets (OOP Version)
with tab1:
    st.subheader("All IT Tickets")
    
    try:
        # Week 11 - Get tickets as objects
        tickets = db_manager.get_all_tickets()
        
        if not tickets:
            st.info("No tickets found. Add some tickets using the 'Add New' tab.")
        else:
            # Convert objects to DataFrame for display
            ticket_dicts = []
            for ticket in tickets:
                ticket_dicts.append({
                    'id': ticket.get_id(),
                    'title': ticket.get_title(),
                    'priority': ticket.get_priority(),
                    'status': ticket.get_status(),
                    'category': ticket.get_category(),
                    'assigned_to': ticket.get_assigned_to(),
                    'created_date': ticket.get_created_date()
                })
            df = pd.DataFrame(ticket_dicts)
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
                    # Week 11 - Use OOP method to insert
                    id = db_manager.insert_ticket(
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

# TAB 3: Update Ticket (OOP Version)
with tab3:
    st.subheader("Update Ticket Status")
    
    try:
        # Week 11 - Get tickets as objects
        tickets = db_manager.get_all_tickets()
        
        if not tickets:
            st.info("No tickets to update.")
        else:
            # Select ticket using objects
            ticket_options = {}
            for ticket in tickets:
                label = f"ID {ticket.get_id()}: {ticket.get_title()}"
                ticket_options[label] = ticket.get_id()
            
            selected = st.selectbox("Select Ticket to Update", list(ticket_options.keys()))
            
            if selected:
                ticket_db_id = ticket_options[selected]
                selected_ticket = db_manager.get_ticket_by_id(ticket_db_id)
                
                st.markdown("### Current Ticket Details")
                st.write(f"**Title:** {selected_ticket.get_title()}")
                st.write(f"**Current Status:** {selected_ticket.get_status()}")
                st.write(f"**Priority:** {selected_ticket.get_priority()}")
                st.write(f"**Category:** {selected_ticket.get_category()}")
                
                with st.form("update_ticket_form"):
                    new_status = st.selectbox(
                        "New Status",
                        ["Open", "In Progress", "Resolved", "Closed"],
                        index=["Open", "In Progress", "Resolved", "Closed"].index(selected_ticket.get_status())
                    )
                    
                    update_btn = st.form_submit_button("Update Status", type="primary", use_container_width=True)
                    
                    if update_btn:
                        try:
                            # Week 11 - Use OOP method
                            rows = db_manager.update_ticket_status(ticket_db_id, new_status)
                            if rows > 0:
                                st.success(f"✅ Ticket updated to {new_status}!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update ticket")
                        except Exception as e:
                            st.error(f"❌ Error updating ticket: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# TAB 4: Delete Ticket (OOP Version)
with tab4:
    st.subheader("Delete Ticket")
    st.warning("⚠️ This action cannot be undone!")
    
    try:
        # Week 11 - Get tickets as objects
        tickets = db_manager.get_all_tickets()
        
        if not tickets:
            st.info("No tickets to delete.")
        else:
            # Select ticket using objects
            ticket_options = {}
            for ticket in tickets:
                label = f"ID {ticket.get_id()}: {ticket.get_title()}"
                ticket_options[label] = ticket.get_id()
            
            selected = st.selectbox("Select Ticket to Delete", list(ticket_options.keys()))
            
            if selected:
                ticket_db_id = ticket_options[selected]
                selected_ticket = db_manager.get_ticket_by_id(ticket_db_id)
                
                # Show ticket details
                st.markdown("### Ticket Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Title:** {selected_ticket.get_title()}")
                    st.write(f"**Priority:** {selected_ticket.get_priority()}")
                    st.write(f"**Status:** {selected_ticket.get_status()}")
                with col2:
                    st.write(f"**Category:** {selected_ticket.get_category()}")
                    st.write(f"**Created:** {selected_ticket.get_created_date()}")
                    st.write(f"**Assigned To:** {selected_ticket.get_assigned_to()}")
                
                # Confirm deletion
                if st.button("🗑️ Delete This Ticket", type="primary", use_container_width=True):
                    try:
                        # Week 11 - Use OOP method
                        rows = db_manager.delete_ticket(ticket_db_id)
                        if rows > 0:
                            st.success(f"✅ Ticket deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete ticket")
                    except Exception as e:
                        st.error(f"❌ Error deleting ticket: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username} | Powered by AngryPanda🐼")
