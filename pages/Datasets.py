# Week 9 - Datasets Page (CRUD Operations)
# Create, Read, Update, Delete dataset metadata

import streamlit as st
import pandas as pd
from app.data.db import connect_database
from datetime import datetime

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

# Database functions
def get_all_datasets():
    """Fetch all datasets from database"""
    conn = connect_database()
    query = "SELECT * FROM datasets_metadata ORDER BY last_updated DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_dataset(dataset_name, source, collection_date, data_type, description):
    """Add new dataset to database"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata (dataset_name, source, collection_date, data_type, description)
        VALUES (?, ?, ?, ?, ?)
    """, (dataset_name, source, collection_date, data_type, description))
    conn.commit()
    conn.close()

def update_dataset(dataset_id, dataset_name, source, collection_date, data_type, description):
    """Update existing dataset"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE datasets_metadata 
        SET dataset_name=?, source=?, collection_date=?, data_type=?, description=?
        WHERE id=?
    """, (dataset_name, source, collection_date, data_type, description, dataset_id))
    conn.commit()
    conn.close()

def delete_dataset(dataset_id):
    """Delete dataset from database"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id=?", (dataset_id,))
    conn.commit()
    conn.close()

# Main page
st.title("📁 Dataset Metadata Management")
st.markdown("Create, view, update, and delete dataset metadata")

# Tabs for different operations
tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "➕ Add New", "✏️ Update", "🗑️ Delete"])

# TAB 1: View All Datasets
with tab1:
    st.subheader("All Datasets")
    
    try:
        df = get_all_datasets()
        
        if df.empty:
            st.info("No datasets found. Add some datasets using the 'Add New' tab.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.success(f"Total datasets: {len(df)}")
            
            # Download button
            csv = df.to_csv(index=False)
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
            dataset_name = st.text_input("Dataset Name", placeholder="e.g., Customer Database 2024")
            source = st.text_input("Source", placeholder="e.g., Internal Systems, API, Survey")
            data_type = st.selectbox(
                "Data Type",
                ["Structured", "Unstructured", "Semi-Structured", "Time-Series", "Geospatial", "Other"]
            )
        
        with col2:
            collection_date = st.date_input("Collection Date", value=datetime.now())
        
        description = st.text_area("Description", placeholder="Describe the dataset, its purpose, and contents...")
        
        submit = st.form_submit_button("Add Dataset", type="primary", use_container_width=True)
        
        if submit:
            if not dataset_name or not description:
                st.error("❌ Dataset name and description are required!")
            else:
                try:
                    add_dataset(
                        dataset_name,
                        source,
                        str(collection_date),
                        data_type,
                        description
                    )
                    st.success("✅ Dataset added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error adding dataset: {e}")

# TAB 3: Update Dataset
with tab3:
    st.subheader("Update Existing Dataset")
    
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
                
                with st.form("update_dataset_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("Dataset Name", value=dataset['dataset_name'])
                        new_source = st.text_input("Source", value=dataset['source'])
                        new_type = st.selectbox(
                            "Data Type",
                            ["Structured", "Unstructured", "Semi-Structured", "Time-Series", "Geospatial", "Other"],
                            index=["Structured", "Unstructured", "Semi-Structured", "Time-Series", "Geospatial", "Other"].index(dataset['data_type'])
                        )
                    
                    with col2:
                        new_date = st.date_input("Collection Date", value=pd.to_datetime(dataset['collection_date']))
                    
                    new_description = st.text_area("Description", value=dataset['description'])
                    
                    update_btn = st.form_submit_button("Update Dataset", type="primary", use_container_width=True)
                    
                    if update_btn:
                        if not new_name or not new_description:
                            st.error("❌ Dataset name and description are required!")
                        else:
                            try:
                                update_dataset(
                                    dataset_id,
                                    new_name,
                                    new_source,
                                    str(new_date),
                                    new_type,
                                    new_description
                                )
                                st.success("✅ Dataset updated successfully!")
                                st.rerun()
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
                    st.write(f"**Name:** {dataset['dataset_name']}")
                    st.write(f"**Source:** {dataset['source']}")
                with col2:
                    st.write(f"**Type:** {dataset['data_type']}")
                    st.write(f"**Date:** {dataset['collection_date']}")
                
                st.write(f"**Description:** {dataset['description']}")
                
                # Confirm deletion
                if st.button("🗑️ Delete This Dataset", type="primary", use_container_width=True):
                    try:
                        delete_dataset(dataset_id)
                        st.success("✅ Dataset deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting dataset: {e}")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username}")
