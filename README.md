# ⚙️ Financial Data Pipeline & Analytics System

## 🎯 Overview
An end-to-end data engineering system that collects, processes, and integrates financial market data and news into a unified analytics pipeline.

Designed to handle large-scale structured and unstructured datasets (130K+ records) and support real-time analytics.

---

## 🚀 Key Highlights
- Built ETL pipeline processing 130,000+ records
- Integrated stock data (API) + financial news (web scraping)
- Designed workflow: ingestion → transformation → serving
- Reduced processing time by ~30%
- Enabled near real-time data updates

---

## 🏗 System Architecture
Data Sources (Yahoo Finance, Investing.com)
        ↓
Data Ingestion (API, Scraping)
        ↓
Data Cleaning & Transformation
        ↓
Feature Engineering (NLP + Time-series)
        ↓
Processed Data Storage
        ↓
Serving Layer (Streamlit Dashboard)

---

## 🔧 Core Components

### 📥 Data Ingestion
- Real-time stock data via Yahoo Finance API  
- Financial news scraping (Investing.com)  
- Batch and near real-time data collection  

### 🔄 ETL Pipeline
- Data cleaning, normalization, validation  
- Feature engineering for analytics & ML  
- Integration of structured + unstructured data  

### 🧠 Data Processing
- NLP pipeline using FinBERT (sentiment scoring)  
- Time-series alignment between news & stock data  
- Optimized processing (~30% faster)  

### 📤 Data Serving
- Streamlit dashboard for data exploration  
- Supports real-time updates  

---

## 🛠 Tech Stack
- Python, SQL  
- Pandas, NumPy  
- Requests, BeautifulSoup  
- Transformers (FinBERT)  
- Streamlit  

---

## ▶️ Run the Project
```bash
git clone <repo-url>
cd <repo-name>
pip install -r requirements.txt
streamlit run stock_dashboard.py
