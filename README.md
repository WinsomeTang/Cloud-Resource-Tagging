# CloudMart Resource Tagging Dashboard

A comprehensive Streamlit dashboard for analyzing cloud resource tagging compliance and cost visibility.

## 📋 Features

- **Task Set 1**: Data Exploration - Load and explore dataset, identify missing values
- **Task Set 2**: Cost Visibility - Analyze costs by tagging status, department, project, and environment
- **Task Set 3**: Tagging Compliance - Create completeness scores, identify gaps, export untagged resources
- **Task Set 4**: Visualization Dashboard - Interactive charts and filters for cost analysis
- **Task Set 5**: Tag Remediation Workflow - Edit tags, compare before/after metrics, download remediated data

## 🚀 Local Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone this repository or download the files
2. Ensure you have these files in the same directory:
   - `cloudmart_dashboard.py`
   - `cloudmart_multi_account.csv`
   - `requirements.txt`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the dashboard:
```bash
streamlit run cloudmart_dashboard.py
```

5. Open your browser to `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud

### Step 1: Prepare Your Repository

1. Create a new GitHub repository
2. Add these files to your repository:
   - `cloudmart_dashboard.py`
   - `cloudmart_multi_account.csv`
   - `requirements.txt`
   - `README.md` (this file)

3. Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit: CloudMart dashboard"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file path (`cloudmart_dashboard.py`)
5. Click "Deploy"

Your app will be live at: `https://<your-username>-<repo-name>.streamlit.app`

## 📁 File Structure

```
project/
├── cloudmart_dashboard.py      # Main Streamlit application
├── cloudmart_multi_account.csv # Dataset
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 📦 Dependencies

- pandas==2.3.3 - Data manipulation
- plotly==6.4.0 - Interactive visualizations
- streamlit==1.51.0 - Web dashboard framework

## 📊 Dataset Schema

The dataset includes 12 columns:
- AccountID - AWS Account ID
- ResourceID - Unique resource identifier
- Service - Cloud service type (EC2, S3, RDS, etc.)
- Region - Geographic region
- Department - Business unit
- Project - Project/application name
- Environment - Prod/Dev/Test
- Owner - Resource owner email
- CostCenter - Budget/cost code
- CreatedBy - Provisioning source
- MonthlyCostUSD - Monthly cost
- Tagged - Yes/No tagging status

## 🎯 Usage

Navigate through the dashboard sections:
1. **Data Exploration** - View dataset overview and missing values
2. **Cost Visibility** - Analyze cost distribution and identify untagged costs
3. **Tagging Compliance** - Review tag completeness and export untagged resources
4. **Visualizations** - Interactive charts with filtering capabilities
5. **Tag Remediation** - Edit tags and download remediated dataset

## 📝 Assignment Requirements

This dashboard fulfills all requirements for Week 10 Activity:
- ✅ All 5 Task Sets completed (1-5)
- ✅ All subtasks implemented with hints followed
- ✅ Interactive Streamlit dashboard
- ✅ Data visualization with Plotly
- ✅ Export functionality for remediated data
- ✅ Before/after comparison metrics
- ✅ Reflection on tagging impact

## 👨‍💻 Author

Winsome Tang - Sheridan College

## 📄 License

This project is for educational purposes (INFO 49971 - Cloud Economics).
