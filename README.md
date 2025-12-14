# Week 7-11: Multi-Domain Intelligence Platform

Student Name: Mike Abuko  
Student ID: M01057708 
Course: CST1510 -CW2 -  Multi-Domain Intelligence Platform 

## Project Description

A web-based cybersecurity platform where users can manage security incidents, datasets, and IT tickets. Started with simple login system, added a database, built web pages, added AI features, and now uses proper Object-Oriented Programming!

## Features
- Secure password hashing using bcrypt
- User registration and login
- SQLite database to store everything
- Web interface with Streamlit
- AI assistant that can analyze incidents and answer questions
- AI now gets current information from the web!
- Professional code structure using classes and objects

## Technical Implementation
- Password Security: bcrypt hashing (no plain text storage)
- Database: SQLite with 4 tables (users, incidents, datasets, tickets)
- Web Framework: Streamlit for the interface
- AI: HuggingFace AI (backup) + Groq (fast) + SerpAPI (current info)
- Code Structure: Object-Oriented Programming with classes

## Project Structure

```
cstProject/
├── Home.py                          # Main login/register page (Week 9, improved Week 11)
├── requirements.txt                 # All packages needed
├── README.md                        # This file!
│
├── .streamlit/
│   └── secrets.toml                 # API keys (not uploaded to GitHub)
│
├── app/
│   ├── data/                        # Week 8 - Database functions
│   │   ├── db.py                    # Connect to database
│   │   ├── schema.py                # Create tables
│   │   ├── users.py                 # User database operations
│   │   ├── incidents.py             # Incident operations
│   │   ├── datasets.py              # Dataset operations
│   │   └── tickets.py               # Ticket operations
│   │
│   └── services/                    # Week 8, 10, 11 - Business logic
│       ├── user_service.py          # Login/register functions (Week 8, improved Week 11)
│       ├── ai_service.py            # AI integration (Week 10, enhanced Week 11)
│       └── database_manager.py      # OOP database service (Week 11)
│
├── models/                          # Week 11 - OOP entity classes
│   ├── user.py                      # User class
│   ├── security_incident.py         # SecurityIncident class
│   ├── dataset.py                   # Dataset class
│   └── it_ticket.py                 # ITTicket class
│
├── pages/                           # Week 9 - Streamlit pages
│   ├── Dashboard.py                 # Main dashboard
│   ├── Incidents.py                 # Manage incidents (Week 9, OOP Week 11)
│   ├── Datasets.py                  # Manage datasets
│   ├── Tickets.py                   # Manage tickets
│   ├── Data_Analytics.py            # Charts and graphs
│   └── AI_Assistant.py              # Week 10 - Chat with AI
│
└── DATA/                            # Week 8, 11 - Data storage
    └── intelligence_platform.db     # SQLite database (57 incidents, 28 datasets, 42 tickets)
```

## Project Progress

### Week 7: User Authentication (Completed)
**What I did:**
- Created a user registration and login system
- Used bcrypt to hash passwords for security
- Stored the users in a text file (users.txt)
- Made sure usernames and passwords follow the rules

