# Week 7: Secure Authentication System

Student Name: Mike Abuko  
Student ID: M01057708 
Course: CST1510 -CW2 -  Multi-Domain Intelligence Platform 

## Project Description

A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass

## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence
- Password confirmations during login and registration
- Error messages to inform the user what is wrong

## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters) - Must contain atleast: one digit, uppercase, and lowercase letters.


## Project Progress

### Week 7: User Authentication (Completed)
- Created a user registration and login system
- Used bcrypt to hash passwords for security
- Stored the users in a text file (users.txt)
- Made sure usernames and passwords follow the rules

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
- `main.py` - demo script to test that the backend functionality works well.

## How to Run

1. Install the required packages:

- pip install -r requirements.txt


2. Run the demo:
- python main.py

This will:
- Create the database file
- Set up all the tables
- Test user registration and login
- Show how CRUD operations work

## Requirements

- Python
- bcrypt - for security
- pandas - for working with data

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

**Files created:**
- `Home.py` - Main login page
- `pages/1_Dashboard.py` through `pages/5_Analytics.py` - All app pages

## 📚 DOCUMENTATION

This project includes comprehensive documentation to help you understand everything:

### 🎯 Quick Links
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Start here to find what you need!
- **[QUICK_START.md](QUICK_START.md)** - Get running in 5 minutes
- **[COMPLETE_WALKTHROUGH.md](COMPLETE_WALKTHROUGH.md)** - Full tutorial (40 min)
- **[TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)** - Test everything systematically
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Overview and stats

### 📖 Which Document Should I Read?

**Just want to run it?** → [QUICK_START.md](QUICK_START.md)  
**Need to understand everything?** → [COMPLETE_WALKTHROUGH.md](COMPLETE_WALKTHROUGH.md)  
**Ready to test?** → [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)  
**Writing your report?** → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)  
**Not sure where to start?** → [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)