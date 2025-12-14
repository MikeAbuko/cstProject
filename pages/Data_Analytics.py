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
        
        st.divider()
        
        # Phishing Spike Detection
        st.markdown("#### 📈 Incident Trends Over Time (Phishing Surge Analysis)")
        
        # Convert date to datetime for plotting
        incidents_df['date'] = pd.to_datetime(incidents_df['date'])
        
        # Count incidents by date and type
        daily_incidents = incidents_df.groupby([pd.Grouper(key='date', freq='W'), 'incident_type']).size().reset_index(name='count')
        
        # Create time series chart
        fig = px.line(
            daily_incidents, 
            x='date', 
            y='count', 
            color='incident_type',
            labels={'date': 'Week', 'count': 'Number of Incidents'},
            title='Weekly Incident Trends - Identifying Threat Surges'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # KEY INSIGHT
        phishing_count = incidents_df[incidents_df['incident_type'] == 'Phishing'].shape[0]
        total_count = len(incidents_df)
        phishing_percent = (phishing_count / total_count * 100) if total_count > 0 else 0
        st.warning(f"⚠️ **Key Finding:** Phishing incidents account for {phishing_count} cases ({phishing_percent:.1f}% of all incidents), showing a focused surge requiring immediate attention.")
        
        st.divider()
        
        # Resolution Time Bottleneck
        st.markdown("#### ⏱️ Resolution Time Bottleneck Analysis")
        
        # Check if resolved_date column exists
        if 'resolved_date' in incidents_df.columns:
            # Filter for resolved incidents
            resolved = incidents_df[incidents_df['status'].isin(['Resolved', 'Closed'])].copy()
            
            if not resolved.empty:
                # Convert dates to datetime
                resolved['date'] = pd.to_datetime(resolved['date'])
                resolved['resolved_date'] = pd.to_datetime(resolved['resolved_date'])
                
                # Calculate resolution time in days
                resolved['resolution_days'] = (resolved['resolved_date'] - resolved['date']).dt.days
                
                # Average resolution time by incident type
                avg_resolution = resolved.groupby('incident_type')['resolution_days'].mean().sort_values(ascending=False)
                
                # Create bar chart
                fig = px.bar(
                    x=avg_resolution.index,
                    y=avg_resolution.values,
                    labels={'x': 'Incident Type', 'y': 'Average Days to Resolve'},
                    title='Resolution Time Bottleneck - Which Threats Take Longest?',
                    color=avg_resolution.values,
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Identify the bottleneck
                if len(avg_resolution) > 0:
                    slowest_type = avg_resolution.index[0]
                    slowest_days = avg_resolution.values[0]
                    if len(avg_resolution) > 1:
                        fastest_type = avg_resolution.index[-1]
                        fastest_days = avg_resolution.values[-1]
                        multiplier = slowest_days / fastest_days if fastest_days > 0 else 1
                        st.error(f"🚨 **Critical Bottleneck:** {slowest_type} incidents take an average of {slowest_days:.1f} days to resolve - {multiplier:.1f}x longer than {fastest_type} incidents ({fastest_days:.1f} days).")
                    else:
                        st.info(f"Average resolution time for {slowest_type}: {slowest_days:.1f} days")
        
        # Show unresolved backlog
        st.markdown("#### 📊 Unresolved Incident Backlog")
        unresolved = incidents_df[~incidents_df['status'].isin(['Resolved', 'Closed'])]
        
        if not unresolved.empty:
            backlog_by_type = unresolved.groupby(['incident_type', 'severity']).size().reset_index(name='backlog_count')
            
            fig = px.bar(
                backlog_by_type,
                x='incident_type',
                y='backlog_count',
                color='severity',
                title='Unresolved Incident Backlog by Type and Severity',
                labels={'backlog_count': 'Open Cases', 'incident_type': 'Threat Type'},
                color_discrete_map={
                    'Critical': 'red',
                    'High': 'orange',
                    'Medium': 'yellow',
                    'Low': 'green'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # KEY INSIGHT
            high_severity_backlog = unresolved[unresolved['severity'].isin(['High', 'Critical'])].shape[0]
            st.warning(f"⚠️ **Backlog Alert:** {high_severity_backlog} high-severity incidents remain unresolved, creating a response bottleneck that delays threat mitigation.")
        else:
            st.success("✅ No unresolved incidents - Great work!")

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
        
        st.divider()
        
        # Staff Performance
        st.markdown("#### 👥 Staff Performance Analysis")
        
        if 'assigned_to' in tickets_df.columns:
            # Count tickets by staff member and status
            staff_workload = tickets_df.groupby(['assigned_to', 'status']).size().reset_index(name='ticket_count')
            
            fig = px.bar(
                staff_workload,
                x='assigned_to',
                y='ticket_count',
                color='status',
                title='Ticket Distribution by Staff Member',
                labels={'assigned_to': 'Staff Member', 'ticket_count': 'Tickets'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Look for performance anomaly
            open_by_staff = tickets_df[tickets_df['status'] == 'Open'].groupby('assigned_to').size()
            if not open_by_staff.empty:
                slowest_staff = open_by_staff.idxmax()
                slowest_count = open_by_staff.max()
                avg_open = open_by_staff.mean()
                st.warning(f"⚠️ **Performance Anomaly:** {slowest_staff} has {slowest_count} open tickets, compared to team average of {avg_open:.1f}, suggesting their might be a potential workload imbalance or process delays.")
        
        st.divider()
        
        # Resolution Time by Staff
        st.markdown("#### ⏱️ Ticket Resolution Time Analysis")
        
        if 'resolved_date' in tickets_df.columns and 'created_date' in tickets_df.columns:
            # Filter resolved tickets
            resolved_tickets = tickets_df[tickets_df['status'] == 'Closed'].copy()
            
            if not resolved_tickets.empty:
                # Convert to datetime and calculate resolution time
                resolved_tickets['created_date'] = pd.to_datetime(resolved_tickets['created_date'])
                resolved_tickets['resolved_date'] = pd.to_datetime(resolved_tickets['resolved_date'])
                resolved_tickets['resolution_days'] = (resolved_tickets['resolved_date'] - resolved_tickets['created_date']).dt.days
                
                # Average resolution time by staff member
                if 'assigned_to' in resolved_tickets.columns:
                    avg_by_staff = resolved_tickets.groupby('assigned_to')['resolution_days'].mean().sort_values(ascending=False)
                    
                    if not avg_by_staff.empty:
                        fig = px.bar(
                            x=avg_by_staff.index,
                            y=avg_by_staff.values,
                            labels={'x': 'Staff Member', 'y': 'Average Days to Close'},
                            title='Staff Performance: Average Ticket Resolution Time',
                            color=avg_by_staff.values,
                            color_continuous_scale='Reds'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Identify performance differences
                        slowest_staff = avg_by_staff.index[0]
                        slowest_time = avg_by_staff.values[0]
                        team_average = avg_by_staff.mean()
                        
                        if slowest_time > team_average * 1.2:
                            st.error(f"🚨 **Performance Anomaly Detected:** {slowest_staff} average resolution time is {slowest_time:.1f} days - {slowest_time/team_average:.1f}x slower than the teams average ({team_average:.1f} days). This requires immediate investigation.")
                        else:
                            st.success(f"✅ Team performance is balanced. Average resolution time: {team_average:.1f} days")
            else:
                st.info("No closed tickets yet to analyze resolution time")

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
        
        st.divider()
        
        # Data Governance & Resource Management
        st.markdown("#### 🗄️ Data Governance & Resource Management")
        
        # Identify large datasets
        large_datasets = datasets_df[datasets_df['file_size_mb'] > 100]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Datasets >100MB", len(large_datasets))
            st.metric("Storage Consumed", f"{large_datasets['file_size_mb'].sum():.1f} MB")
        
        with col2:
            # Resource by source
            if 'source' in datasets_df.columns:
                source_consumption = datasets_df.groupby('source')['file_size_mb'].sum().sort_values(ascending=False)
                if not source_consumption.empty:
                    st.metric("Top Source", source_consumption.index[0])
                    st.metric("Source Storage", f"{source_consumption.iloc[0]:.1f} MB")
                    
                    # Show chart of consumption by source
                    st.markdown("##### Resource Consumption by Data Source")
                    fig = px.pie(
                        values=source_consumption.values,
                        names=source_consumption.index,
                        title='Storage Usage by Department/Source'
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Governance Recommendation
        if len(large_datasets) > 0:
            st.info(f"📋 **Governance Recommendation:** Consider archiving {len(large_datasets)} datasets exceeding 100MB to optimize storage. Review datasets from high-consumption sources.")
        
        # Data quality check
        st.markdown("##### Data Quality Analysis")
        # Check for datasets with unusually low record count for their size
        datasets_df['bytes_per_record'] = (datasets_df['file_size_mb'] * 1024 * 1024) / datasets_df['record_count']
        quality_issues = datasets_df[datasets_df['bytes_per_record'] > 10000]  # More than 10KB per record is unusual
        
        if not quality_issues.empty:
            st.warning(f"⚠️ **Quality Alert:** {len(quality_issues)} datasets have unusually large file size relative to record counts, suggesting potential data quality issues or need to improve.")
        else:
            st.success("✅ All datasets show normal ratios")

# Footer
st.markdown("---")
st.caption(f"🔐 Logged in as: {st.session_state.username} | Powered by AngryPanda🐼")
