# ⚙️ Financial Data Pipeline & Analytics System

## 🎯 Overview

An end-to-end data engineering system that collects, processes, and integrates financial market data and news into a unified analytics pipeline.
Designed to handle **large-scale structured and unstructured datasets (130K+ records)** and support near real-time analytics.
This project uniquely combines **financial news sentiment (PhoBERT + FinBERT)** with **stock price time-series data** to enable advanced analytics and forecasting.
<img width="1901" height="876" alt="image" src="https://github.com/user-attachments/assets/f95d749e-05e8-44e2-a31f-f440b6155d7b" />
<img width="1497" height="776" alt="image" src="https://github.com/user-attachments/assets/ce1ae214-1f04-46d9-bf08-09de9f4572eb" />

---

## 🚀 Key Highlights

* Built an ETL pipeline processing **130,000+ records**
* Integrated **stock data (API)** with **financial news (web scraping)**
* Designed a complete workflow: **ingestion → processing → feature engineering → serving**
* Reduced processing time by **~30%** through pipeline optimization
* Enabled **near real-time data updates** for analytics and visualization
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/98ef06ee-c123-4818-820e-709898c0864e" />

---

## 🧠 Novelty & Technical Contribution

This project goes beyond traditional stock analysis by combining **NLP** and **time-series financial data** in one unified pipeline.

* **Hybrid NLP Integration**
  Uses **PhoBERT** for Vietnamese text understanding and **FinBERT** for finance-oriented sentiment extraction

* **Cross-domain Data Fusion**
  Combines **unstructured data** (financial news) with **structured data** (stock prices, indicators)

* **Time-series Alignment**
  Aligns sentiment signals with stock price movements to support downstream analysis and forecasting

* **Sentiment-driven Feature Engineering**
  Generates sentiment-based features that enrich predictive modeling and analytics workflows

---

## 🏗️ System Architecture

![System Architecture](./images/architecture.png)

```text
Data Sources (Yahoo Finance, Investing.com)
        ↓
Data Ingestion (API, Web Scraping)
        ↓
Data Cleaning & Transformation
        ↓
Feature Engineering (PhoBERT + FinBERT + Time-series)
        ↓
Processed Data Storage
        ↓
Serving Layer (Streamlit Dashboard)
```

---

## 🔄 Data Pipeline Flow

![Data Pipeline Flow](./images/pipeline.png)

```text
News / Market APIs
        ↓
Ingestion
        ↓
Cleaning / Normalization / Deduplication
        ↓
Sentiment Extraction (PhoBERT + FinBERT)
        ↓
Time-series Merge with Stock Data
        ↓
Feature Store / Processed Dataset
        ↓
Dashboard / Forecasting / Analytics
```

---

## 📊 Dashboard Preview

![Dashboard Preview](./images/dashboard.png)

---

## 🧩 System Design Explanation

The system is designed as a modular data pipeline with five main layers:

1. **Data Ingestion Layer**
   Collects stock price data from APIs and financial news from web sources.
   Supports batch collection and near real-time updates.

2. **Processing & ETL Layer**
   Cleans, validates, normalizes, and transforms raw data into a consistent format.

3. **NLP & Feature Engineering Layer**
   Uses **PhoBERT** and **FinBERT** to extract sentiment from Vietnamese financial news, then aligns those signals with stock price time-series data to create enriched analytical features.

4. **Storage Layer**
   Stores processed datasets for efficient querying, dashboarding, and downstream forecasting tasks.

5. **Serving Layer**
   Exposes processed data through a **Streamlit dashboard** for interactive exploration and visualization.

### Design Considerations

* **Modularity:** Each stage is separated for easier maintenance and future scaling
* **Scalability:** Can be extended with Airflow, Kafka, Spark, or cloud infrastructure
* **Data Consistency:** Ensured through validation, normalization, and deduplication
* **Performance:** Optimized processing reduced runtime by about **30%**
* **Extensibility:** New data sources or models can be integrated with minimal redesign

---

## 🔧 Core Components

### 📥 Data Ingestion

* Real-time stock data via Yahoo Finance API
* Financial news scraping from Investing.com
* Batch and near real-time data collection

### 🔄 ETL Pipeline

* Data cleaning, normalization, and validation
* Deduplication and transformation
* Integration of structured and unstructured data

### 🧠 NLP & Data Processing

* Vietnamese text representation with **PhoBERT**
* Financial sentiment extraction with **FinBERT**
* Sentiment scoring and feature generation
* Time-series alignment between news and stock data

### 📤 Data Serving

* Streamlit dashboard for exploration and visualization
* Supports analytics and prediction workflows

---

## 🛠 Tech Stack

* **Languages:** Python, SQL
* **Data Processing:** Pandas, NumPy
* **Scraping & APIs:** Requests, BeautifulSoup, yfinance
* **NLP:** PhoBERT, FinBERT, Transformers
* **Visualization:** Streamlit, Plotly
* **Modeling:** LSTM, time-series forecasting

---

## ▶️ Run the Project

```bash
git clone <repo-url>
cd <repo-name>
pip install -r requirements.txt
streamlit run stock_dashboard.py
```

---

## 📁 Suggested Repository Structure

```text
project-root/
├── images/
│   ├── architecture.png
│   ├── pipeline.png
│   └── dashboard.png
├── stock_dashboard.py
├── requirements.txt
└── README.md
```

---

## 📈 Why This Project Matters

This project demonstrates:

* Real-world **data pipeline architecture**
* Integration of **multiple heterogeneous data sources**
* Practical use of **PhoBERT + FinBERT** in a finance setting
* Strong **ETL, NLP, and time-series engineering** skills
* End-to-end thinking from ingestion to serving

---

## 🔮 Future Improvements

* Add **Airflow** for orchestration
* Add **Kafka** for streaming ingestion
* Store data in a **data warehouse**
* Deploy on **AWS / GCP**
* Build a dedicated **feature store** for downstream models
