# water-issues-reporter
1. Project Overview
The Water Issues Reporter System is a web-based application that allows citizens to report water-related issues (leakages and quality problems) to the responsible water authorities. The system consists of:

Public Reporting App (Streamlit-based Python application)

Management Dashboard (HTML/CSS/JS web interface for authorities)

2. System Requirements
2.1 Software Requirements
Python 3.8+ (Download: https://www.python.org/downloads/)

VS Code (Recommended IDE: https://code.visualstudio.com/)

Git (For version control: https://git-scm.com/)

Web Browser (Chrome/Firefox recommended)

2.2 Python Libraries
The project requires the following Python packages (listed in requirements.txt):

Copy
streamlit==1.25.0
Pillow==10.0.0
python-dotenv==1.0.0
geopy==2.3.0
uuid==1.30
Install them using:

bash
Copy
pip install -r requirements.txt
3. Setup Instructions
3.1 Setting Up the Reporting App (Streamlit)
Clone the repository (if applicable):

bash
Copy
git clone https://github.com/stark-priver/water-issues-reporter.git
cd water-issues-reporter
Install dependencies:

bash
Copy
pip install -r requirements.txt
Run the Streamlit app:

bash
Copy
streamlit run leakageApp.py
The app will open at http://localhost:8501.

3.2 Setting Up the Dashboard (HTML/CSS/JS)
Open the dashboard folder in VS Code:

bash
Copy
code dashboard/
Install Live Server Extension (for testing):

Open VS Code Extensions (Ctrl+Shift+X).

Search for "Live Server" by Ritwick Dey and install it.

Run the Dashboard:

Right-click index.html and select "Open with Live Server".

The dashboard will open at http://localhost:5500.

4. Key Features
4.1 Public Reporting App (Streamlit)
Bilingual Support (English/Swahili)

Water Leakage & Quality Reporting

Photo Upload & GPS Location Detection

Severity & Status Tracking

4.2 Management Dashboard (HTML/CSS/JS)
Real-time Report Monitoring

Filter Reports by Type & Status

Interactive Map for Location Tracking

Admin Controls (Status Updates, Assign Teams)

5. Deployment Options
5.1 Local Testing
Streamlit App: Runs on http://localhost:8501

Dashboard: Runs on http://localhost:5500 (via Live Server)

5.2 Cloud Deployment (Recommended)
Streamlit Cloud (Free tier available: https://streamlit.io/cloud)

Netlify/Vercel (For the dashboard: https://www.netlify.com/)

Firebase Hosting (Alternative: https://firebase.google.com/)

6. Troubleshooting
Issue	Solution
ModuleNotFoundError	Run pip install -r requirements.txt
Streamlit app not loading	Check if port 8501 is free
Dashboard not loading in Live Server	Ensure index.html is in the correct folder
GPS not working	Allow browser location permissions
7. Future Improvements
Mobile App Integration (Flutter/React Native)

SMS/Email Alerts for critical reports

Automated Water Quality Analysis (AI-based)

8. Support & Contact
For technical support, contact:
📧 Email: support@waterauthority.mbeya
📞 Phone: +255 XXX XXX XXX

🔹 Happy Reporting!
This system helps improve water management in Mbeya.
Thank you for your contribution! 💧

📄 Appendix
requirements.txt (Python dependencies)

leakageApp.py (Streamlit reporting app)

dashboard/ (HTML/CSS/JS management dashboard)

📌 Notes
Always test changes locally before deploying.

Keep credentials secure (use .env for sensitive data).

Document Version: 1.0
Last Updated: 2023-10-20