import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database_manager import DatabaseManager
from services.ai_assistant import AIAssistant
from models.security_incident import SecurityIncident

# Page setup
st.set_page_config(
    page_title="Cybersecurity Dashboard",
    page_icon="🔒",
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
        background: linear-gradient(135deg, #ef4444, #f97316);
        border-color: #ef4444;
        color: white !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
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
st.title("🔒 Cybersecurity Command Centre")
st.caption("Real-time threat monitoring and incident management")

# Load incidents using DatabaseManager and convert to SecurityIncident objects
rows = db.get_all_incidents()
incidents = []
for row in rows:
    incident = SecurityIncident(
        incident_id=row[0],
        date=row[1],
        incident_type=row[2],
        severity=row[3],
        status=row[4],
        description=row[5]
    )
    incidents.append(incident)


# Convert to DataFrame for display
df_incidents = pd.DataFrame([inc.to_dict() for inc in incidents]) if incidents else pd.DataFrame()

# Calculate metrics using objects
critical_count = sum(1 for inc in incidents if inc.get_severity().lower() == "critical")
high_count = sum(1 for inc in incidents if inc.get_severity().lower() == "high")
open_count = sum(1 for inc in incidents if inc.get_status().lower() == "open")

# Display metrics in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🚨 Critical", critical_count)

with col2:
    st.metric("⚠️ High Severity", high_count)

with col3:
    st.metric("📂 Open Cases", open_count)

with col4:
    st.metric("📊 Total Incidents", len(incidents))

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 View Data", "➕ Add Incident", "📤 Upload CSV", "📊 Analytics & Insights", "🤖 AI Assistant"])

# Tab 1: View Data
with tab1:
    if len(df_incidents) > 0:
        # Time-series chart: Incidents over time
        st.subheader("📈 Incidents Over Time")
        
        # Prepare time-series data
        df_incidents_copy = df_incidents.copy()
        df_incidents_copy['date'] = pd.to_datetime(df_incidents_copy['date'], errors='coerce')
        df_incidents_copy = df_incidents_copy.dropna(subset=['date'])
        
        if len(df_incidents_copy) > 0:
            # Group by date and count incidents
            df_incidents_copy['date_only'] = df_incidents_copy['date'].dt.date
            time_series = df_incidents_copy.groupby('date_only').size().reset_index(name='count')
            time_series.columns = ['Date', 'Incidents']
            time_series = time_series.sort_values('Date')
            time_series = time_series.set_index('Date')
            
            # Display line chart
            st.line_chart(time_series, color="#ef4444", height=300)
        else:
            st.info("⚠️ Date information unavailable for time-series analysis")
        
        st.markdown("---")
        
        # Bar chart: Incidents by Severity
        st.subheader("📊 Incidents by Severity")
        severity_counts = df_incidents["severity"].value_counts().reset_index()
        severity_counts.columns = ["severity", "count"]
        st.bar_chart(severity_counts.set_index("severity"), color="#ef4444")
        
        st.markdown("---")
        
        # Data table
        st.subheader("📋 All Incidents")
        st.dataframe(df_incidents, width='stretch', height=350)
    else:
        st.info("🔍 No incidents recorded yet. Add one to get started!")


# Tab 2: Add Incident
with tab2:
    st.subheader("🆕 Report New Incident")
    
    with st.form("incident_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("📅 Date")
            incident_type = st.selectbox("🎯 Incident Type", ["Malware", "Phishing", "DDoS", "Ransomware", "Data Breach"])
            severity = st.selectbox("⚡ Severity", ["Low", "Medium", "High", "Critical"])
        with col2:
            status = st.selectbox("📌 Status", ["Open", "In Progress", "Resolved", "Closed"])
            description = st.text_area("📝 Description", height=130)
        
        submitted = st.form_submit_button("🚀 Submit Incident")
    
    if submitted:
        if not description:
            st.error("❌ Please provide a description")
        else:
            # Use DatabaseManager to insert incident
            db.insert_incident(str(date), incident_type, severity, status, description)
            st.success("✅ Incident reported successfully!")
            st.rerun()

# Tab 3: Upload CSV
with tab3:
    st.subheader("📁 Import CSV Data")
    st.info("📋 Required columns: date, incident_type, severity, status, description")
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv", key="incident_upload")
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        st.dataframe(new_df.head(), width='stretch')
        
        if st.button("📥 Import Data"):
            for _, row in new_df.iterrows():
                db.insert_incident(
                    str(row.get('date', '')),
                    str(row.get('incident_type', '')),
                    str(row.get('severity', '')),
                    str(row.get('status', '')),
                    str(row.get('description', ''))
                )

            st.success(f"✅ Added {len(new_df)} incidents")
            st.rerun()

# Tab 4: Analytics & Insights
with tab4:
    st.subheader("🎯 High-Value Security Analysis")
    
    if len(df_incidents) > 0:
        # Analysis 1: Phishing Surge Detection
        st.markdown("### 🎣 Phishing Threat Analysis")
        

        phishing_incidents = df_incidents[df_incidents['incident_type'].str.contains('Phishing', case=False, na=False)]
        total_phishing = len(phishing_incidents)
        total_incidents = len(df_incidents)
        phishing_percentage = (total_phishing / total_incidents * 100) if total_incidents > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Phishing Incidents", total_phishing)
        with col2:
            st.metric("Phishing % of Total", f"{phishing_percentage:.1f}%")
        with col3:
            unresolved_phishing = len(phishing_incidents[phishing_incidents['status'].isin(['Open', 'In Progress'])])
            st.metric("Unresolved Phishing", unresolved_phishing, delta=None)
        
        if total_phishing > 0:
            # Phishing trend over time
            phishing_trend = phishing_incidents.copy()
            phishing_trend['date'] = pd.to_datetime(phishing_trend['date'], errors='coerce')
            phishing_trend = phishing_trend.dropna(subset=['date'])
            if len(phishing_trend) > 0:
                phishing_trend['date_only'] = phishing_trend['date'].dt.date
                phishing_time_series = phishing_trend.groupby('date_only').size().reset_index(name='count')
                phishing_time_series.columns = ['Date', 'Phishing Incidents']
                phishing_time_series = phishing_time_series.sort_values('Date')
                phishing_time_series = phishing_time_series.set_index('Date')
                st.line_chart(phishing_time_series, color="#ef4444", height=250)
            

            # Phishing by severity
            st.markdown("**Phishing Incidents by Severity:**")
            phishing_severity = phishing_incidents['severity'].value_counts().reset_index()
            phishing_severity.columns = ['Severity', 'Count']
            st.bar_chart(phishing_severity.set_index('Severity'), color="#f97316")
        
        st.markdown("---")
        
        # Analysis 2: Response Bottleneck Analysis
        st.markdown("### ⏱️ Resolution Time & Bottleneck Analysis")
        
        # Calculate days open (simulated - would need resolved_date in real scenario)
        df_with_status = df_incidents.copy()
        df_with_status['days_open'] = 0  # Placeholder - would calculate from dates
        
        # Status analysis - identify bottlenecks
        status_analysis = df_incidents.groupby('status').agg({
            'id': 'count',
            'severity': lambda x: (x.isin(['Critical', 'High']).sum())
        }).reset_index()
        status_analysis.columns = ['Status', 'Total Count', 'High/Critical Count']
        status_analysis = status_analysis.sort_values('Total Count', ascending=False)
        
        st.markdown("**Incident Distribution by Status (Bottleneck Identification):**")
        st.dataframe(status_analysis, width='stretch', hide_index=True)
        
        # Find which threat category has longest resolution (unresolved)
        st.markdown("**Threat Categories with Most Unresolved Cases:**")
        unresolved_by_type = df_incidents[df_incidents['status'].isin(['Open', 'In Progress'])].groupby('incident_type').agg({
            'id': 'count',
            'severity': lambda x: (x.isin(['Critical', 'High']).sum())
        }).reset_index()
        unresolved_by_type.columns = ['Incident Type', 'Unresolved Count', 'High/Critical']
        unresolved_by_type = unresolved_by_type.sort_values('Unresolved Count', ascending=False)
        st.dataframe(unresolved_by_type, width='stretch', hide_index=True)
        
        if len(unresolved_by_type) > 0:
            st.bar_chart(unresolved_by_type.set_index('Incident Type')['Unresolved Count'], color="#ef4444")
    else:
        st.info("🔍 No incidents recorded yet. Add data to see analytics insights.")

# Tab 5: AI Assistant
with tab5:
    
    # Build context from current data with full details
    if incidents:
        severity_counts = {}
        status_counts = {}
        type_counts = {}
        for inc in incidents:
            sev = inc.get_severity()
            stat = inc.get_status()
            typ = inc.get_incident_type()
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            status_counts[stat] = status_counts.get(stat, 0) + 1
            type_counts[typ] = type_counts.get(typ, 0) + 1
        
        # Include ALL incidents with full details - no limits
        # Build detailed incident list for all incidents
        detailed_list = "\n".join([
            f"""
Incident ID: {inc.get_id()}
Date: {inc.get_date()}
Type: {inc.get_incident_type()}
Severity: {inc.get_severity()}
Status: {inc.get_status()}
Description: {inc.get_description()}
---"""
            for inc in incidents
        ])
        
        DATA_CONTEXT = f"""
CURRENT DASHBOARD DATA:
- Total Incidents: {len(incidents)}
- By Severity: {severity_counts}
- By Status: {status_counts}
- By Type: {type_counts}

DETAILED INCIDENT INFORMATION (with full descriptions and status):
{detailed_list}

Note: You have access to complete details including incident IDs, dates, types, severity levels, current status, and full descriptions. Use this information to answer questions about specific incidents, their current state, and provide detailed analysis.
"""
    else:
        DATA_CONTEXT = "\nCURRENT DASHBOARD DATA: No incidents recorded yet.\n"
    
    # System prompt for AI
    SYSTEM_PROMPT = f"""You are a friendly cybersecurity expert assistant with access to detailed incident information.

{DATA_CONTEXT}

Responsibilities:
- Answer questions about specific incidents using their ID, status, description, and other details
- Provide detailed analysis of incidents including their current status and descriptions
- Analyse threats and provide MITRE ATT&CK references when relevant
- Give actionable remediation recommendations based on incident details
- When asked about a specific incident, provide its full details including status and description

IMPORTANT: You have access to complete incident information including:
- Incident IDs (use these to reference specific incidents)
- Current status (Open, In Progress, Resolved, Closed)
- Full descriptions (use these to understand what happened)
- Dates, types, and severity levels

Always refer to actual incident data when answering questions. Be specific and detailed when discussing incidents."""
    
    # Initialize AIAssistant
    ai = AIAssistant(system_prompt=SYSTEM_PROMPT, history_key="cyber_chat_history")
    
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
                
                # Button to list available models
                if st.button("🔍 List Available Models", key="list_models_cyber"):
                    try:
                        available_models = AIAssistant.list_available_models(api_key)
                        if available_models:
                            st.success("✅ Available models:")
                            for model in available_models[:10]:  # Show first 10
                                st.code(model, language=None)
                        else:
                            st.warning("No models found or error listing models")
                    except Exception as e:
                        st.error(f"Error listing models: {str(e)}")
        except Exception as e:
            st.error(f"❌ **Configuration Error:** {str(e)}")
            st.info("💡 Make sure `.streamlit/secrets.toml` exists with your API key")
    else:
        # AI header with clear button
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown("### 🛡️ Security AI Assistant")
            st.caption("Ask about incidents, threats, or security best practices")
        with col_h2:
            if st.button("🗑️ Clear", key="cyber_clear"):
                ai.clear_history()
                st.rerun()
        
        st.markdown("---")
        
        # Welcome message
        if len(ai.get_history()) == 0:
            st.write("👋 Welcome! I'm your Security Assistant")
            st.write("I can analyse incidents, explain threats, and provide security recommendations.")
        
        # Display chat history
        for msg in ai.get_history():
            role = "user" if msg["role"] == "user" else "assistant"
            with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🛡️"):
                st.markdown(msg["content"])
        
        # Handle user input
        user_input = st.chat_input("💬 Ask about security...")
        
        if user_input:
            # Show user message
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(user_input)
            
            # Get AI response with streaming
            with st.chat_message("assistant", avatar="🛡️"):
                container = st.empty()
                ai.send_message_stream(user_input, container)


# Sign out button
st.markdown("---")
if st.button("🚪 Sign Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("Home.py")
