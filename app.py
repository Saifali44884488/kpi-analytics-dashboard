import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta
import io

# Page config
st.set_page_config(page_title="QuickShop Analytics", page_icon="📊", layout="wide")

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'last_upload' not in st.session_state:
    st.session_state.last_upload = None

st.title("📊 QuickShop Analytics Dashboard")
st.markdown("**Enterprise-grade analytics dashboard with real-time insights**")

# CACHED SAMPLE DATA FUNCTION (improves performance!)
@st.cache_data
def create_sample_data():
    """Create sample business data - cached for better performance"""
    data = {
        'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
        'Visitors': [1500 + i*50 + (i%7)*200 for i in range(30)],
        'Orders': [150 + i*5 + (i%7)*20 for i in range(30)],
        'Revenue': [15000 + i*500 + (i%7)*2000 for i in range(30)],
        'Segment': ['Mobile' if i%2 == 0 else 'Desktop' for i in range(30)]
    }
    return pd.DataFrame(data)

# CACHED DATA PROCESSING
@st.cache_data
def process_uploaded_data(uploaded_file):
    """Process uploaded CSV with caching for performance"""
    try:
        df = pd.read_csv(uploaded_file)
        df['Date'] = pd.to_datetime(df['Date'])
        return df, None
    except Exception as e:
        return None, str(e)

# SIDEBAR - DATA SOURCE
st.sidebar.header("📁 Data Management")

data_source = st.sidebar.radio(
    "Choose your data source:",
    ("📊 Use Sample Data", "📁 Upload CSV File"),
    key="data_source_radio"
)

df = None
data_info = ""

if data_source == "📊 Use Sample Data":
    df = create_sample_data()
    data_info = f"Sample dataset: {len(df)} rows, {(df['Date'].max() - df['Date'].min()).days + 1} days"
    st.sidebar.success("✅ Sample data loaded")
    
    # Download sample format
    sample_csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Download Sample Format",
        data=sample_csv,
        file_name="quickshop_sample_data.csv",
        mime="text/csv",
        help="Download this file to see the expected CSV format"
    )

else:  # Upload CSV File
    uploaded_file = st.sidebar.file_uploader(
        "📁 Upload your CSV file", 
        type="csv",
        help="Required columns: Date, Visitors, Orders, Revenue, Segment",
        key="csv_uploader"
    )
    
    if uploaded_file is not None:
        # Check if this is a new file
        if st.session_state.last_upload != uploaded_file.name:
            with st.sidebar.spinner("Processing your data..."):
                df, error = process_uploaded_data(uploaded_file)
                st.session_state.last_upload = uploaded_file.name
        else:
            df, error = process_uploaded_data(uploaded_file)
        
        if error:
            st.sidebar.error(f"❌ Error: {error}")
        elif df is not None:
            # Validate columns
            required_cols = ['Date', 'Visitors', 'Orders', 'Revenue', 'Segment']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.sidebar.error(f"❌ Missing columns: {', '.join(missing_cols)}")
                st.sidebar.markdown("**Required columns:**")
                for col in required_cols:
                    st.sidebar.markdown(f"• {col}")
                df = None
            else:
                data_info = f"Your data: {len(df)} rows, {len(df['Segment'].unique())} segments"
                st.sidebar.success("✅ Data loaded successfully!")
                st.session_state.data_loaded = True

