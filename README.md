<img width="1355" height="596" alt="image" src="https://github.com/user-attachments/assets/be83a299-7e1e-419c-bdfc-e5ea085a172b" />
🔧 WCP Tracker (Western Cape Performance Tracker)

A Flask-based web application designed to track the quarterly performance of government departments against their Annual Performance Plan (APP) indicators. The system provides a centralized portal for data submission, automates compliance checks, and exports clean data ready for business intelligence tools like Power BI.

![alt text](https://img.shields.io/badge/python-3.8+-blue.svg)


![alt text](https://img.shields.io/badge/flask-2.x-brightgreen.svg)


![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)

🎯 Core Features

Admin Dashboard: Centrally manage departments and their associated performance indicators.

Department Submission Portal: An intuitive form for departments to submit their quarterly performance data.

Automated Compliance Flagging: The system automatically generates flags for common issues like:

Underperformance (actual value below target)

Late Submissions

Reporting & Audit Trail: View a comprehensive list of all historical submissions, including who submitted them, when, and what flags were raised.

Power BI Data Export: Generate a clean, structured CSV file with a single click, perfectly formatted for use as a data source in Power BI.

🛠️ System Architecture & Tech Stack

The application is built with a simple and robust set of tools, making it easy to maintain and deploy.

Component	Tool	Purpose
Backend App	Flask (Python)	Data collection, indicator setup, submission portal, compliance logic.
Database	SQLite / SQLAlchemy	Stores departments, indicators, quarterly submissions, and flags.
Frontend	HTML + Bootstrap	Clean input forms and summary pages for a professional UI.
Data Export	Pandas + CSV	Exports submission data for use in Power BI or other tools.
Dashboarding	Power BI (via CSV)	Data visualizations for submissions, compliance, and performance KPIs.
📸 Screenshots

(Note: Replace these with actual screenshots of your running application.)

1. Admin Dashboard

(https://user-images.githubusercontent.com/<img width="1355" height="596" alt="image" src="https://github.com/user-attachments/assets/b9edb894-63e6-4179-8d37-1ddcbf48ca97" />
)

Shows the list of all departments and indicators, with options to add new ones.
<img width="1346" height="599" alt="image" src="https://github.com/user-attachments/assets/3d7b8c5d-5fcc-4e95-b1c1-13fb295bf07b" />


2. Submission Form

<img width="1358" height="595" alt="image" src="https://github.com/user-attachments/assets/ba7642db-baca-42b3-9475-51b4ac830a54" />


The simple form for submitting quarterly performance data for a specific indicator.
<img width="1358" height="599" alt="image" src="https://github.com/user-attachments/assets/707af8d5-adb7-4816-8f16-5125c204964a" />


3. Submissions List & Audit Trail

A comprehensive table of all submissions, highlighted with compliance flags.
<img width="1365" height="598" alt="image" src="https://github.com/user-attachments/assets/22369807-fbb5-47b5-b157-19ad71425820" />


🚀 Getting Started

Follow these instructions to get a local copy of the project up and running for development and testing purposes.

Prerequisites

Git

Python (3.8 or higher recommended)

Installation & Setup

Clone the repository:

Generated sh
git clone https://github.com/your-username/wcp-tracker.git
cd wcp-tracker


Create and activate a virtual environment:

On Windows:

Generated sh
python -m venv venv
.\venv\Scripts\activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

On macOS/Linux:

Generated sh
python3 -m venv venv
source venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

Install the required packages:

Generated sh
pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

Initialize and seed the database:
This command will create the wcp_tracker.db file and populate it with mock departments and indicators for testing.

Generated sh
flask seed-db
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

Run the Flask application:

Generated sh
flask run
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

The application will be available at http://127.0.0.1:5000.

📋 Usage

Once the application is running, you can perform the following actions:

Admin Tasks: Navigate to http://127.0.0.1:5000/admin to add or view departments and indicators.

Submit Data: From the admin dashboard, click the "Submit Data" button next to any indicator to go to the submission form. Fill it out and submit.

View Submissions: Go to http://127.0.0.1:5000/submissions to see the audit trail of all data entered.

Export for Power BI: Click the "Export for Power BI" link in the navigation bar. This will generate and download wcp_submissions_export.csv.

Power BI Integration

Run the application and make a few submissions.

Export the data using the link in the navigation bar.

Open Power BI Desktop.

Click Get Data > Text/CSV and select the downloaded wcp_submissions_export.csv file.

You can now build your dashboards using the provided data.

🗂️ Project Folder Structure
Generated code
wcp_tracker/
│
├── app.py              # Main Flask application file (routes, logic)
├── models.py           # SQLAlchemy database models
├── forms.py            # WTForms classes for input validation
├── data/
│   └── seed_data.py    # Logic to populate the database with mock data
├── static/             # CSS, JavaScript, and other static assets
├── templates/          # HTML templates for rendering pages
├── exports/            # Default directory for CSV exports (created automatically)
├── requirements.txt    # List of Python package dependencies
└── README.md           # This file
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
📈 Future Enhancements

CRUD Operations: Implement Update and Delete functionality for departments and indicators.

User Authentication: Add a login system to distinguish between Admins and Department-level users.

Advanced Logic: Add a field to indicators to specify if a lower value is better (e.g., response time).

Flag Resolution: Add a mechanism for admins to mark compliance flags as "Resolved".

📜 License

This project is licensed under the MIT License.
