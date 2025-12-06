<div align="center">

# 📊 Stock Analysis Dashboard

### *Your Complete AI-Powered Stock Market Intelligence Platform*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*A comprehensive stock analysis and prediction dashboard featuring real-time data analysis, advanced technical indicators, AI-powered sentiment analysis, and state-of-the-art machine learning price predictions.*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

---

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 📈 **Pricing Data Analysis**
- 🔴 **Real-time Stock Data** from Yahoo Finance
- 📊 **8 Chart Types**: Candle, Line, Bar, Step, Mountain, Wave, Scatter, Histogram
- 🎯 **Advanced Technical Indicators**:
  - Moving Averages (SMA20/50, EMA20/50)
  - RSI, MACD, Bollinger Bands
  - Ichimoku Cloud
  - Fibonacci Retracement
  - Average Directional Index (ADX)
- 🔍 **Pattern Recognition**: Head & Shoulders
- ⏰ **Flexible Timeframes**: 1D to 5Y
- 📐 **Performance Metrics**: Returns, Volatility, Risk-Adjusted Returns

</td>
<td width="50%">

### 🤖 **AI-Powered Analysis**
- 🧠 **GPT-4o Integration** for intelligent insights
- 💬 **Custom Query Engine** for personalized analysis
- 📰 **Real-time News Scraping** from Investing.com
- 🎭 **Sentiment Analysis** using FinBERT
- 📊 **Sentiment Scoring**: Positive, Negative, Neutral
- 💾 **Export Results** to CSV

</td>
</tr>
<tr>
<td width="50%">

### 📉 **Price Prediction Engine**
- 🔬 **Multiple ML Models**:
  - 🧬 LSTM (Long Short-Term Memory)
  - 🔄 RNN (Recurrent Neural Network)
  - 🎯 DNN (Deep Neural Network)
- 📁 **Custom Data Upload** (CSV/Excel)
- ⚙️ **Adjustable Parameters**: Window size, epochs, batch size
- 📏 **Evaluation Metrics**: MAE, MSE, RMSE, MAPE, R²
- 📊 **Interactive Visualizations** with Plotly

</td>
<td width="50%">

### 📊 **Fundamental Analysis**
- 💼 Balance Sheet Analysis *(Coming Soon)*
- 💰 Income Statement *(Coming Soon)*
- 💵 Cash Flow Statement *(Coming Soon)*
- 📈 Financial Ratios *(Planned)*

</td>
</tr>
</table>

## 🚀 Quick Start

### 📋 Prerequisites

```plaintext
✅ Python 3.8 or higher
✅ pip package manager
✅ OpenAI API Key (for AI Analysis)
✅ Alpha Vantage API Key (for Fundamental Data)
```

### 💻 Installation

**1️⃣ Clone the repository**
```bash
git clone <repository-url>
cd hehe
```

**2️⃣ Install dependencies**
```bash
pip install streamlit pandas numpy matplotlib torch tensorflow yfinance plotly openai requests beautifulsoup4 alpha_vantage transformers scikit-learn
```

**3️⃣ Configure API Keys**

Open `stock_dashboard.py` and update:
```python
openai.api_key = 'your-openai-api-key-here'
alpha_vantage_key = "your-alpha-vantage-key-here"
```

> 💡 **Get your API keys:**
> - OpenAI: https://platform.openai.com/api-keys
> - Alpha Vantage: https://www.alphavantage.co/support/#api-key

**4️⃣ Launch the dashboard**
```bash
streamlit run stock_dashboard.py
```

**5️⃣ Open your browser**
```plaintext
🌐 Navigate to: http://localhost:8501
```

## 📦 Core Dependencies

<div align="center">

| Category | Libraries |
|----------|-----------|
| **Web Framework** | `streamlit` |
| **Data Processing** | `pandas`, `numpy` |
| **Visualization** | `matplotlib`, `plotly` |
| **Machine Learning** | `torch`, `tensorflow`, `scikit-learn` |
| **Financial Data** | `yfinance`, `alpha_vantage` |
| **AI & NLP** | `openai`, `transformers` |
| **Web Scraping** | `requests`, `beautifulsoup4` |

