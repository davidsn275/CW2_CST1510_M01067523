# Multi-Domain Intelligence Platform

Student Name: David Sandanum
Student ID: M01067523
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform

## Project Description

A comprehensive multi-domain intelligence platform built with Streamlit that provides secure access to analytics dashboards across cybersecurity, data science, and IT operations domains. The platform features user authentication, interactive dashboards, data visualization, and AI-powered assistance.

## Features

### 🔐 Authentication System
- Secure user registration and login
- Password hashing using bcrypt
- Session management with Streamlit
- User data persistence in SQLite database

### 🔒 Cybersecurity Incidents Dashboard
- View and manage security incidents
- Interactive data visualization
- Filter and search capabilities
- Incident tracking and analysis

### 📊 Data Science Dashboard
- Dataset management and exploration
- Data visualization tools
- Statistical analysis capabilities
- AI-powered insights

### 🖥️ IT Operations Dashboard
- IT ticket management
- Operational metrics and monitoring
- Ticket tracking and resolution

### 🤖 AI Assistant
- Integrated AI-powered assistance
- Context-aware responses
- Multi-domain support

## Technical Implementation

### Technology Stack
- **Frontend Framework:** Streamlit
- **Database:** SQLite
- **Data Processing:** Pandas
- **Authentication:** bcrypt password hashing
- **AI Integration:** Google Generative AI

### Project Structure
```
CW2_CST1510_M01067523/
├── Home.py                      # Main entry point and authentication page
├── pages/                        # Streamlit multi-page application
│   ├── 1_Incidents _Dashboard.py # Cybersecurity incidents dashboard
│   ├── 2_DataScience.py         # Data science dashboard
│   └── 3_ITOperations.py        # IT operations dashboard
├── services/                     # Core service modules
│   ├── auth_manager.py          # User authentication management
│   ├── database_manager.py      # Database connection and queries
│   └── ai_assistant.py          # AI assistant integration
├── models/                       # Data models
│   ├── user.py                  # User model
│   ├── security_incident.py     # Security incident model
│   ├── it_ticket.py             # IT ticket model
│   └── dataset.py               # Dataset model
├── app/                          # Application modules
│   ├── data/                    # Data access layer
│   └── services/                # Additional services
├── DATA/                         # Data storage
│   ├── intelligence_platform.db # SQLite database
│   ├── cyber_incidents.csv      # Sample cybersecurity data
│   ├── it_tickets.csv           # Sample IT tickets data
│   └── datasets_metadata.csv    # Dataset metadata
└── docs/                         # Documentation
    └── README.md                # This file
```

### Database Schema
- **Users Table:** Stores user credentials and authentication data
- **Security Incidents Table:** Tracks cybersecurity incidents
- **IT Tickets Table:** Manages IT operational tickets
- **Datasets Table:** Stores dataset metadata and information

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd CW2_CST1510_M01067523
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r docs/Requiremens.txt
   ```

   Required packages:
   - `streamlit` - Web application framework
   - `pandas` - Data manipulation and analysis
   - `bcrypt` - Password hashing (if used)
   - `google-generativeai` - AI assistant integration

3. **Initialize the database:**
   The database will be automatically created on first run if it doesn't exist.

4. **Run the application:**
   ```bash
   streamlit run Home.py
   ```

5. **Access the application:**
   Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

## Usage

### First Time Setup
1. Launch the application using `streamlit run Home.py`
2. Navigate to the "Register" tab
3. Create a new account with a username and password
4. Switch to the "Login" tab and sign in with your credentials

### Navigating the Platform
- **Home Page:** Authentication and main entry point
- **Incidents Dashboard:** View and manage cybersecurity incidents
- **Data Science Dashboard:** Explore datasets and perform analysis
- **IT Operations Dashboard:** Manage IT tickets and operations

### Features Overview
- **Interactive Dashboards:** All dashboards feature interactive visualizations and filtering
- **Data Management:** Add, edit, and delete records through intuitive interfaces
- **AI Assistance:** Get AI-powered insights and assistance across all domains
- **Secure Access:** All features require user authentication

## Security Features

- **Password Hashing:** User passwords are hashed using SHA256 before storage
- **Session Management:** Secure session tracking using Streamlit's session state
- **Input Validation:** Username and password validation on registration
- **Database Security:** SQLite database with proper connection management

## Data Sources

The platform includes sample data files:
- `cyber_incidents.csv` - Cybersecurity incident records
- `it_tickets.csv` - IT support ticket data
- `datasets_metadata.csv` - Dataset information and metadata

## Development Notes

- The application uses a multi-page Streamlit architecture
- Database connections are managed through the `DatabaseManager` service
- Authentication is handled by the `AuthManager` service
- All data models follow a consistent structure for easy extension