# MAIN DASHBOARD - ONLY IF DATA EXISTS
if df is not None:
    # DATA INFO
    st.info(f"📈 {data_info}")
    
    # ADVANCED FILTERS
    st.sidebar.header("🎛️ Dashboard Controls")
    
    # Smart date defaults
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    default_start = max_date - timedelta(days=7)  # Last week by default
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start Date", max(default_start, min_date), min_value=min_date, max_value=max_date)
    with col2:
        end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
    
    # Segment filter with select all/none
    available_segments = sorted(df['Segment'].unique().tolist())
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Select All", key="select_all"):
            st.session_state.selected_segments = available_segments
    with col2:
        if st.button("Clear All", key="clear_all"):
            st.session_state.selected_segments = []
    
    if 'selected_segments' not in st.session_state:
        st.session_state.selected_segments = available_segments
        
    segments = st.sidebar.multiselect(
        "📱 Segments",
        options=available_segments,
        default=st.session_state.selected_segments,
        key="segments_multiselect"
    )
    
    # Update session state
    st.session_state.selected_segments = segments
    
    # FILTER DATA
    filtered_df = df[
        (df['Date'].dt.date >= start_date) & 
        (df['Date'].dt.date <= end_date) &
        (df['Segment'].isin(segments))
    ]
    
    if len(filtered_df) > 0:
        # KEY METRICS WITH TRENDS
        st.subheader("📊 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_visitors = filtered_df['Visitors'].sum()
            avg_daily_visitors = filtered_df['Visitors'].mean()
            st.metric(
                "👥 Total Visitors", 
                f"{total_visitors:,}",
                delta=f"{avg_daily_visitors:.0f} avg/day"
            )
        
        with col2:
            total_orders = filtered_df['Orders'].sum()
            avg_daily_orders = filtered_df['Orders'].mean()
            st.metric(
                "🛒 Total Orders", 
                f"{total_orders:,}",
                delta=f"{avg_daily_orders:.0f} avg/day"
            )
        
        with col3:
            total_revenue = filtered_df['Revenue'].sum()
            avg_daily_revenue = filtered_df['Revenue'].mean()
            st.metric(
                "💰 Total Revenue", 
                f"${total_revenue:,}",
                delta=f"${avg_daily_revenue:,.0f} avg/day"
            )
        
        with col4:
            conversion_rate = (total_orders / total_visitors * 100) if total_visitors > 0 else 0
            avg_order_value = (total_revenue / total_orders) if total_orders > 0 else 0
            st.metric(
                "📈 Conversion Rate", 
                f"{conversion_rate:.1f}%",
                delta=f"${avg_order_value:.0f} AOV"
            )
        
        st.divider()
        
        # VISUALIZATIONS
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Performance Trends")
            
            # Multi-metric line chart
            chart_df = filtered_df.melt(
                id_vars=['Date', 'Segment'], 
                value_vars=['Visitors', 'Orders', 'Revenue'],
                var_name='Metric', 
                value_name='Value'
            )
            
            metric_choice = st.selectbox(
                "Select metric to visualize:",
                ["Revenue", "Visitors", "Orders"],
                key="metric_selector"
            )
            
            chart_data = filtered_df if metric_choice else filtered_df
            fig = px.line(
                filtered_df, 
                x='Date', 
                y=metric_choice, 
                color='Segment',
                title=f"{metric_choice} Over Time by Segment"
            )
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Segment Analysis")
            
            analysis_type = st.radio(
                "Analysis type:",
                ["Distribution", "Performance"],
                horizontal=True,
                key="analysis_radio"
            )
            
            if analysis_type == "Distribution":
                segment_data = filtered_df.groupby('Segment')['Visitors'].sum().reset_index()
                fig = px.pie(
                    segment_data, 
                    values='Visitors', 
                    names='Segment',
                    title="Visitor Distribution by Segment"
                )
            else:
                segment_data = filtered_df.groupby('Segment').agg({
                    'Revenue': 'sum',
                    'Orders': 'sum',
                    'Visitors': 'sum'
                }).reset_index()
                segment_data['Conversion Rate'] = (segment_data['Orders'] / segment_data['Visitors'] * 100)
                
                fig = px.bar(
                    segment_data, 
                    x='Segment', 
                    y='Conversion Rate',
                    title="Conversion Rate by Segment",
                    text='Conversion Rate'
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            
            st.plotly_chart(fig, use_container_width=True)
        
        # DETAILED DATA TABLE
        with st.expander("📋 View Detailed Data", expanded=False):
            st.dataframe(
                filtered_df.sort_values('Date', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        
        # EXPORT OPTIONS
        st.subheader("📤 Export & Share")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Regular CSV export
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Raw Data",
                data=csv_data,
                file_name=f"dashboard_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Summary report
            summary_data = {
                'Metric': ['Total Visitors', 'Total Orders', 'Total Revenue', 'Conversion Rate', 'Avg Order Value'],
                'Value': [
                    f"{total_visitors:,}",
                    f"{total_orders:,}", 
                    f"${total_revenue:,}",
                    f"{conversion_rate:.1f}%",
                    f"${avg_order_value:.2f}"
                ],
                'Period': [f"{start_date} to {end_date}"] * 5
            }
            summary_df = pd.DataFrame(summary_data)
            summary_csv = summary_df.to_csv(index=False)
            
            st.download_button(
                label="📊 Export Summary Report",
                data=summary_csv,
                file_name=f"weekly_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col3:
            # Segment breakdown
            segment_summary = filtered_df.groupby('Segment').agg({
                'Visitors': 'sum',
                'Orders': 'sum', 
                'Revenue': 'sum'
            }).reset_index()
            segment_summary['Conversion Rate'] = (segment_summary['Orders'] / segment_summary['Visitors'] * 100).round(2)
            segment_csv = segment_summary.to_csv(index=False)
            
            st.download_button(
                label="🎯 Export Segment Analysis",
                data=segment_csv,
                file_name=f"segment_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    else:
        st.warning("⚠️ No data matches your current filters. Try adjusting your date range or segments.")

else:
    # WELCOME SCREEN
    st.markdown("## 🚀 Welcome to QuickShop Analytics!")
    
    st.markdown("""
    ### Get started in seconds:
    
    **Option 1: Try with sample data** 📊
    - Click "Use Sample Data" in the sidebar
    - Explore 30 days of realistic e-commerce data
    - Test all dashboard features instantly
    
    **Option 2: Upload your own data** 📁  
    - Click "Upload CSV File" in the sidebar
    - Your CSV needs these columns: `Date`, `Visitors`, `Orders`, `Revenue`, `Segment`
    - Download the sample format to see the exact structure needed
    
    ### 🎯 Dashboard Features:
    - **Real-time filtering** by date ranges and segments
    - **Interactive visualizations** with multiple chart types
    - **Key performance indicators** with trend analysis
    - **Export capabilities** for reports and data sharing
    - **Professional UI** optimized for business users
    """)
    
    # Show sample data structure
    with st.expander("👀 Preview: Expected Data Format"):
        sample_preview = create_sample_data().head()
        st.dataframe(sample_preview, use_container_width=True)

# FOOTER
st.markdown("---")
st.markdown("*🏆 Professional Analytics Dashboard • Built with Streamlit • Ready for Production*")