</div>

## 🎯 How to Use

<details open>
<summary><b>📈 Pricing Data Analysis</b></summary>

1. Select a stock ticker from the sidebar dropdown
2. Choose date range (start and end dates)
3. Select data frequency (1D to 5Y)
4. Pick your preferred chart type
5. Enable technical indicators from the sidebar
6. Adjust pattern detection window size
7. View real-time charts and metrics

</details>

<details>
<summary><b>📰 FastFocus News</b></summary>

1. Navigate to the News tab
2. Browse paginated stock market news
3. Use Previous/Next buttons or jump to specific page
4. Click "Read More" to view full article content
5. Stay updated with latest market developments

</details>

<details>
<summary><b>🤖 AI Analysis</b></summary>

1. Go to Chat AI Analysis tab
2. Enter your stock ticker in Pricing tab first
3. Type custom questions or analysis requests
4. Click Submit to get AI-powered insights
5. Receive intelligent recommendations and analysis

</details>

<details>
<summary><b>🧠 Sentiment Analysis</b></summary>

1. Navigate to Sentiment Analysis tab
2. Enter financial text or news headline
3. Click Submit to analyze sentiment
4. View positive, negative, and neutral scores
5. Download results as CSV for further analysis

</details>

<details>
<summary><b>📉 Price Prediction</b></summary>

1. Choose data source (Pricing Data or Upload Custom)
2. Select input features for prediction
3. Adjust model parameters:
   - n_past (historical window)
   - n_future (prediction horizon)
   - n_target (specific target day)
   - Train-test split ratio
4. Choose ML model (LSTM/RNN/DNN)
5. Configure batch size and epochs
6. Click "Train Model" and wait for results
7. View predictions, metrics, and visualizations

</details>

## 🎨 Supported Assets

<div align="center">

### 🌍 Global Coverage

| Category | Tickers |
|----------|---------|
| **📱 Tech Giants** | AAPL, MSFT, GOOGL, META, NVDA, AMZN, TSLA |
| **📊 Major Indices** | ^GSPC (S&P 500), NQ=F (Nasdaq), ^DJI (Dow Jones) |
| **💰 Financial** | JPM, V, MA, BRK-B |
| **🏥 Healthcare** | UNH, JNJ, PFE |
| **🛒 Consumer Goods** | WMT, PG, KO, PEP, DIS |
| **⚡ Energy** | XOM |
| **💻 Technology** | CSCO, ORCL, INTC |
| **💱 Forex** | EURUSD=X, VND=X |

*...and many more available through Yahoo Finance!*

</div>

## ⚙️ Configuration Guide

### 🎨 Technical Indicators Customization

| Parameter | Range | Description |
|-----------|-------|-------------|
| **Window Size** | 5-50 days | Pattern detection sensitivity |

### 🤖 ML Model Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| **n_past** | 5-60 | 30 | Historical window size |
| **n_future** | 1-30 | 7 | Prediction horizon |
| **n_target** | 1-30 | 5 | Specific prediction day |
| **Train-Test Split** | 0.1-0.9 | 0.8 | Data splitting ratio |
| **Batch Size** | 8-256 | 50 | Training batch size |
| **Epochs** | 10-500 | 100 | Training iterations |

> 💡 **Pro Tip**: Start with default values and adjust based on your data characteristics and computational resources.

## 🧬 Model Architecture

<table>
<tr>
<td width="33%">

### 🔷 LSTM Model
```
Input Layer
    ↓
LSTM(64) + Dropout(0.3)
    ↓
BatchNorm
    ↓
LSTM(50) + Dropout(0.3)
    ↓
BatchNorm
    ↓
LSTM(32) + Dropout(0.3)
    ↓
Dense(50) + Dropout(0.3)
    ↓
Output Layer
```
**Features:**
- ✅ Long-term dependencies
- ✅ L2 regularization
- ✅ Early stopping

</td>
<td width="33%">

