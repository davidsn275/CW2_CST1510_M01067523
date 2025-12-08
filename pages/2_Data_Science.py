import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database_manager import DatabaseManager
from services.ai_assistant import AIAssistant
from models.dataset import Dataset

# Page setup
st.set_page_config(
    page_title="Data Science Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize DatabaseManager
db = DatabaseManager("DATA/intelligence_platform.db")
db.connect()

# Styling
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Tab styling - clean and appealing */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 20px;
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-color: #3b82f6;
        color: white !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stTabs [aria-selected="false"] {
        color: rgba(255, 255, 255, 0.7) !important;
    }
</style>
""", unsafe_allow_html=True)

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ You must be logged in to view this page")
    if st.button("🔐 Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Dashboard header
st.title("📊 Data Science Hub")
st.caption("Centralized dataset management and analytics platform")

# Load datasets using DatabaseManager and convert to Dataset objects
rows = db.get_all_datasets()
datasets = []
for row in rows:
    dataset = Dataset(
        dataset_id=row[0],
        name=row[1],
        category=row[2],
        source=row[3],
        last_updated=row[4],
        record_count=row[5] or 0,
        file_size_mb=row[6] or 0.0
    )
    datasets.append(dataset)

# Convert to DataFrame for display
df_datasets = pd.DataFrame([ds.to_dict() for ds in datasets]) if datasets else pd.DataFrame()

# Calculate metrics using objects
total_records = sum(ds.get_record_count() for ds in datasets)
total_size = sum(ds.get_file_size_mb() for ds in datasets)
avg_size = total_size / len(datasets) if datasets else 0
categories = set(ds.get_category() for ds in datasets)

# Display metrics in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📁 Total Datasets", len(datasets))

with col2:
    st.metric("📊 Total Records", f"{total_records:,}")

with col3:
    st.metric("💾 Storage Used", f"{total_size:.1f} MB")

with col4:
    st.metric("🏷️ Categories", len(categories))

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 View Data", "➕ Add Dataset", "📤 Upload CSV", "📊 Analytics & Insights", "🤖 AI Assistant"])

# Tab 1: View Data
with tab1:
    if len(df_datasets) > 0:
        # Time-series chart: Dataset uploads over time
        st.subheader("📈 Dataset Registrations Over Time")
        
        # Prepare time-series data
        df_datasets_copy = df_datasets.copy()
        if "last_updated" in df_datasets_copy.columns:
            df_datasets_copy['last_updated'] = pd.to_datetime(df_datasets_copy['last_updated'], errors='coerce')
            df_datasets_copy = df_datasets_copy.dropna(subset=['last_updated'])
            
            if len(df_datasets_copy) > 0:
                # Group by date and count datasets
                df_datasets_copy['date_only'] = df_datasets_copy['last_updated'].dt.date
                time_series = df_datasets_copy.groupby('date_only').size().reset_index(name='count')
                time_series.columns = ['Date', 'Datasets']
                time_series = time_series.sort_values('Date')
                time_series = time_series.set_index('Date')
                
                # Display line chart
                st.line_chart(time_series, color="#3b82f6", height=300)
            else:
                st.info("⚠️ Date information unavailable for time-series analysis")
        else:
            st.info("⚠️ Date information unavailable for time-series analysis")
        
        st.markdown("---")
        
        # Charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("📊 Datasets by Category")
            if "category" in df_datasets.columns:
                cat_counts = df_datasets["category"].value_counts().reset_index()
                cat_counts.columns = ["category", "count"]
                st.bar_chart(cat_counts.set_index("category"), color="#3b82f6", height=250)
        
        with chart_col2:
            st.subheader("💾 Storage by Dataset (MB)")
            if "file_size_mb" in df_datasets.columns and "dataset_name" in df_datasets.columns:
                size_data = df_datasets[["dataset_name", "file_size_mb"]].sort_values("file_size_mb", ascending=False).head(8)
                st.bar_chart(size_data.set_index("dataset_name"), color="#8b5cf6", height=250)
        
        st.markdown("---")
        
        # Data table
        st.subheader("📋 Dataset Inventory")
        st.dataframe(df_datasets, width='stretch', height=300)
    else:
        st.info("🔍 No datasets registered yet. Add your first dataset!")


# Tab 2: Add Dataset
with tab2:
    st.subheader("🆕 Register New Dataset")
    
    with st.form("dataset_form"):
        col1, col2 = st.columns(2)
        with col1:
            dataset_name = st.text_input("📛 Dataset Name")
            category = st.selectbox("📂 Category", ["Training Data", "Testing Data", "Raw Data", "Processed Data"])
            source = st.text_input("🔗 Source")
        with col2:
            last_updated = st.date_input("📅 Last Updated")
            record_count = st.number_input("📊 Record Count", min_value=0, step=1)
            file_size_mb = st.number_input("💾 File Size (MB)", min_value=0.0, step=0.1)
        
        submitted = st.form_submit_button("💾 Save Dataset")
    
    if submitted:
        if not dataset_name or not source:
            st.error("❌ Please fill in all required fields")
        else:
            # Use DatabaseManager to insert dataset
            db.insert_dataset(dataset_name, category, source, str(last_updated), int(record_count), float(file_size_mb))
            st.success("✅ Dataset registered successfully!")
            st.rerun()

# Tab 3: Upload CSV
with tab3:
    st.subheader("📁 Import CSV Data")
    st.info("📋 Required columns: dataset_name, category, source, last_updated, record_count, file_size_mb")
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv", key="dataset_upload")
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        st.dataframe(new_df.head(), width='stretch')
        
        if st.button("📥 Import Data"):
            for _, row in new_df.iterrows():
                db.insert_dataset(
                    str(row.get('dataset_name', '')),
                    str(row.get('category', '')),
                    str(row.get('source', '')),
                    str(row.get('last_updated', '')),
                    int(row.get('record_count', 0)),
                    float(row.get('file_size_mb', 0.0))
                )
            st.success(f"✅ Added {len(new_df)} datasets")
            st.rerun()

# Tab 4: Analytics & Insights
with tab4:
    st.subheader("🎯 High-Value Data Governance Analysis")
    st.info("Problem Statement: The team must manage a growing catalog of large datasets uploaded by various departments. Analyze resource consumption and data source dependency to recommend data governance and archiving policies.")
    
    if len(df_datasets) > 0:
        # Analysis 1: Resource Consumption Analysis
        st.markdown("### 💾 Storage Resource Consumption Analysis")
        
        total_storage = sum(ds.get_file_size_mb() for ds in datasets)
        total_records = sum(ds.get_record_count() for ds in datasets)
        avg_storage = total_storage / len(datasets) if datasets else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Storage (MB)", f"{total_storage:.1f} MB")
        with col2:
            st.metric("Average Dataset Size", f"{avg_storage:.2f} MB")
        with col3:
            st.metric("Total Records", f"{total_records:,}")
        
        # Storage by source (data source dependency)
        st.markdown("**Storage Consumption by Data Source:**")
        if "source" in df_datasets.columns:
            source_storage = df_datasets.groupby('source').agg({
                'file_size_mb': 'sum',
                'dataset_name': 'count'
            }).reset_index()
            source_storage.columns = ['Data Source', 'Total Storage (MB)', 'Dataset Count']
            source_storage = source_storage.sort_values('Total Storage (MB)', ascending=False)
            st.dataframe(source_storage, width='stretch', hide_index=True)
            
            # Visualize storage by source
            if len(source_storage) > 0:
                st.bar_chart(source_storage.set_index('Data Source')['Total Storage (MB)'], color="#3b82f6", height=300)
        
        st.markdown("---")
        
        # Analysis 2: Data Source Dependency Mapping
        st.markdown("### 🔗 Data Source Dependency Analysis")
        

        if "source" in df_datasets.columns:
            source_dependency = df_datasets.groupby('source').agg({
                'dataset_name': 'count',
                'file_size_mb': 'sum',
                'record_count': 'sum'
            }).reset_index()
            source_dependency.columns = ['Source', 'Datasets', 'Total Size (MB)', 'Total Records']
            source_dependency = source_dependency.sort_values('Datasets', ascending=False)
            
            st.markdown("**Dependency Score = Number of datasets × Storage size × Record count**")
            source_dependency['Dependency Score'] = (
                source_dependency['Datasets'] * 
                source_dependency['Total Size (MB)'] * 
                (source_dependency['Total Records'] / 1000)  # Normalize
            )
            source_dependency = source_dependency.sort_values('Dependency Score', ascending=False)
            st.dataframe(source_dependency, width='stretch', hide_index=True)
            
            # Identify critical dependencies
            critical_sources = source_dependency[source_dependency['Dependency Score'] > source_dependency['Dependency Score'].quantile(0.75)]
            if len(critical_sources) > 0:
                st.markdown("**⚠️ Critical Dependencies (Top 25% by dependency score):**")
                for _, row in critical_sources.iterrows():
                    st.markdown(f"- **{row['Source']}**: {int(row['Datasets'])} datasets, {row['Total Size (MB)']:.1f} MB")
    else:
        st.info("🔍 No datasets registered yet. Add datasets to see analytics insights.")

# Tab 5: AI Assistant
with tab5:

    # Build context from current data with full details
    if datasets:
        category_counts = {}
        for ds in datasets:
            cat = ds.get_category()
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Create detailed dataset information
        detailed_datasets = "\n".join([
            f"""
Dataset ID: {ds.get_id()}
Name: {ds.get_name()}
Category: {ds.get_category()}
Source: {ds.get_source()}
Last Updated: {ds.get_last_updated()}
Record Count: {ds.get_record_count():,}
File Size: {ds.get_file_size_mb():.2f} MB
---"""
            for ds in datasets
        ])
        
        DATA_CONTEXT = f"""
CURRENT DASHBOARD DATA:
- Total Datasets: {len(datasets)}
- Total Records: {total_records:,}
- Total Storage: {total_size:.1f} MB
- By Category: {category_counts}

DETAILED DATASET INFORMATION (with full details):
{detailed_datasets}

Note: You have access to complete dataset details including IDs, names, categories, sources, update dates, record counts, and file sizes. Use this information to answer questions about specific datasets and provide detailed analysis.
"""
        
    else:
        DATA_CONTEXT = "\nCURRENT DASHBOARD DATA: No datasets registered yet.\n"
    
    # System prompt for AI
    SYSTEM_PROMPT = f"""You are a friendly data science expert assistant with access to detailed dataset information.

{DATA_CONTEXT}

Responsibilities:
- Answer questions about specific datasets using their ID, name, category, source, and other details
- Provide detailed analysis of datasets including their current status, size, and record counts
- Suggest analysis and ML approaches based on dataset characteristics
- Explain data science concepts
- When asked about a specific dataset, provide its full details including source, category, and size

IMPORTANT: You have access to complete dataset information including:
- Dataset IDs (use these to reference specific datasets)
- Names, categories, and sources
- Last updated dates
- Record counts and file sizes

Always refer to actual dataset data when answering questions. Be specific and detailed when discussing datasets."""
    
    # Initialize AIAssistant
    ai = AIAssistant(system_prompt=SYSTEM_PROMPT, history_key="ds_chat_history")
    
    if not ai.is_configured():
        st.warning("⚠️ AI Assistant is not available")
        
        # Check if API key exists
        try:
            api_key = st.secrets.get("GOOGLE_API_KEY")
            if not api_key:
                st.error("❌ **API Key Missing**\n\nPlease add your Google API key to `.streamlit/secrets.toml`")
                st.code('GOOGLE_API_KEY = "your-api-key-here"', language="toml")
            else:
                # API key exists but model failed to initialize
                error_msg = st.session_state.get("api_error", "Unknown error")
                st.error(f"❌ **API Configuration Error**\n\n{error_msg}\n\n**Possible causes:**\n- Invalid API key\n- Quota exceeded\n- Model unavailable\n\n**Solutions:**\n- Verify your API key at [Google AI Studio](https://aistudio.google.com/)\n- Check your [API usage](https://ai.dev/usage?tab=rate-limit)\n- Try again later")
        except Exception as e:
            st.error(f"❌ **Configuration Error:** {str(e)}")
            st.info("💡 Make sure `.streamlit/secrets.toml` exists with your API key")

    else:
        # AI header with clear button
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown("### 🧠 Data Science AI Assistant")
            st.caption("Ask about datasets, analysis, or machine learning")
        with col_h2:
            if st.button("🗑️ Clear", key="ds_clear"):
                ai.clear_history()
                st.rerun()
        

        st.markdown("---")
        
        # Welcome message
        if len(ai.get_history()) == 0:
            st.write("👋 Welcome! I'm your Data Science Assistant")
            st.write("I can help with data analysis, ML recommendations, and dataset insights.")
        
        # Display chat history
        for msg in ai.get_history():
            role = "user" if msg["role"] == "user" else "assistant"
            with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🧠"):
                st.markdown(msg["content"])
        
        # Handle user input
        user_input = st.chat_input("💬 Ask about data science...")
        
        if user_input:
            # Show user message
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(user_input)
            
            # Get AI response with streaming
            with st.chat_message("assistant", avatar="🧠"):
                container = st.empty()
                ai.send_message_stream(user_input, container)


# Sign out button
st.markdown("---")
if st.button("🚪 Sign Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("Home.py")
    
