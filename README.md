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
<img width="459" height="172" alt="{F5FC556B-F740-4846-8E49-A717B3046CAE}" src="https://github.com/user-attachments/assets/91f52a5a-764e-49d0-9f10-283a25aecdba" />

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
<img width="455" height="255" alt="{0C0034DB-080D-45A4-B3A2-9FC2F463534C}" src="https://github.com/user-attachments/assets/9ddbb6da-ab44-4c75-9b01-6396a36c9958" />

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
