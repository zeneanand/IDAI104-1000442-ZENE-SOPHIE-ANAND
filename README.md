
📈 Crypto Volatility Visualizer
An interactive financial analytics dashboard built using Streamlit, Pandas, NumPy, and Plotly to simulate and analyze cryptocurrency market volatility using mathematical models and real OHLCV data.

Student Name: zene sophie anand 
Student ID: 1000442
Course: Artificial Intelligence
Focus: Mathematics for AI-I Assessment Type: Formative Assessment 2 (FA-2)

🚀 Live Demo
🔗 https://idai104-1000414-aditya-jitendra-kumar-sahani.streamlit.app

🧠 Project Overview
Crypto Volatility Visualizer connects mathematical functions to real-world financial behavior.

The application allows users to:

Simulate cryptocurrency price movements
Analyze real 1-minute Bitcoin OHLCV data (1M+ rows)
Measure volatility and trend direction
Compare stable vs volatile market conditions
Visualize trading behavior interactively
🎨 UI/UX Planning & Storyboard
This project involved careful pre-planning of the user experience, layout structure, and component behavior to ensure a smooth and intuitive workflow. You can view the complete design storyboard, wireframes, and skill planning here:

🔗 Storyboard Access Link : https://www.canva.com/design/DAHBjXYdWME/QiOeIvriqCXobmNKAjonLg/edit?utm_content=DAHBjXYdWME&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Storyboard
<img width="616" height="483" alt="Screenshot 2026-03-04 at 11 47 41 AM" src="https://github.com/user-attachments/assets/fad2310b-3eac-44a1-af66-4f6674f04d78" />

✨ Features
🔹 Market Simulation Engine
Users can generate synthetic price data using:

Sine Wave Model (market cycles)
Cosine Wave Model
Random Noise Model (market shocks)
Adjustable parameters:

Amplitude (Volatility level)
Frequency (Trading intensity)
Drift (Market trend direction)
Comparison Mode (Side-by-side visualization)
🔹 Real Dataset Analysis
Supports three data sources:

Preloaded demo dataset
Google Drive-hosted BTC dataset (1M+ rows)
Custom CSV upload (OHLCV format)
The app performs:

Unix timestamp → datetime conversion
Column renaming and cleaning
Missing value detection
Volatility calculation (High - Low)
Statistical summary generation
🔹 Interactive Visualizations
Built with Plotly:

Close Price Trend
High vs Low Band
Volume Chart
Stable vs Volatile Detection
Side-by-Side Comparison Mode
All charts include:

Proper axis labels
Hover tooltips
Zoom and pan support
Dynamic filtering
🖼️ App Screenshots
Onboarding Screen	Login Screen	Signup Screen
<img width="1901" height="926" alt="Onboarding Screen" src="https://github.com/user-attachments/assets/ce874b1c-06f6-4c3b-a530-b3979d05721c" />
Login Screen
<img width="1906" height="927" alt="Login Screen" src="https://github.com/user-attachments/assets/08c742a7-3962-4cf7-8917-d547701ac515" />
Signup Screen
<img width="1911" height="934" alt="Signup Screen" src="https://github.com/user-attachments/assets/ecfe4584-311e-4f2f-a8e5-410b53540306" />
Demo Page
<img width="1901" height="920" alt="Demo Page" src="https://github.com/user-attachments/assets/05c78657-e373-482f-b856-d5becb3224bb" />
Forget Password
<img width="1904" height="927" alt="Forget Password" src="https://github.com/user-attachments/assets/c4712ed6-9926-4634-b9c1-3f11d057b5ee" />
Dashboard
<img width="1913" height="928" alt="Dashboard" src="https://github.com/user-attachments/assets/41cc9f8d-6e95-4e3f-bac6-6374be597229" />
Controls
<img width="221" height="623" alt="Controls" src="https://github.com/user-attachments/assets/36487d25-9720-40f7-a9fa-57601b5203b7" />
Simulation Setting
<img width="217" height="405" alt="Simulation Setting" src="https://github.com/user-attachments/assets/6b50c9c1-cf9d-45da-acbc-9e3e4a2d42d2" />
Real Dataset
<img width="1795" height="910" alt="Real Dataset Screen" src="https://github.com/user-attachments/assets/6514a9a4-ddec-475c-9b8f-6942082ec2f4" />
Math Concept 2
<img width="1031" height="622" alt="Math Concept 2" src="https://github.com/user-attachments/assets/1ddb9f2d-607a-4e5b-882d-19d8f9c019cb" />
Math Concept 3
<img width="1481" height="588" alt="Math Concept 3" src="https://github.com/user-attachments/assets/ed51f36a-4636-40da-a983-49b4bdd0ec1c" />
Edit Profile
<img width="1909" height="931" alt="Edit Profile" src="https://github.com/user-attachments/assets/1f4a5cda-c7f0-416b-9109-1ba0329a4a8b" />
Feedback
<img width="1909" height="935" alt="Feedback" src="https://github.com/user-attachments/assets/669ae159-798f-414f-964f-390aab7d40cf" />
Loading Screen	


