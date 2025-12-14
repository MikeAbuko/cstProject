# Week 9 + 11 - Datasets Page (CRUD Operations - OOP Version)
# Create, Read, Update, Delete dataset metadata using OOP

import streamlit as st
import pandas as pd
from datetime import datetime
# Week 11 - Import OOP classes
from app.services.database_manager import DatabaseManager
from models.dataset import Dataset

# Page configuration
st.set_page_config(
    page_title="Datasets",
    page_icon="📁",
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
st.title("📁 Datasets Management")
st.markdown("Create, view, update, and delete dataset metadata")

# Tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "➕ Add New", "✏️ Update", "🗑️ Delete"])

# TAB 1: View All Datasets (OOP Version)
with tab1:
    st.subheader("All Datasets")
    
    try:
        # Week 11 - Get datasets as objects
        datasets = db_manager.get_all_datasets()
        
        if not datasets:
            st.info("No datasets found. Add some datasets using the 'Add New' tab.")
        else:
            # Convert objects to DataFrame for display
            dataset_dicts = []
            for dataset in datasets:
                dataset_dicts.append({
                    'id': dataset.get_id(),
                    'dataset_name': dataset.get_name(),
                    'category': dataset.get_format(),
                    'source': dataset.get_source(),
                    'record_count': dataset.get_rows(),
                    'file_size_mb': round(dataset.calculate_size_mb(), 2)
                })
            df = pd.DataFrame(dataset_dicts)
            
            # Filter by category
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_category = st.multiselect(
                    "Filter by Category",
                    df['category'].unique().tolist()
                )
            
            # Apply filter - start with all data
            filtered_df = df.copy()
            
            if filter_category:
                filtered_df = filtered_df[filtered_df['category'].isin(filter_category)]
            
            # Display table
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            st.success(f"Total datasets: {len(filtered_df)}")
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="datasets_metadata.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Error loading datasets: {e}")

# TAB 2: Add New Dataset
with tab2:
    st.subheader("Add New Dataset")
    
    with st.form("add_dataset_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            dataset_name = st.text_input("Dataset Name", placeholder="e.g., Network Logs 2024")
            
            category = st.selectbox(
                "Category",
                ["Threat Intelligence", "Network Logs", "User Data", "System Logs", 
                 "Malware Samples", "Security Reports", "Other"]
            )
            
            source = st.text_input("Source", placeholder="e.g., Internal Systems")
        
        with col2:
            last_updated = st.date_input("Last Updated", value=datetime.now())
            
            record_count = st.number_input("Record Count", min_value=0, value=0, step=1)
            
            file_size_mb = st.number_input("File Size (MB)", min_value=0.0, value=0.0, step=0.1, format="%.2f")
        
        submit = st.form_submit_button("Add Dataset", type="primary", use_container_width=True)
        
        if submit:
            if not dataset_name or not source:
                st.error("❌ Dataset Name and Source are required!")
            else:
                try:
                    # Week 11 - Use OOP method
                    id = db_manager.insert_dataset(
                        dataset_name=dataset_name,
                        category=category,
                        source=source,
                        last_updated=str(last_updated),
                        record_count=record_count,
                        file_size_mb=file_size_mb
                    )
                    st.success(f"✅ Dataset '{dataset_name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error adding dataset: {e}")

# TAB 3: Update Dataset
with tab3:
    st.subheader("Update Dataset Record Count")
    
    try:
        df = get_all_datasets()
        
        if df.empty:
            st.info("No datasets to update.")
        else:
            # Select dataset to update
            dataset_options = {f"ID {row['id']}: {row['dataset_name']}": row['id'] 
                              for _, row in df.iterrows()}
            selected = st.selectbox("Select Dataset to Update", list(dataset_options.keys()))
            
            if selected:
                dataset_id = dataset_options[selected]
                dataset = df[df['id'] == dataset_id].iloc[0]
                
                st.markdown("### Current Dataset Details")
                st.write(f"**Name:** {dataset['dataset_name']}")
                st.write(f"**Category:** {dataset['category']}")
                st.write(f"**Current Record Count:** {dataset['record_count']}")
                st.write(f"**Source:** {dataset['source']}")
                st.write(f"**Last Updated:** {dataset['last_updated']}")
                
                with st.form("update_dataset_form"):
                    new_count = st.number_input(
                        "New Record Count",
                        min_value=0,
                        value=int(dataset['record_count']),
                        step=1
                    )
                    
                    update_btn = st.form_submit_button("Update Record Count", type="primary", use_container_width=True)
                    
                    if update_btn:
                        try:
                            rows = update_dataset_records(dataset_id, new_count)
                            if rows > 0:
                                st.success(f"✅ Dataset '{dataset['dataset_name']}' updated!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update dataset")
                        except Exception as e:
                            st.error(f"❌ Error updating dataset: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# TAB 4: Delete Dataset
with tab4:
    st.subheader("Delete Dataset")
    st.warning("⚠️ This action cannot be undone!")
    
    try:
        df = get_all_datasets()
        
        if df.empty:
            st.info("No datasets to delete.")
        else:
            # Select dataset to delete
            dataset_options = {f"ID {row['id']}: {row['dataset_name']}": row['id'] 
                              for _, row in df.iterrows()}
            selected = st.selectbox("Select Dataset to Delete", list(dataset_options.keys()))
            
            if selected:
                dataset_id = dataset_options[selected]
                dataset = df[df['id'] == dataset_id].iloc[0]
                
                # Show dataset details
                st.markdown("### Dataset Details")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**ID:** {dataset['id']}")
                    st.write(f"**Name:** {dataset['dataset_name']}")
                    st.write(f"**Category:** {dataset['category']}")
                    st.write(f"**Source:** {dataset['source']}")
                
                with col2:
                    st.write(f"**Record Count:** {dataset['record_count']}")
                    st.write(f"**File Size:** {dataset['file_size_mb']} MB")
                    st.write(f"**Last Updated:** {dataset['last_updated']}")
                
                # Confirm deletion
                if st.button("🗑️ Delete This Dataset", type="primary", use_container_width=True):
                    try:
                        rows = delete_dataset(dataset_id)
                        if rows > 0:
                            st.success(f"✅ Dataset '{dataset['dataset_name']}' deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete dataset")
                    except Exception as e:
                        st.error(f"❌ Error deleting dataset: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username} | Powered by AngryPanda🐼")
