# Week 9 - Analytics Page
# Data visualization and charts

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.data.db import connect_database

# Page configuration
st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please login first!")
    st.info("👈 Go to Home page to login")
    st.stop()

# Fetch data functions
def get_incidents_data():
    conn = connect_database()
    query = "SELECT * FROM cyber_incidents"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_datasets_data():
    conn = connect_database()
    query = "SELECT * FROM datasets_metadata"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_tickets_data():
    conn = connect_database()
    query = "SELECT * FROM it_tickets"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Main page
st.title("📈 Analytics & Visualization")
st.markdown("Visualize data from all modules")

# Section selector
analysis_type = st.selectbox(
    "Select Analysis Type",
    ["Overview", "Cyber Incidents", "Datasets", "IT Tickets"]
)

# OVERVIEW SECTION
if analysis_type == "Overview":
    st.subheader("📊 System Overview")
    
    try:
        # Get all data
        incidents_df = get_incidents_data()
        datasets_df = get_datasets_data()
        tickets_df = get_tickets_data()
        
        # Create metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🚨 Total Incidents", len(incidents_df))
        with col2:
            st.metric("📁 Total Datasets", len(datasets_df))
        with col3:
            st.metric("🎫 Total Tickets", len(tickets_df))
        
        st.markdown("---")
        
        # Create overview charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Data distribution pie chart
            data_counts = pd.DataFrame({
                'Category': ['Incidents', 'Datasets', 'Tickets'],
                'Count': [len(incidents_df), len(datasets_df), len(tickets_df)]
            })
            
            fig = px.pie(data_counts, values='Count', names='Category', 
                        title='Data Distribution Across Modules')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Status summary
            st.markdown("### 📋 Quick Stats")
            st.info(f"**Incidents:** {len(incidents_df)} records")
            st.info(f"**Datasets:** {len(datasets_df)} records")
            st.info(f"**Tickets:** {len(tickets_df)} records")
            total = len(incidents_df) + len(datasets_df) + len(tickets_df)
            st.success(f"**Total Records:** {total}")
    
    except Exception as e:
        st.error(f"Error loading overview: {e}")

# CYBER INCIDENTS SECTION
elif analysis_type == "Cyber Incidents":
    st.subheader("🚨 Cyber Incidents Analytics")
    
    try:
        df = get_incidents_data()
        
        if df.empty:
            st.info("No incident data available.")
        else:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Incidents", len(df))
            with col2:
                critical_count = len(df[df['severity'] == 'Critical'])
                st.metric("Critical", critical_count)
            with col3:
                high_count = len(df[df['severity'] == 'High'])
                st.metric("High", high_count)
            with col4:
                medium_count = len(df[df['severity'] == 'Medium'])
                st.metric("Medium", medium_count)
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Incidents by severity
                severity_counts = df['severity'].value_counts().reset_index()
                severity_counts.columns = ['Severity', 'Count']
                
                fig1 = px.bar(severity_counts, x='Severity', y='Count',
                             title='Incidents by Severity',
                             color='Severity',
                             color_discrete_map={
                                 'Critical': '#dc3545',
                                 'High': '#fd7e14',
                                 'Medium': '#ffc107',
                                 'Low': '#28a745'
                             })
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Incidents by type
                type_counts = df['incident_type'].value_counts().reset_index()
                type_counts.columns = ['Type', 'Count']
                
                fig2 = px.pie(type_counts, values='Count', names='Type',
                             title='Incidents by Type')
                st.plotly_chart(fig2, use_container_width=True)
            
            # Timeline
            st.markdown("### 📅 Incident Timeline")
            df['incident_date'] = pd.to_datetime(df['incident_date'])
            df_sorted = df.sort_values('incident_date')
            
            fig3 = px.scatter(df_sorted, x='incident_date', y='severity',
                            color='incident_type', size_max=15,
                            title='Incident Timeline',
                            labels={'incident_date': 'Date', 'severity': 'Severity'})
            st.plotly_chart(fig3, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading incident analytics: {e}")

# DATASETS SECTION
elif analysis_type == "Datasets":
    st.subheader("📁 Dataset Analytics")
    
    try:
        df = get_datasets_data()
        
        if df.empty:
            st.info("No dataset data available.")
        else:
            # Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Datasets", len(df))
            with col2:
                unique_types = df['data_type'].nunique()
                st.metric("Data Types", unique_types)
            with col3:
                unique_sources = df['source'].nunique()
                st.metric("Unique Sources", unique_sources)
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Datasets by type
                type_counts = df['data_type'].value_counts().reset_index()
                type_counts.columns = ['Type', 'Count']
                
                fig1 = px.bar(type_counts, x='Type', y='Count',
                             title='Datasets by Type',
                             color='Type')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Datasets by source
                source_counts = df['source'].value_counts().head(10).reset_index()
                source_counts.columns = ['Source', 'Count']
                
                fig2 = px.pie(source_counts, values='Count', names='Source',
                             title='Top 10 Dataset Sources')
                st.plotly_chart(fig2, use_container_width=True)
            
            # Timeline
            st.markdown("### 📅 Dataset Collection Timeline")
            df['collection_date'] = pd.to_datetime(df['collection_date'])
            df_sorted = df.sort_values('collection_date')
            
            # Count by month
            df['month'] = df_sorted['collection_date'].dt.to_period('M').astype(str)
            monthly_counts = df.groupby('month').size().reset_index(name='count')
            
            fig3 = px.line(monthly_counts, x='month', y='count',
                          title='Datasets Collected Over Time',
                          labels={'month': 'Month', 'count': 'Number of Datasets'})
            st.plotly_chart(fig3, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading dataset analytics: {e}")

# IT TICKETS SECTION
elif analysis_type == "IT Tickets":
    st.subheader("🎫 IT Tickets Analytics")
    
    try:
        df = get_tickets_data()
        
        if df.empty:
            st.info("No ticket data available.")
        else:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Tickets", len(df))
            with col2:
                open_count = len(df[df['status'] == 'Open'])
                st.metric("Open", open_count)
            with col3:
                in_progress = len(df[df['status'] == 'In Progress'])
                st.metric("In Progress", in_progress)
            with col4:
                resolved = len(df[df['status'] == 'Resolved'])
                st.metric("Resolved", resolved)
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Tickets by status
                status_counts = df['status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                
                fig1 = px.bar(status_counts, x='Status', y='Count',
                             title='Tickets by Status',
                             color='Status',
                             color_discrete_map={
                                 'Open': '#ffc107',
                                 'In Progress': '#17a2b8',
                                 'Resolved': '#28a745',
                                 'Closed': '#6c757d'
                             })
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Tickets by priority
                priority_counts = df['priority'].value_counts().reset_index()
                priority_counts.columns = ['Priority', 'Count']
                
                fig2 = px.pie(priority_counts, values='Count', names='Priority',
                             title='Tickets by Priority',
                             color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Status by Priority
            st.markdown("### 📊 Status Distribution by Priority")
            priority_status = df.groupby(['priority', 'status']).size().reset_index(name='count')
            
            fig3 = px.bar(priority_status, x='priority', y='count', color='status',
                         title='Ticket Status by Priority',
                         labels={'priority': 'Priority', 'count': 'Number of Tickets'},
                         barmode='group')
            st.plotly_chart(fig3, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading ticket analytics: {e}")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username}")