🧮 Mathematical Models
Concept	Formula / Representation	Market Meaning
1-min Volatility	High − Low	Statistics / Real market risk measurement
Sine price cycle	y = A·sin(f·x) + drift·x	Predictable cyclical bull/bear phases
Cosine price cycle	y = A·cos(f·x) + drift·x	Cycle starting at market peak
Random Noise	y = N(0,A) + drift·x	Sudden news-driven shocks (closest to BTC)
Bull market	drift > 0	Long-term upward trend
Bear market	drift < 0	Long-term downward trend
Volatility index σ	√(Σ(x−μ)²/n)	Differentiates high-risk vs safe assets
Parameter	Meaning	Market Interpretation
Amplitude (A)	Wave height	Size of price swings
Frequency (f)	Wave speed	Trading activity
Drift	Linear slope	Bull/Bear market trend
Std Dev (σ)	Spread of values	Volatility index
📊 Dataset
File: btcusd_1-min_data.csv
Google Drive Link: Dataset Download Link

Format: OHLCV
Frequency: 1-minute intervals
Size: ~1,048,576 rows
Period: January 2012 – Present
Source: Kaggle public dataset
Column	Description
Timestamp	Unix seconds since Jan 1, 1970
Open	Opening price
High	Highest price
Low	Lowest price
Close	Closing price
Volume	Trading volume
🛠 Tech Stack
Frontend

Streamlit
Data Processing

Pandas
NumPy
Visualization

Plotly
Deployment

Streamlit Cloud
📁 Project Structure
IDAI104-1000414-ADITYA-JITENDRA-KUMAR-SAHANI/
│
├── assets/
│   └── App Screenshots/
├── app.py
├── requirements.txt
└── README.md
⚙ Installation & Local Setup
Clone Repository
git https://github.com/adityasahani392217/IDAI104-1000414-ADITYA-JITENDRA-KUMAR-SAHANI
cd  IDAI104-1000414-ADITYA-JITENDRA-KUMAR-SAHANI
Install Dependencies
pip install -r requirements.txt
Run Application
streamlit run app.py
🌐 Deployment
Push project to GitHub:
git add .
git commit -m "Initial commit"
git push origin main
Connect repository to Streamlit Cloud:
Go to share.streamlit.io
Click "New app"
Select your repository, branch, and file path
Select app.py as entry point.
Deploy and share URL!
🏗 System Architecture

📚 Learning Outcomes
This project demonstrates:

Financial time-series visualization
Mathematical modeling of markets
Data pipeline creation
Large dataset handling (1M+ rows)
Interactive dashboard design
Cloud deployment workflow
👥 Collaborators
Name	WACP NO
Aditya Jitendra Kumar Sahani	1000414
Zene Sophie Anand	1000442
Naman Om shreshta	1000432
📄 License
This application was exclusively developed for academic assessment and portfolio demonstration. It serves as an open-source technical showcase demonstrating applied mathematical modeling, algorithmic financial analysis, and large-scale data visualization in a practical software setting.