### 🔶 RNN Model
```
Input Layer
    ↓
RNN(64) + Dropout(0.3)
    ↓
BatchNorm
    ↓
RNN(50) + Dropout(0.3)
    ↓
BatchNorm
    ↓
RNN(32) + Dropout(0.3)
    ↓
Dense(50) + Dropout(0.3)
    ↓
Output Layer
```
**Features:**
- ✅ Sequential patterns
- ✅ L2 regularization
- ✅ Early stopping

</td>
<td width="33%">

### 🔸 DNN Model
```
Input Layer
    ↓
Dense(128) + Dropout(0.3)
    ↓
Dense(64) + Dropout(0.3)
    ↓
Dense(32) + Dropout(0.3)
    ↓
Flatten
    ↓
Output Layer
```
**Features:**
- ✅ ReLU activation
- ✅ Fast training
- ✅ Simple architecture

</td>
</tr>
</table>

## 🛡️ Error Handling & Logging

```plaintext
📝 Comprehensive Logging
   ├── 📄 error.log - Detailed error tracking
   ├── 🔍 User-friendly messages
   ├── 🚦 API rate limit handling
   ├── 🔐 Authentication validation
   └── 🌐 Connection error recovery
```

## 🎨 UI/UX Excellence

<div align="center">

| Feature | Description |
|---------|-------------|
| 🌙 **Dark Theme** | Professional, eye-friendly interface |
| 📱 **Responsive** | Optimized for all screen sizes |
| 📊 **Interactive Charts** | Powered by Plotly |
| 🗂️ **Tabbed Navigation** | Clean, organized layout |
| 🎛️ **Sidebar Controls** | Easy parameter adjustment |
| 💾 **Export Options** | Download results instantly |
| ⚡ **Real-time Updates** | Live data synchronization |

</div>

## 📝 Important Notes

> 🔑 **API Keys Required**
> - OpenAI API for AI Analysis features
> - Alpha Vantage API for fundamental data (may require renewal)

> 📡 **Data Sources**
> - Yahoo Finance: Real-time stock data
> - Investing.com: Market news (rate-limited)
> - ProsusAI/finbert: Sentiment analysis (auto-downloaded)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

```plaintext
🐛 Report bugs
💡 Suggest features
📝 Improve documentation
🔧 Submit pull requests
⭐ Star the repository
```

<div align="center">

**[Open an Issue](../../issues)** • **[Submit a PR](../../pulls)** • **[View Discussions](../../discussions)**

</div>

## 📄 License

<div align="center">

**MIT License** © 2024 Stock Analysis Dashboard

Powered by [Yahoo Finance](https://finance.yahoo.com/) | Built with ❤️ using Python

</div>

## 🔮 Roadmap & Future Enhancements

<table>
<tr>
<td width="50%">

### 🚀 Version 2.0 (Q1 2026)
- [ ] 📊 Complete Fundamental Data integration
- [ ] 🔍 Advanced pattern recognition (Cup & Handle, Double Top/Bottom)
- [ ] 💼 Portfolio management & tracking
- [ ] 🔔 Real-time alerts & notifications

</td>
<td width="50%">

### 🌟 Version 3.0 (Q2 2026)
- [ ] 📱 Mobile-responsive design
- [ ] 💾 Database integration for predictions
- [ ] 🌐 Multi-language support
- [ ] 🤖 Custom AI models & ensemble methods

</td>
</tr>
</table>

## 📞 Support & Community

<div align="center">

### Need Help?

| Resource | Description |
|----------|-------------|
| 📖 **[Documentation](#)** | Complete usage guide |
| 🐛 **[Issue Tracker](../../issues)** | Report bugs |
| 💬 **[Discussions](../../discussions)** | Ask questions |
| 📧 **[Email](mailto:support@example.com)** | Direct support |
| 📝 **error.log** | Check local logs |

</div>

---

<div align="center">

### 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/stock-dashboard&type=Date)](https://star-history.com/#yourusername/stock-dashboard&Date)

### Built With

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

### 💝 Made with Love

**Developed by passionate developers for the trading community**

*If you find this project useful, consider giving it a ⭐!*

---

**© 2024-2025 Stock Analysis Dashboard** | **[View License](LICENSE)** | **[Report Security Issue](SECURITY.md)**

</div>