**Password Rules:**
- At least 8 characters long *(Improved in Week 11)*
- Must have at least one number
- Must have at least one uppercase letter
- Must have at least one lowercase letter
- Must have at least one special character (any symbol: !@#$%^&*£€¥ etc.) *(Improved in Week 11)*

**Username Rules:**
- Between 3-20 characters
- Only letters and numbers (no special characters)

### Week 8: Database Integration (Completed)
**What I did:**
- Set up SQLite database to store all the data
- Created 4 tables:
  - `users` - stores user accounts
  - `cyber_incidents` - stores security incidents
  - `datasets_metadata` - stores dataset information
  - `it_tickets` - stores IT support tickets

- Moved my login/register functions to work with the database instead of users.txt file making it more dynamic
- Learned CRUD (Create, Read, Update, Delete)
- Made sure to use `?` placeholders to prevent SQL injection attacks
- Tested to make sure it works

**Files created:**
- `app/data/db.py` - connects to the database
- `app/data/schema.py` - creates the tables
- `app/data/users.py` - handles user operations
- `app/data/incidents.py` - handles incidents
- `app/data/datasets.py` - handles datasets
- `app/data/tickets.py` - handles tickets
- `app/services/user_service.py` - handles user login/registration with database
  

### Week 9: Web Interface (Completed)
**What I did:**
- Built a complete web application using Streamlit
- Created 5 pages:
  - `Home.py` - Login and registration
  - `1_Dashboard.py` - Main page with quick stats
  - `2_Incidents.py` - View, add, edit, delete cyber incidents
  - `3_Datasets.py` - View, add, edit, delete datasets
  - `4_Tickets.py` - View, add, edit, delete IT tickets
  - `5_Analytics.py` - Charts and visualizations

- Added session state to keep users logged in
- Protected all pages so only logged-in users can access them
- Made CRUD forms for all data types
- Added data visualization with charts
- Made it look professional with custom styling

**User Experience Improvements:** *(Improved in Week 11)*
- Smart registration flow: After signing up, you're automatically taken to the login page
- Success messages show you what's happening
- Forms clear themselves after submission for security
- No username data stays in memory when switching between login/register tabs
- Password requirements shown in a helpful dropdown

**Files created:**
- `Home.py` - Main login page *(Improved in Week 11)*
- `pages/Dashboard.py` through `pages/Analytics.py` - All app pages

### Week 10: AI Integration (Completed)
**What I learned:**
- How to use external AI APIs in my application
- Working with Hugging Face Inference API
- Storing API keys securely using Streamlit secrets
- Creating AI-powered features for cybersecurity analysis
- Writing prompts to get good responses from AI

**What I built:**
- **AI Service Module** (`app/services/ai_service.py`) *(Improved in Week 11/12)*
  - `analyze_security_incident()` - AI analyzes incidents
  - `generate_security_tips()` - AI creates security tips
  - `chat_with_ai()` - Chat with AI about security

- **AI Assistant Page** (`pages/AI_Assistant.py`)
  - Ask AI any cybersecurity question
  - Quick question buttons for common topics
  - Generate security best practices
  - Get instant AI-powered answers

- **Enhanced Incidents Page** *(Improved in Week 11 with OOP)*
  - AI-powered incident analysis button
  - Threat level assessment from AI
  - Automatic recommendations

**Technologies used:**
- **Hugging Face Inference API** - Access to AI models
- **Llama-3.2-3B-Instruct** - The AI model we use *(Changed in Week 11)*
- **Streamlit Secrets** - Secure way to store API keys
- **huggingface_hub** Python library

**Features:**
✅ AI analyzes security incidents  
✅ Chat with AI about cybersecurity  
✅ Generate security tips automatically  
✅ Get threat assessments  
✅ Quick questions with preset answers  
✅ Secure API key storage  

**New files:**
- `.streamlit/secrets.toml` - Stores API key (not uploaded to git) *(Updated in Week 11)*
- `app/services/ai_service.py` - AI integration functions *(Completely rewritten in Week 11)*
- `pages/AI_Assistant.py` - AI chat page
  

**Modified files:**
- `pages/Incidents.py` - Added AI analysis *(Converted to OOP in Week 11)*
- `pages/Dashboard.py` - Added AI features section
- `requirements.txt` - Added huggingface_hub *(Added groq and google-search-results in Week 11)*

**How to use:**
1. Go to the **Incidents** page
2. Add or select an incident
3. Click "Analyze with AI" to get assessment
4. Visit **AI Assistant** page to chat
5. Ask questions or generate tips

### Week 11: OOP Refactoring & Enhanced AI (Completed)

**What I learned:**
- How to write Object-Oriented code with classes
- Private attributes (using `__` double underscore)
- How to organize code into Models and Services
- Working with multiple AI providers
- Getting real-time data from the internet
- Writing professional prompts to make AI smarter

**What I built:**

#### 1. Object-Oriented Programming (Classes)

Created 4 entity classes in the `models/` folder:
- `User` - represents a user with private attributes like __username and __password_hash
- `SecurityIncident` - represents a cyber incident with methods like get_severity_level()
- `Dataset` - represents a dataset with methods to calculate size
- `ITTicket` - represents an IT ticket with methods to change status

Also created service classes:
- `DatabaseManager` - handles all database stuff, returns objects instead of dictionaries
- `AIAssistant` - the upgraded AI that can use multiple providers
- `AuthManager` - handles user authentication with validation rules

Three domain pages now use these OOP classes:
- `Home.py` uses User objects and AuthManager
- `pages/Incidents.py` uses SecurityIncident objects
- `pages/Datasets.py` uses Dataset objects
- `pages/IT_Operations.py` uses ITTicket objects

Why? Because it makes code cleaner and more organized! Plus I learned encapsulation (hiding data with private attributes).

#### 2. Enhanced AI System (Improved from Week 10)

Made the AI **way better** than Week 10's version:
- **3 AI Providers** (Week 10 only had HuggingFace): 
  - Groq (super fast, tries this first)
  - HuggingFace (reliable backup, always works)
  - SerpAPI (searches Google for current news)

- **Automatic Backup**: If Groq doesn't work, it tries HuggingFace
- **Real-Time Info**: Can search the web for latest cybersecurity threats (Week 10 couldn't do this!)
- **Better Answers**: AI now responds like a real security expert with proper structure
- **Professional Prompts**: Rewrote all prompts to get senior-level responses

The AI now mentions actual dates (like December 2025) and includes real URLs from news sites at the end for credibility. Week 10 AI could only use old training data!

#### 3. Security Improvements (Enhanced from Week 7 & Week 9)

**Password Validation (Enhanced from Week 7):**
- Added new length and special character requirement
- Better error messages showing exactly what's needed
- Smart detection: accepts any special character including £€¥ and any other symbols
- Uses `not char.isalnum()` check

**User Registration Flow (Enhanced from Week 9):**
- Smart registration flow: After signing up, you're automatically taken to the login page
- Forms clear themselves after submission for security
- No username data stays in memory when switching between login/register tabs
- Password requirements shown in a helpful dropdown

#### 4. More Realistic Data

Added lots of test data to make it look professional:
- 57 security incidents (phishing, ransomware, DDoS, malware, etc.)
- 28 datasets (different categories, sizes from 5MB to 1GB)
- 42 IT tickets (different priorities and statuses)

Week 8's database only had a few sample records and now it looks like a real system

**New files created in Week 11:**
- `models/user.py` - User class
- `models/security_incident.py` - SecurityIncident class
- `models/dataset.py` - Dataset class
- `models/it_ticket.py` - ITTicket class
- `app/services/database_manager.py` - DatabaseManager class
- `OOP_IMPLEMENTATION.md` - Documentation
- `AI_ENHANCEMENTS.md` - AI improvements documentation

**Files updated in Week 11:**
- `app/services/ai_service.py` - Rewritten with Groq + SerpAPI
- `app/services/user_service.py` - Added special character validation
- `pages/Incidents.py` - Converted to use OOP classes
- `Home.py` - Improved registration flow and security
- `requirements.txt` - Added `groq` and `google-search-results`
- `.streamlit/secrets.toml` - Added GROQ_API_KEY and SERPAPI_KEY

**How the enhanced AI works:**

When you ask the AI a question now:
1. Searches Google for current articles (if SerpAPI is set up) - **NEW in Week 11**
2. Tries Groq first because it's fast - **NEW in Week 11**
3. Falls back to HuggingFace if Groq doesn't work - **NEW in Week 11**
4. Gives you a professional answer with real sources at the bottom - **NEW in Week 11**

Example answer format:
```
Organizations face evolving threats in December 2025...

[Professional analysis with current threat landscape]

References:
[1] Cloudflare Q3 2025 DDoS Report - https://actual-url.com
[2] CISO Series Latest Threats - https://another-url.com
```

**Why these Week 11 improvements are cool:**
- AI knows about 2025 threats (Week 10 could only reference 2023-2024)
- Gives actual website links you can click (Week 10 had no links)
- Much faster with Groq (10x faster than Week 10's HuggingFace-only approach)
- Still works even if you don't have Groq or SerpAPI (backup)
- Code is organized with classes
- Password security improved with special character requirement
- User experience improved with redirecting after registration

## How to Run

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Set up your API keys in `.streamlit/secrets.toml`:
```toml
# Week 10 - Required
HF_TOKEN = "your_huggingface_token"

# Week 11 - Optional but recommended
GROQ_API_KEY = "your_groq_key"      # Makes AI 10x faster
SERPAPI_KEY = "your_serpapi_key"    # Gets current news from Google
```

3. Run the web app:
```bash
streamlit run Home.py
```

4. Open your browser and go to the URL shown (usually http://localhost:8501)

5. Login with test logins:

**Test User Accounts:**
- **Username:** `jsmith` | **Password:** `Secure2024!`
- **Username:** `mbrown` | **Password:** `Password123!`

Or create your own account using the Register tab

## Requirements

- Python 3.13
- bcrypt - for secure passwords (Week 7)
- pandas - for working with data (Week 8)
- streamlit - for the web interface (Week 9)
- plotly - for charts and graphs (Week 9)
- huggingface_hub - to use AI (Week 10)
- groq - for faster AI (Week 11 - optional)
- google-search-results - to get current news (Week 11 - optional)

## Setting up API keys:

1. **HuggingFace** (Required - Week 10)
   - Make account at https://huggingface.co
   - Go to Settings → Access Tokens
   - Create new token with "Read" access
   - This is the basic AI that always works

2. **Groq** (Optional - Week 11 enhancement)
   - Sign up at https://console.groq.com/keys
   - Get free API key with generous daily limits of about 14,400 requests
   - AI will try this first because it's super fast
   - Makes responses 10x faster than HuggingFace alone

3. **SerpAPI** (Optional - Week 11 enhancement)
   - Sign up at https://serpapi.com/manage-api-key
   - Get free API key with monthly limit of around 100 searches
   - Lets AI search Google for latest threats and news
   - Brings in December 2025 information instead of just training data

4. Put them all in `.streamlit/secrets.toml`:
   ```toml
   HF_TOKEN = "your_hf_token"
   GROQ_API_KEY = "your_groq_key"    # Week 11 - Optional
   SERPAPI_KEY = "your_serpapi_key"  # Week 11 - Optional
   ```

5. Don't upload secrets.toml to GitHub! (it's already in .gitignore)

**Note:** The AI still works with just HuggingFace (Week 10 setup), but adding Groq and SerpAPI (Week 11) makes it much better!

---

## Final Improvements Analytics

Made the analytics page with real problem-solving insights:

**Incidents Tab:**
- Time chart showing when Phishing attacks spiked (not just counts!)
- Calculates how many days each threat type takes to fix
- Shows which high-severity incidents are still open (the backlog problem)

**Tickets Tab:**
- See which staff member has the most open tickets
- Calculates average resolution time by person
- Shows performance anomalies automatically

**Datasets Tab:**
- Recommends which big datasets should be archived (>100MB)
- Shows which department uses the most storage
- Checks for quality issues (weird file sizes)

Now the charts don't just show data - they tell you what's wrong and what to fix! All the important findings show up in colored warning/information boxes.

---
