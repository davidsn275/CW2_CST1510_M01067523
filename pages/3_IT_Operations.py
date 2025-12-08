import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database_manager import DatabaseManager
from services.ai_assistant import AIAssistant
from models.it_ticket import ITTicket

# Page setup
st.set_page_config(
    page_title="IT Operations Dashboard",
    page_icon="💻",
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
        background: linear-gradient(135deg, #10b981, #06b6d4);
        border-color: #10b981;
        color: white !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
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
st.title("💻 IT Operations Center")
st.caption("Streamlined ticket management and support tracking")


# Load tickets using DatabaseManager and convert to ITTicket objects
rows = db.get_all_tickets()
tickets = []
for row in rows:
    ticket = ITTicket(
        ticket_id=row[0],
        date=row[1],
        category=row[2],
        priority=row[3],
        status=row[4],
        description=row[5],
        assigned_to=row[6] or ""
    )
    tickets.append(ticket)

# Convert to DataFrame for display
df_tickets = pd.DataFrame([tkt.to_dict() for tkt in tickets]) if tickets else pd.DataFrame()

# Calculate metrics using objects
critical_count = sum(1 for tkt in tickets if tkt.get_priority().lower() == "critical")
open_count = sum(1 for tkt in tickets if tkt.get_status().lower() == "open")
resolved_count = sum(1 for tkt in tickets if tkt.get_status().lower() == "resolved")


# Display metrics in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🚨 Critical Priority", critical_count)

with col2:
    st.metric("📂 Open Tickets", open_count)

with col3:
    st.metric("✅ Resolved", resolved_count)

with col4:
    st.metric("📊 Total Tickets", len(tickets))

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 View Data", "➕ Create Ticket", "📤 Upload CSV", "📊 Analytics & Insights", "🤖 AI Assistant"])


# Tab 1: View Data
with tab1:
    if len(df_tickets) > 0:
        # Time-series chart: Tickets over time
        st.subheader("📈 Tickets Created Over Time")
        
        # Prepare time-series data
        df_tickets_copy = df_tickets.copy()
        if "date" in df_tickets_copy.columns:
            df_tickets_copy['date'] = pd.to_datetime(df_tickets_copy['date'], errors='coerce')
            df_tickets_copy = df_tickets_copy.dropna(subset=['date'])
            
            if len(df_tickets_copy) > 0:
                # Group by date and count tickets
                df_tickets_copy['date_only'] = df_tickets_copy['date'].dt.date
                time_series = df_tickets_copy.groupby('date_only').size().reset_index(name='count')
                time_series.columns = ['Date', 'Tickets']
                time_series = time_series.sort_values('Date')
                time_series = time_series.set_index('Date')
                
                # Display line chart
                st.line_chart(time_series, color="#10b981", height=300)
            else:
                st.info("⚠️ Date information unavailable for time-series analysis")
        else:
            st.info("⚠️ Date information unavailable for time-series analysis")
        
        st.markdown("---")
        
        # Bar chart: Tickets by Status
        st.subheader("📊 Tickets by Status")
        status_counts = df_tickets["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        st.bar_chart(status_counts.set_index("status"), color="#10b981")
        
        st.markdown("---")
        
        # Show data table
        st.subheader("📋 All Tickets")
        st.dataframe(df_tickets, width='stretch', height=350)
    else:
        st.info("🔍 No tickets found. Create your first ticket!")

# Tab 2: Create Ticket
with tab2:
    st.subheader("🆕 Create Support Ticket")
    
    with st.form("ticket_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("📅 Date")
            category = st.selectbox("📂 Category", ["Network", "Hardware", "Software", "Database", "Email", "Security"])
            priority = st.selectbox("⚡ Priority", ["Low", "Medium", "High", "Critical"])
        with col2:
            status = st.selectbox("📌 Status", ["Open", "In Progress", "On Hold", "Resolved", "Closed"])
            assigned_to = st.text_input("👤 Assigned To")
            description = st.text_area("📝 Description", height=80)
        
        submitted = st.form_submit_button("🎫 Create Ticket")
    
    if submitted:
        if not description:
            st.error("❌ Please provide a description")
        else:
            # Use DatabaseManager to insert ticket
            db.insert_ticket(str(date), category, priority, status, description, assigned_to)
            st.success("✅ Ticket created successfully!")
            st.rerun()

# Tab 3: Upload CSV
with tab3:
    st.subheader("📁 Import CSV Data")
    st.info("📋 Required columns: date, category, priority, status, description, assigned_to")
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv", key="ticket_upload")
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        st.dataframe(new_df.head(), width='stretch')
        
        if st.button("📥 Import Data"):
            for _, row in new_df.iterrows():
                db.insert_ticket(
                    str(row.get('date', '')),
                    str(row.get('category', '')),
                    str(row.get('priority', '')),
                    str(row.get('status', '')),
                    str(row.get('description', '')),
                    str(row.get('assigned_to', ''))
                )
            st.success(f"✅ Added {len(new_df)} tickets")
            st.rerun()

# Tab 4: Analytics & Insights
with tab4:
    st.subheader("🎯 High-Value IT Operations Analysis")
    st.info("Problem Statement: The IT support team is struggling with slow resolution times. Pinpoint staff performance anomalies and identify process stage bottlenecks causing delays.")
    
    if len(df_tickets) > 0:
        # Analysis 1: Staff Performance Analysis
        st.markdown("### 👥 Staff Performance & Workload Analysis")
        
        if "assigned_to" in df_tickets.columns:
            staff_analysis = df_tickets.groupby('assigned_to').agg({
                'id': 'count',
                'status': lambda x: (x.isin(['Open', 'In Progress']).sum())
            }).reset_index()
            staff_analysis.columns = ['Staff Member', 'Total Tickets', 'Open/In Progress']
            staff_analysis = staff_analysis.sort_values('Total Tickets', ascending=False)
            
            # Calculate open ticket ratio
            staff_analysis['Open Ratio %'] = (staff_analysis['Open/In Progress'] / staff_analysis['Total Tickets'] * 100).round(1)
            staff_analysis = staff_analysis.sort_values('Open Ratio %', ascending=False)
            
            st.markdown("**Ticket Distribution by Staff Member:**")
            st.dataframe(staff_analysis, width='stretch', hide_index=True)
            
            # Visualize staff workload
            if len(staff_analysis) > 0:
                st.markdown("**Staff Workload (Total Tickets):**")
                st.bar_chart(staff_analysis.set_index('Staff Member')['Total Tickets'], color="#10b981", height=250)
                
                st.markdown("**Open Ticket Ratio by Staff (Higher = More Backlog):**")
                st.bar_chart(staff_analysis.set_index('Staff Member')['Open Ratio %'], color="#f59e0b", height=250)
        
        st.markdown("---")
        
        # Analysis 2: Process Stage Bottleneck Analysis
        st.markdown("### ⏳ Process Bottleneck & Resolution Analysis")
        
        # Status analysis - identify bottlenecks
        status_bottleneck = df_tickets.groupby('status').agg({
            'id': 'count',
            'priority': lambda x: (x.isin(['Critical', 'High']).sum())
        }).reset_index()
        status_bottleneck.columns = ['Status', 'Ticket Count', 'Critical/High Priority']
        status_bottleneck = status_bottleneck.sort_values('Ticket Count', ascending=False)
        
        st.markdown("**Ticket Distribution by Status (Bottleneck Identification):**")
        st.dataframe(status_bottleneck, width='stretch', hide_index=True)
        
        # Visualize status distribution
        if len(status_bottleneck) > 0:
            st.bar_chart(status_bottleneck.set_index('Status')['Ticket Count'], color="#06b6d4", height=300)
        
        # Identify problematic statuses
        problematic_statuses = status_bottleneck[
            (status_bottleneck['Status'].isin(['Open', 'In Progress', 'On Hold'])) & 
            (status_bottleneck['Ticket Count'] > 3)
        ]
        
        st.markdown("---")
        
        # Analysis 3: Priority vs Resolution Analysis
        st.markdown("### 🎯 Priority Analysis")
        
        priority_analysis = df_tickets.groupby('priority').agg({
            'id': 'count',
            'status': lambda x: (x.isin(['Open', 'In Progress']).sum())
        }).reset_index()
        priority_analysis.columns = ['Priority', 'Total Tickets', 'Unresolved']
        priority_analysis['Resolution Rate %'] = ((priority_analysis['Total Tickets'] - priority_analysis['Unresolved']) / priority_analysis['Total Tickets'] * 100).round(1)
        priority_analysis = priority_analysis.sort_values('Total Tickets', ascending=False)
        
        st.dataframe(priority_analysis, width='stretch', hide_index=True)
    else:
        st.info("🔍 No tickets found. Create tickets to see analytics insights.")

# Tab 5: AI Assistant
with tab5:
    # Build context from current data with full details
    if tickets:
        priority_counts = {}
        status_counts = {}
        category_counts = {}
        for tkt in tickets:
            pri = tkt.get_priority()
            stat = tkt.get_status()
            cat = tkt.get_category()
            priority_counts[pri] = priority_counts.get(pri, 0) + 1
            status_counts[stat] = status_counts.get(stat, 0) + 1
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Include ALL tickets with full details
        # Create detailed ticket information with full descriptions and status
        detailed_tickets = "\n".join([
            f"""
Ticket ID: {tkt.get_id()}
Date: {tkt.get_date()}
Category: {tkt.get_category()}
Priority: {tkt.get_priority()}
Status: {tkt.get_status()}
Assigned To: {tkt.get_assigned_to() if tkt.get_assigned_to() else 'Unassigned'}
Description: {tkt.get_description()}
---"""
            for tkt in tickets
        ])
        
        DATA_CONTEXT = f"""
CURRENT DASHBOARD DATA:
- Total Tickets: {len(tickets)}
- Open Tickets: {open_count}
- By Priority: {priority_counts}
- By Status: {status_counts}
- By Category: {category_counts}

DETAILED TICKET INFORMATION (with full descriptions and status):
{detailed_tickets}

Note: You have access to complete ticket details including ticket IDs, dates, categories, priorities, current status, assignments, and full descriptions. Use this information to answer questions about specific tickets, their current state, and provide detailed troubleshooting assistance.
"""
    else:
        DATA_CONTEXT = "\nCURRENT DASHBOARD DATA: No tickets found yet.\n"
    
    # System prompt for AI
    SYSTEM_PROMPT = f"""You are a friendly IT support expert assistant with access to detailed ticket information.

{DATA_CONTEXT}

Responsibilities:
- Answer questions about specific tickets using their ID, status, description, priority, and other details
- Provide detailed analysis of tickets including their current status, descriptions, and assignments
- Help troubleshoot technical issues based on ticket descriptions
- Provide step-by-step solutions tailored to the specific ticket details
- When asked about a specific ticket, provide its full details including status, description, and assignment

IMPORTANT: You have access to complete ticket information including:
- Ticket IDs (use these to reference specific tickets)
- Current status (Open, In Progress, Resolved, Closed)
- Full descriptions (use these to understand the technical issue)
- Priorities, categories, dates, and assignments

Always refer to actual ticket data when answering questions. Be specific and detailed when discussing tickets and provide actionable troubleshooting steps."""
    
    # Initialize AIAssistant
    ai = AIAssistant(system_prompt=SYSTEM_PROMPT, history_key="it_chat_history")
    
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
            st.markdown("### 💻 IT Support AI Assistant")
            st.caption("Ask about tickets, troubleshooting, or IT best practices")
        with col_h2:
            if st.button("🗑️ Clear", key="it_clear"):
                ai.clear_history()
                st.rerun()
        
        st.markdown("---")
        
        # welcome message
        if len(ai.get_history()) == 0:
            st.write("👋 Welcome! I'm your IT Support Assistant")
            st.write("I can help troubleshoot issues, prioritize tickets, and provide solutions.")
        
        # Display chat history
        for msg in ai.get_history():
            role = "user" if msg["role"] == "user" else "assistant"
            with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "💻"):
                st.markdown(msg["content"])
        
        # Handle user input
        user_input = st.chat_input("💬 Ask about IT support...")
        
        if user_input:
            # Show user message
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(user_input)
            
            # Get AI response with streaming
            with st.chat_message("assistant", avatar="💻"):
                container = st.empty()
                ai.send_message_stream(user_input, container)


# Sign out button
st.markdown("---")
if st.button("🚪 Sign Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("Home.py")

