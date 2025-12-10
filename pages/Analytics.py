# Week 9 - Analytics Page
# Simple charts to visualize data

import streamlit as st
import pandas as pd
import plotly.express as px
from app.data.incidents import get_all_incidents
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets

# Page configuration
st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please login first!")
    st.info("👈 Go to Home page to login")
    st.stop()

# Page title
st.title("📊 Analytics Dashboard")
st.markdown("View charts and statistics")

# Get data from database
try:
    incidents_df = get_all_incidents()
    datasets_df = get_all_datasets()
    tickets_df = get_all_tickets()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Show summary numbers at top
st.subheader("📈 Summary")

col1, col2, col3 = st.columns(3)

with col1:
    total_incidents = len(incidents_df) if not incidents_df.empty else 0
    st.metric("🚨 Total Incidents", total_incidents)

with col2:
    total_datasets = len(datasets_df) if not datasets_df.empty else 0
    st.metric("📁 Total Datasets", total_datasets)

with col3:
    total_tickets = len(tickets_df) if not tickets_df.empty else 0
    st.metric("🎫 Total Tickets", total_tickets)

st.divider()

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["🚨 Incidents", "🎫 Tickets", "📁 Datasets"])

# TAB 1: Incidents
with tab1:
    st.subheader("Incident Analytics")
    
    if incidents_df.empty:
        st.info("No incidents yet. Add some incidents to see charts!")
    else:
        # Show two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Incidents by Type")
            # Count how many of each type
            type_counts = incidents_df['incident_type'].value_counts()
            # Make a bar chart
            fig = px.bar(
                x=type_counts.index,
                y=type_counts.values,
                labels={'x': 'Type', 'y': 'Count'},
                color=type_counts.values,
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Incidents by Severity")
            # Count how many of each severity
            severity_counts = incidents_df['severity'].value_counts()
            # Make a pie chart
            fig = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                color=severity_counts.index,
                color_discrete_map={
                    'Critical': 'red',
                    'High': 'orange',
                    'Medium': 'yellow',
                    'Low': 'green'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Status chart
        st.markdown("#### Incidents by Status")
        status_counts = incidents_df['status'].value_counts()
        fig = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            labels={'x': 'Status', 'y': 'Count'},
            color=status_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: Tickets
with tab2:
    st.subheader("Ticket Analytics")
    
    if tickets_df.empty:
        st.info("No tickets yet. Add some tickets to see charts!")
    else:
        # Show two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Tickets by Priority")
            # Count how many of each priority
            priority_counts = tickets_df['priority'].value_counts()
            # Make a pie chart
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                color=priority_counts.index,
                color_discrete_map={
                    'Critical': 'red',
                    'High': 'orange',
                    'Medium': 'yellow',
                    'Low': 'green'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Tickets by Status")
            # Count how many of each status
            status_counts = tickets_df['status'].value_counts()
            # Make a bar chart
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                labels={'x': 'Status', 'y': 'Count'},
                color=status_counts.values,
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Category chart
        st.markdown("#### Tickets by Category")
        category_counts = tickets_df['category'].value_counts()
        fig = px.bar(
            x=category_counts.index,
            y=category_counts.values,
            labels={'x': 'Category', 'y': 'Count'},
            color=category_counts.values,
            color_continuous_scale='Purples'
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: Datasets
with tab3:
    st.subheader("Dataset Analytics")
    
    if datasets_df.empty:
        st.info("No datasets yet. Add some datasets to see charts!")
    else:
        # Show summary numbers
        col1, col2 = st.columns(2)
        
        with col1:
            total_records = datasets_df['record_count'].sum()
            st.metric("📊 Total Records", f"{total_records:,}")
        
        with col2:
            total_size = datasets_df['file_size_mb'].sum()
            st.metric("💾 Total Size", f"{total_size:.1f} MB")
        
        st.divider()
        
        # Show two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Datasets by Category")
            # Count how many of each category
            category_counts = datasets_df['category'].value_counts()
            # Make a bar chart
            fig = px.bar(
                x=category_counts.index,
                y=category_counts.values,
                labels={'x': 'Category', 'y': 'Count'},
                color=category_counts.values,
                color_continuous_scale='Teal'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Top 5 Largest Datasets")
            # Get the 5 biggest datasets
            top5 = datasets_df.nlargest(5, 'file_size_mb')
            # Make a bar chart
            fig = px.bar(
                top5,
                x='dataset_name',
                y='file_size_mb',
                labels={'dataset_name': 'Dataset', 'file_size_mb': 'Size (MB)'},
                color='file_size_mb',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username}")
