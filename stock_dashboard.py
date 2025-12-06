import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import mplcursors
import re
import torch
import logging
import tensorflow as tf
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go
import openai
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from alpha_vantage.fundamentaldata import FundamentalData
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, SimpleRNN, Dense, Dropout,Flatten
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.regularizers import l2


# Cấu hình logging
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Cấu hình khóa API OpenAI và Alpha Vantage
openai.api_key = ''
alpha_vantage_key = "V9JY2HAHDEH9BNHS" #có thể link hoạt tạo mã mới khi hết hạn

# Cấu hình ứng dụng
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        /* Thiết lập chung */
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #1E1E1E;
            color: #E0E0E0;
            margin: 0;
            padding: 0;
        }

        /* Tiêu đề chính */
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: 700;
            margin: 20px 0;
            color: #4CAF50;
        }

        /* Tiêu đề phụ */
        .sub-title {
            text-align: center;
            font-size: 18px;
            margin-bottom: 40px;
            color: #B0BEC5;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            background-color: #E8E8E8; /* Nền tabs sáng */
            color: #333333; /* Màu chữ */
            border-radius: 4px;
            padding: 8px 16px;
            margin-right: 5px;
            font-size: 16px;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #4CAF50; /* Nền xanh lá khi hover */
            color: white;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #4CAF50; /* Nền xanh lá khi được chọn */
            color: white;
        }
        
        
        /* Sidebar */
        .sidebar .sidebar-content {
            background-color: #2C2C2C;
            border-right: 1px solid #424242;
            padding: 20px;
        }

        /* Footer */
        footer {
            text-align: center;
            color: #B0BEC5;
            padding: 15px;
            border-top: 1px solid #424242;
            margin-top: 50px;
            background-color: #2C2C2C;
        }

        /* Nút bấm */
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            transition-duration: 0.4s;
        }

        .stButton button:hover {
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
        }

        /* Bảng */
        .stDataFrame {
            color: #E0E0E0;
            border-radius: 4px;
        }

        /* Tiêu đề bảng */
        .stDataFrame th {
            background-color: #424242;
            color: #E0E0E0;
            padding: 10px;
        }

        /* Hàng bảng */
        .stDataFrame td {
            padding: 10px;
        }

        /* Đường kẻ giữa các hàng */
        .stDataFrame tr {
            border-bottom: 1px solid #424242;
        }

        /* Đổi màu hàng khi hover */
        .stDataFrame tr:hover {
            background-color: #424242;
        }
    </style>
""", unsafe_allow_html=True)


# Thêm tiêu đề chính và phụ
st.markdown("""
    <div class="main-title">📊 Stock Analysis Dashboard</div>
    <div class="sub-title">Analyze and Predict Stock Prices with Advanced Tools</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#

# Tabs cho Pricing, Fundamental, News, và OpenAI Analysis
pricing_tab, fundamental_tab, news,ai_analysis_tab, sentiment_analysis, prediction_price = st.tabs( 
                                                                                                   
    [
        "📈 Pricing Data",
        "📊 Fundamental Data",
        "📰 FastFocus News",
        "🤖 Chat AI Analysis",
        "🧠 Sentiment Analysis",
        "📉 Stock Price Prediction",
    ]    
)

# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#


# Pricing Data Tab
with pricing_tab:
    # Sidebar: Nhập thông tin
    st.sidebar.header("📁 Stock Selection")

    # Danh sách ticker quốc tế
    tickers = {
        
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "^GSPC": "S&P500",
        "NQ=F": "Nasdaq",
        "^DJI": "Dow Jones",
        "EURUSD=X": "EUR/USD",
        "AMZN": "Amazon",
        "TSLA": "Tesla",
        "GOOGL": "Google (Alphabet)",
        "META": "Meta (Facebook)",
        "NVDA": "NVIDIA",
        "BRK-B": "Berkshire Hathaway",
        "JPM": "JPMorgan Chase",
        "V": "Visa",
        "UNH": "UnitedHealth",
        "PG": "Procter & Gamble",
        "DIS": "Disney",
        "VND=X": "USD/VND",
        'JNJ':'Johnson & Johnson',
        'XOM':'Exxon Mobil Corp.',
        'WMT':'Walmart Inc',
        'MA':'Mastercard Incorporated',
        'PFE':'Pfizer Inc.',
        'KO':'Coca-Cola Co',
        'PEP':'PepsiCo Inc',
        'CSCO':'Cisco Systems, Inc.',
        'ORCL':'Oracle Corp.',
        'INTC':'Intel Corp.'
    }

    # Chuyển dictionary thành danh sách mô tả
    ticker_selection = st.sidebar.selectbox(
        "Select a Ticker:",
        options=list(tickers.values())  # Hiển thị tên mô tả
    )

    # Lấy ticker tương ứng từ tên mô tả
    ticker = [key for key, value in tickers.items() if value == ticker_selection][0]

    # Nhập ngày bắt đầu và kết thúc
    start_date = st.sidebar.date_input("Start Date", value=datetime(2022, 1, 1))
    end_date = st.sidebar.date_input("End Date", value=datetime.now())

    # Kiểm tra ngày
    if start_date >= end_date:
        st.error("Start date must be before the end date!")

    # Lựa chọn tần suất dữ liệu
    frequency = st.sidebar.selectbox("Data Frequency", 
                                      options=["1D", "3D", "5D", "1WK", "1M", "3M", "5M", "1Y", "3Y", "5Y", "all"])

    # Lựa chọn kiểu biểu đồ
    chart_type = st.sidebar.selectbox("Chart Type", 
                                       options=["Candle", "Step", "Mountain", "Wave", "Scatter", "Line", "Bar", "Histogram"])

    # Kiểm tra dữ liệu nhập
    if not ticker:
        st.warning("Please enter a valid stock ticker!")
    else:
        # Lấy dữ liệu từ Yahoo Finance
        try:
            with st.spinner("Fetching stock data..."):
                data = yf.download(ticker, start=start_date, end=end_date)
                if data.empty:
                    st.warning("No data available for this ticker and time range.")
                else:
                    # Xử lý lỗi multi-index và loại bỏ ký hiệu ticker
                    data.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in data.columns]
                    data.columns = [col.replace(f" {ticker}", "").strip() for col in data.columns]
                    
                    # Tính %Change - sử dụng Close vì auto_adjust=True
                    # Với auto_adjust=True, Close đã được điều chỉnh và không có Adj Close
                    if 'Close' in data.columns:
                        data["%Change"] = data['Close'] / data['Close'].shift(1) - 1
                    elif 'Adj Close' in data.columns:
                        data["%Change"] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
                    else:
                        st.warning("'Close' or 'Adj Close' column not found. Skipping %Change calculation.")
                        data["%Change"] = 0  # Giá trị mặc định
                    
                    st.success(f"Data for {ticker} loaded successfully!")
                    
                    # Lưu dữ liệu vào session state
                    st.session_state['pricing_data'] = data  # Thêm dòng này
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    
    # Tùy chọn chỉ số kỹ thuật
    st.sidebar.header("Technical Indicators Options")
    technical_indicators = st.sidebar.multiselect(
        "Choose Technical Indicators:",
        options=["SMA20", "SMA50", "EMA20", "EMA50", "RSI", "MACD", "Bollinger Bands","Ichimoku Cloud", "Fibonacci Retracement",'ADX','Head and Shoulder'],
        default=["SMA20", "SMA50"]  # Không chọn mặc định, có thể thay đổi danh sách mặc định nếu muốn
    )

    # Kiểm tra các tùy chọn đã chọn
    show_sma20 = "SMA20" in technical_indicators
    show_sma50 = "SMA50" in technical_indicators
    show_ema20 = "EMA20" in technical_indicators
    show_ema50 = "EMA50" in technical_indicators
    show_rsi = "RSI" in technical_indicators
    show_macd = "MACD" in technical_indicators
    show_bollinger = "Bollinger Bands" in technical_indicators
    show_ichimoku = "Ichimoku Cloud" in technical_indicators
    show_fibonacci = "Fibonacci Retracement" in technical_indicators
    show_adx = "ADX" in technical_indicators
    show_patterns = "Head and Shoulder" in technical_indicators

    # Xử lý tần suất dữ liệu
    if not data.empty:
        data.index = pd.to_datetime(data.index)
        # Lưu dữ liệu vào session state sau khi tải thành công
        st.session_state['pricing_data'] = data

        if frequency != "1D":
            freq_mapping = {
                "3D": "3D",
                "5D": "5D",
                "1WK": "W",
                "1M": "M",
                "3M": "3M",
                "5M": "5D",
                "1Y": "A",
                "3Y": "3A",
                "5Y": "5A"
            }
            if frequency in freq_mapping:
                data = data.resample(freq_mapping[frequency]).last()

        st.header(f"Showing data with {frequency} frequency:")   
        # Tính toán hiệu suất
        if "%Change" in data.columns and data["%Change"].sum() != 0:
            annual_return = data["%Change"].mean() * 252 * 100
            stdev = np.std(data["%Change"]) * np.sqrt(252)
            st.write(f"Annual Return: {annual_return:.2f}%")
            st.write(f"Standard Deviation: {stdev * 100:.2f}%")
            if stdev != 0:
                st.write(f"Risk Adjusted Return: {annual_return / (stdev * 100):.2f}%")
        st.write(data)
        st.write(f"{chart_type} Chart") 
        # Tính toán và hiển thị chỉ số kỹ thuật nếu được chọn
        if 'Close' in data.columns:
            if show_sma20:
                data['SMA20'] = data['Close'].rolling(window=20).mean()
            if show_sma50:
                data['SMA50'] = data['Close'].rolling(window=50).mean()
            if show_ema20:
                data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
            if show_ema50:
                data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
                
            if show_rsi:
                delta = data['Close'].diff(1)
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                avg_gain = gain.rolling(window=14).mean()
                avg_loss = loss.rolling(window=14).mean()
                rs = avg_gain / avg_loss
                data['RSI'] = 100 - (100 / (1 + rs))
            if show_macd:
                exp1 = data['Close'].ewm(span=12, adjust=False).mean()
                exp2 = data['Close'].ewm(span=26, adjust=False).mean()
                data['MACD'] = exp1 - exp2
                data['MACD Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
                
            if show_bollinger:
                data['BB_Middle'] = data['Close'].rolling(window=20).mean()
                data['BB_Upper'] = data['BB_Middle'] + (data['Close'].rolling(window=20).std() * 2)
                data['BB_Lower'] = data['BB_Middle'] - (data['Close'].rolling(window=20).std() * 2)
            # Tính toán và hiển thị Ichimoku Cloud
            if show_ichimoku:
                data['Tenkan_Sen'] = (data['High'].rolling(9).max() + data['Low'].rolling(9).min()) / 2
                data['Kijun_Sen'] = (data['High'].rolling(26).max() + data['Low'].rolling(26).min()) / 2
                data['Senkou_Span_A'] = ((data['Tenkan_Sen'] + data['Kijun_Sen']) / 2).shift(26)
                data['Senkou_Span_B'] = (data['High'].rolling(52).max() + data['Low'].rolling(52).min()) / 2
                
            # Fibonacci Retracement
            if show_fibonacci:
                high = data['High'].max()
                low = data['Low'].min()
                levels = {
                    "0%": high,
                    "23.6%": high - 0.236 * (high - low),
                    "38.2%": high - 0.382 * (high - low),
                    "50%": high - 0.5 * (high - low),
                    "61.8%": high - 0.618 * (high - low),
                    "100%": low,
                }
                # Lưu các mức Fibonacci vào data
                for level, value in levels.items():
                    data[level] = value
            # Tính ADX (Average Directional Index)
            if show_adx:
                def calculate_adx(data, n=14):
                    high = data['High']
                    low = data['Low']
                    close = data['Close']
                    
                    plus_dm = high.diff().clip(lower=0)
                    minus_dm = (-low.diff()).clip(lower=0)
                    
                    tr = pd.concat([high - low, abs(high - close.shift()), abs(low - close.shift())], axis=1).max(axis=1)
                    atr = tr.rolling(window=n).mean()
                    
                    plus_di = 100 * (plus_dm.rolling(window=n).mean() / atr)
                    minus_di = 100 * (minus_dm.rolling(window=n).mean() / atr)
                    
                    adx = 100 * abs((plus_di - minus_di) / (plus_di + minus_di)).rolling(window=n).mean()
                    return adx

                data['ADX'] = calculate_adx(data)

        # # Hiển thị dữ liệu chỉ khi có chỉ số kỹ thuật được chọn
        # if any([show_sma20, show_sma50, show_ema20, show_ema50, show_rsi, show_macd, show_bollinger,show_ichimoku,show_fibonacci,show_adx]):
        #     st.write("📊 Technical Indicators")
        #     st.write(data)

        # Tạo biểu đồ
        fig = go.Figure()

        # Biểu đồ chính
        if chart_type == "Line":
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
        elif chart_type == "Step":
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', line_shape='hv', name='Step'))
        elif chart_type == "Mountain":
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], fill='tozeroy', mode='lines', name='Mountain'))
        elif chart_type == "Wave":
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', line=dict(shape='spline', smoothing=1.3), name='Wave'))
        elif chart_type == "Scatter":
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='markers', name='Scatter'))
        elif chart_type == "Candle":
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick',
                increasing=dict(line=dict(color='green'), fillcolor='green'),  # Màu xanh cho tăng giá
                decreasing=dict(line=dict(color='red'), fillcolor='red')  # Màu đỏ cho giảm giá
            ))
        elif chart_type == "Bar":
            fig.add_trace(go.Bar(x=data.index, y=data['Close'], name='Bar'))
        elif chart_type == "Histogram":
            fig.add_trace(go.Histogram(x=data['Close'], name='Histogram'))
            

        # Thêm các chỉ số kỹ thuật vào biểu đồ nếu được chọn
        if show_sma20 and 'SMA20' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], mode='lines', name='SMA20', line=dict(color='blue', dash='dash')))
        if show_sma50 and 'SMA50' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'], mode='lines', name='SMA50', line=dict(color='green', dash='dash')))
        if show_ema20 and 'EMA20' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], mode='lines', name='EMA20', line=dict(color='orange', dash='dot')))
        if show_ema50 and 'EMA50' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], mode='lines', name='EMA50', line=dict(color='red', dash='dot')))
            
        if show_bollinger and 'BB_Upper' in data.columns and 'BB_Lower' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['BB_Upper'], mode='lines', line=dict(dash='dash', color='purple'), name='BB Upper'))
            fig.add_trace(go.Scatter(x=data.index, y=data['BB_Lower'], mode='lines', line=dict(dash='dash', color='red'), name='BB Lower'))
            
        if show_rsi and 'RSI' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI', yaxis='y2', line=dict(color='purple')))
        if show_macd and 'MACD' in data.columns and 'MACD Signal' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD', yaxis='y3', line=dict(color='cyan')))
            fig.add_trace(go.Scatter(x=data.index, y=data['MACD Signal'], mode='lines', name='MACD Signal', yaxis='y3', line=dict(color='magenta')))
            
        if show_ichimoku and 'Tenkan_Sen' in data.columns and 'Kijun_Sen' in data.columns and 'Senkou_Span_A' in data.columns and 'Senkou_Span_B' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['Tenkan_Sen'], name="Tenkan_Sen"))
            fig.add_trace(go.Scatter(x=data.index, y=data['Kijun_Sen'], name="Kijun_Sen"))
            fig.add_trace(go.Scatter(x=data.index, y=data['Senkou_Span_A'], name="Senkou Span A"))
            fig.add_trace(go.Scatter(x=data.index, y=data['Senkou_Span_B'], name="Senkou Span B"))
            
        if show_fibonacci:
            for level in levels.keys():
                if level in data.columns:
                    fig.add_trace(go.Scatter(
                        x=[data.index.min(), data.index.max()],
                        y=[data[level][0], data[level][0]],  # Giá trị cố định trên toàn biểu đồ
                        mode="lines",
                        name=level,
                        line=dict(dash="dot")
                    ))
        if show_adx and 'ADX' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['ADX'], mode='lines', name='ADX', line=dict(color='purple')))

        # Nhận diện Chart Patterns (ví dụ: Head and Shoulders)
        # Tùy chọn Sidebar
        window_size = st.sidebar.slider("Window Size for Pattern Detection", 5, 50, 10)
        # window_size điều chỉnh phạm vi dữ liệu kiểm tra để tìm "vai trái" và "vai phải".
        # Nên thử nghiệm với các giá trị window_size khác nhau để tìm ra giá trị phù hợp nhất với dữ liệu và khung thời gian phân tích của mình.

        # Hàm phát hiện Head and Shoulders
        def detect_head_and_shoulders(data, window=10):
            data['Head_and_Shoulders'] = 0  # Mặc định không có mẫu
            for i in range(window, len(data) - window):
                left_shoulder = data['High'][i - window:i].max()
                head = data['High'][i]
                right_shoulder = data['High'][i + 1:i + window + 1].max()

                # Điều kiện để là Head and Shoulders
                if left_shoulder < head and right_shoulder < head and abs(left_shoulder - right_shoulder) <= (0.05 * head):
                    data.loc[data.index[i], 'Head_and_Shoulders'] = 1
            return data

        # Nhận diện Head and Shoulders
        if show_patterns:
            # Gọi hàm phát hiện Head and Shoulders
            data = detect_head_and_shoulders(data, window=window_size)
            hs_pattern = data[data['Head_and_Shoulders'] == 1]

            # Thêm vào biểu đồ
            fig.add_trace(go.Scatter(
                x=hs_pattern.index, 
                y=hs_pattern['Close'], 
                mode='markers', 
                name='Head and Shoulders',
                marker=dict(size=10, color='red', symbol='triangle-up')
            ))

            # Hiển thị bảng nếu có mẫu được phát hiện
            if not hs_pattern.empty:
                st.write("Detected Head and Shoulders Patterns:")
                st.dataframe(hs_pattern[['High', 'Close']])
            else:
                st.write("No Head and Shoulders patterns detected.")

            # Cập nhật layout biểu đồ
            fig.update_layout(
                title=f"{ticker} Stock Chart with Selected Indicators",
                yaxis=dict(title="Stock Price (USD)"),
                xaxis=dict(title="Date", tickformat="%d-%m-%Y"),
                hovermode="x unified",
            )

    # Hiển thị biểu đồ
    st.plotly_chart(fig)


# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#

#Fundamental Data Tab
with fundamental_tab:
    st.write("Feature under development.")
    # fd = FundamentalData(alpha_vantage_key, output_format="pandas")
    # try:
    #     st.subheader("Balance Sheet")
    #     balance_sheet = fd.get_balance_sheet_annual(ticker)[0].T[2:]
    #     balance_sheet.columns = list(fd.get_balance_sheet_annual(ticker)[0].T.iloc[0])
    #     st.write(balance_sheet)

    #     st.subheader("Income Statement")
    #     income_statement = fd.get_income_statement_annual(ticker)[0].T[2:]
    #     income_statement.columns = list(fd.get_income_statement_annual(ticker)[0].T.iloc[0])
    #     st.write(income_statement)

    #     st.subheader("Cash Flow Statement")
    #     cash_flow = fd.get_cash_flow_annual(ticker)[0].T[2:]
    #     cash_flow.columns = list(fd.get_cash_flow_annual(ticker)[0].T.iloc[0])
    #     st.write(cash_flow)
    # except Exception as e:
    #     st.error(f"Error fetching fundamental data: {e}")


# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#

#News Tab
with news:
    # Hàm chuyển đổi thời gian tương đối thành thời gian thực
    def convert_relative_date(relative_date):
        if "minute" in relative_date:
            minutes = int(relative_date.split()[0])
            return datetime.now() - timedelta(minutes=minutes)
        elif "hour" in relative_date:
            hours = int(relative_date.split()[0])
            return datetime.now() - timedelta(hours=hours)
        elif "day" in relative_date:
            days = int(relative_date.split()[0])
            return datetime.now() - timedelta(days=days)
        else:
            return datetime.now()  # Trả về thời gian hiện tại nếu không xác định được

    # Hàm scrape dữ liệu
    def scrape_investing_news(page_num, max_articles=5): # Thêm tham số max_articles với giá trị mặc định là 5
        url = f"https://www.investing.com/news/stock-market-news/{page_num}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.warning(f"Failed to retrieve page {page_num}: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_='news-analysis-v2_content__z0iLP w-full text-xs sm:flex-1')

        news_data = []
        for article in articles:
            if len(news_data) >= max_articles:  # Dừng nếu đã đạt số bài cần crawl
                break
            try:
                # Lấy tiêu đề
                title = article.find(
                    'a',
                    class_='text-inv-blue-500 hover:text-inv-blue-500 hover:underline focus:text-inv-blue-500 focus:underline whitespace-normal text-sm font-bold leading-5 !text-[#181C21] sm:text-base sm:leading-6 lg:text-lg lg:leading-7'
                ).get_text(strip=True)

                # Lấy thời gian
                date_text = article.find('time').get_text(strip=True)
                if "ago" in date_text:
                    date = convert_relative_date(date_text).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    date = date_text

                # Lấy liên kết bài viết chi tiết
                link = article.find('a')['href']
                if link.startswith("http"):
                    full_link = link
                else:
                    full_link = f"https://www.investing.com{link}"

                # Lấy nội dung bài viết chi tiết
                try:
                    detail_response = requests.get(full_link, headers=headers, timeout=15)
                    detail_response.raise_for_status()
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    content_div = detail_soup.find('div', class_='article_WYSIWYG__O0uhw article_articlePage__UMz3q text-[18px] leading-8')
                    content = content_div.get_text(strip=True) if content_div else "No Content Available"
                except requests.exceptions.RequestException as e:
                    content = f"Error retrieving content: {e}"

                news_data.append({"title": title, "date": date, "content": content})
            except Exception as e:
                st.warning(f"Error processing article: {e}")

        return news_data

    # Biến lưu trữ số trang hiện tại
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1  # Mặc định là trang đầu tiên

    # Tổng số trang
    total_pages = 10  # Có thể thay đổi theo thực tế

    # Giao diện điều hướng trang
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)  # Đường phân cách đẹp

    # Điều hướng trong một hàng
    col1, col2, col3 = st.columns([1, 7, 1])  # Chỉnh tỷ lệ các cột để cân đối hơn

    # Nút "Previous" ở cột trái
    with col1:
        if st.button("Previous") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1

    # Phần "Go to page: [số trang]" ở cột giữa
    with col2:
        st.markdown(
            "<div style='text-align: center; font-size: 16px;'><b>Go to page:</b></div>",
            unsafe_allow_html=True,
        )
        selected_page = st.number_input(
            "Page Number",
            min_value=1,
            max_value=total_pages,
            value=st.session_state.current_page,
            step=1,
            label_visibility="collapsed",  # Ẩn nhãn mặc định
        )
        # Cập nhật số trang nếu người dùng thay đổi giá trị
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page

    # Nút "Next" ở cột phải
    with col3:
        if st.button("Next") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1

    # Hiển thị số trang hiện tại
    st.subheader(f"Page {st.session_state.current_page} of {total_pages}")

    # Lấy dữ liệu từ trang hiện tại với giới hạn số bài viết
    page = st.session_state.current_page
    news = scrape_investing_news(page)

    # Hiển thị kết quả
    if not news:
        st.warning(f"No news found for page {page}")
    else:
        for index, item in enumerate(news, start=1):
            st.subheader(f"News {index}")
            st.write(f"📅 Published: {item['date']}")
            st.write(f"📰 Title: {item['title']}")
            with st.expander("Read More"):
                st.write(item['content'])

# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#

# AI Analysis Tab
with ai_analysis_tab:

    # Kiểm tra xem người dùng đã nhập ticker hay chưa
    if not ticker :
        st.warning("Please enter a valid stock ticker to proceed with AI Analysis.")
    else:
        import time
        from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError
        
        # Hàm để lấy phản hồi từ OpenAI
        def get_ai_response(prompt):
            try:
                client = OpenAI(api_key=openai.api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                )
                time.sleep(2)  # Chờ 2 giây trước khi gửi yêu cầu tiếp theo
                return response.choices[0].message.content
            except AuthenticationError:
                return "Error: Invalid API Key. Please check your API Key."
            except RateLimitError:
                return "Error: Rate limit exceeded. Please try again later."
            except APIConnectionError:
                return "Error: Unable to connect to OpenAI servers. Check your internet connection."
            except Exception as e:
                return f"Error while fetching AI response: {e}"
    # Ô nhập và nút submit
    st.subheader("Custom AI Query")
    user_input = st.text_area("Enter your question or prompt below:", f"3 Reasons why buying {ticker} stock")
    if st.button("Submit", key="ai_analysis_submit"):
        if not user_input.strip():
            st.warning("Please enter a valid input before submitting.")
        else:
            response = get_ai_response(user_input.strip())
            if response.startswith("Error"):
                st.error(response)  # Hiển thị lỗi chi tiết
            else:
                st.write(response)

# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#

# Tab dự đoán giá
with prediction_price:
        # Session state để lưu dữ liệu sau khi chuẩn bị
        if 'uploaded_file' not in st.session_state:
            st.session_state['uploaded_file'] = None
        if 'prepared_data' not in st.session_state:
            st.session_state['prepared_data'] = None
        if 'selected_columns' not in st.session_state:
            st.session_state['selected_columns'] = None
        if 'pricing_data' not in st.session_state:
            st.session_state['pricing_data'] = None

        # st.header("🤖 Stock Price Prediction")
        
        # Chọn nguồn dữ liệu
        st.subheader("Select Data Source")
        data_source = st.radio(
            "Choose data source for prediction:",
            options=["Use Pricing Data", "Upload Custom Data"]
        )

        if data_source == "Use Pricing Data":
            # Kiểm tra nếu có dữ liệu từ tab Pricing
            if st.session_state.get('pricing_data') is None:
                st.error("No pricing data available. Please fetch data from the Pricing tab.")
                st.stop()
            else:
                data = st.session_state['pricing_data']
                # Loại bỏ giá trị inf và -inf
                data.replace([np.inf, -np.inf], np.nan, inplace=True)
                # Xóa các giá trị NaN phát sinh từ chỉ số kỹ thuật
                data.dropna(inplace=True)
                
                st.write(f"Using {ticker} Pricing Data:")
                st.write(data)

        elif data_source == "Upload Custom Data":
            st.subheader("Data Preparation")
            uploaded_file = st.file_uploader("Upload Data (CSV or Excel)", type=["csv", "xlsx"])

            if uploaded_file is not None:
                # Đọc dữ liệu
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file)
                    st.success("CSV file loaded successfully!")
                elif uploaded_file.name.endswith('.xlsx'):
                    data = pd.read_excel(uploaded_file)
                    st.success("Excel file loaded successfully!")
                else:
                    st.error("Unsupported file format. Please upload a CSV or Excel file.")
                    st.stop()
                    

                # Xử lý dữ liệu
                if 'Date' in data.columns or isinstance(data.iloc[0, 0], pd.Timestamp):
                    data['Date'] = pd.to_datetime(data['Date'])
                    data.set_index('Date', inplace=True)

                # Xử lý các cột chứa ký tự 'K', 'M', '%'
                for col in data.columns:
                    if data[col].dtype == 'object':
                        data[col] = data[col].replace(r'K', 'e3', regex=True).replace(r'M', 'e6', regex=True)
                        data[col] = data[col].replace('%', '', regex=True).astype(float) / 100
                        data[col] = pd.to_numeric(data[col], errors='coerce')
                # Loại bỏ giá trị inf và -inf
                data.replace([np.inf, -np.inf], np.nan, inplace=True)
                # Loại bỏ gái trị NaN
                data.dropna(inplace=True)
                st.session_state['prepared_data'] = data
                st.write("Uploaded and Cleaned Data:")
                st.write(data)
            else:
                st.stop()

        # Lựa chọn các biến đầu vào
        st.subheader("Select Input Features for Prediction")
        available_columns = data.columns.tolist()
        selected_columns = st.multiselect("Select Features", available_columns, default=available_columns)

        if not selected_columns:
            st.error("Please select at least one feature.")
            st.stop()
        else:
            data = data[selected_columns]
            st.session_state['prepared_data'] = data
            st.write("Selected Data for Modeling:")
            st.write(data)

        # Điều chỉnh tham số
        st.subheader("Adjust Parameters")
        n_past = st.number_input("Number of Past Days (n_past)", min_value=5, max_value=60, value=30, step=1)
        n_future = st.number_input("Number of Future Days (n_future)", min_value=1, max_value=30, value=7, step=1)
        n_target = st.number_input("Specific date in the future to predict (n_target)", min_value=1, max_value=30, value=5, step=1)
        train_test_split = st.slider("Train-Test Split Ratio", min_value=0.1, max_value=0.9, value=0.8, step=0.01)

        # Chuẩn hóa dữ liệu
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data.values)

        train_size = int(len(scaled_data) * train_test_split)
        train_data = scaled_data[:train_size]
        test_data = scaled_data[train_size - n_past:]  # Đảm bảo tính liên tục của chuỗi

        # Xem shape dữ liệu
        st.subheader("Train-Test Data Shape")
        st.write(f"Train Data: {train_data.shape}")
        st.write(f"Test Data: {test_data.shape}")

        # Điều chỉnh batch size và epochs
        batch_size = st.number_input("Batch Size", min_value=8, max_value=256, value=50, step=8)
        epochs = st.number_input("Epochs", min_value=10, max_value=500, value=100, step=10)

        # Chọn mô hình
        st.subheader("Choose Model")
        model_type = st.selectbox("Model Type", ["LSTM", "RNN", "DNN"])

        # Huấn luyện mô hình
        if st.button("Train Model"):
            with st.spinner("Training model... This may take some time."):

                # Tạo chuỗi cho train và test
                trainX, trainY = [], []
                for i in range(n_past, len(train_data) - n_future + 1):
                    trainX.append(train_data[i - n_past:i, :])
                    trainY.append(train_data[i + n_target - 1, 0])

                testX, testY = [], []
                for i in range(n_past, len(test_data) - n_future + 1):
                    testX.append(test_data[i - n_past:i, :])
                    testY.append(test_data[i + n_target - 1, 0])

                trainX, trainY = np.array(trainX), np.array(trainY)
                testX, testY = np.array(testX), np.array(testY)

                # Xóa bộ nhớ cache của TensorFlow trước khi xây dựng mô hình mới
                tf.keras.backend.clear_session()
                # Xây dựng mô hình
                model = Sequential()
                if model_type == "LSTM":
                    # First LSTM layer
                    model.add(LSTM(units=64, return_sequences=True, input_shape=(trainX.shape[1], trainX.shape[2]),
                                kernel_regularizer=l2(0.01)))
                    model.add(Dropout(0.3))  # Increase dropout to avoid overfitting
                    model.add(BatchNormalization())  # Normalize activations
                    # Second LSTM layer
                    model.add(LSTM(units=50, return_sequences=True, kernel_regularizer=l2(0.01)))
                    model.add(Dropout(0.3))
                    model.add(BatchNormalization())
                    # Third LSTM layer
                    model.add(LSTM(units=32, return_sequences=False, kernel_regularizer=l2(0.01)))
                    model.add(Dropout(0.3))
                    model.add(BatchNormalization())
                    # Fully connected layers
                    model.add(Dense(units=50, activation='relu', kernel_regularizer=l2(0.01)))  # Fully connected layer
                    model.add(Dropout(0.3))  # Dropout for the dense layer
                elif model_type == "RNN":
                    model.add(SimpleRNN(units=64, return_sequences=True, input_shape=(trainX.shape[1], trainX.shape[2]),
                kernel_regularizer=l2(0.01)))
                    model.add(Dropout(0.3))  # Increase dropout to avoid overfitting
                    model.add(BatchNormalization())  # Normalize activations
                    # Second RNN layer
                    model.add(SimpleRNN(units=50, return_sequences=True, kernel_regularizer=l2(0.01)))
                    model.add(Dropout(0.3))
                    model.add(BatchNormalization())
                    # Third RNN layer
                    model.add(SimpleRNN(units=32, return_sequences=False, kernel_regularizer=l2(0.01)))
                    model.add(Dropout(0.3))
                    model.add(BatchNormalization())
                    # Fully connected layers
                    model.add(Dense(units=50, activation='relu', kernel_regularizer=l2(0.01)))  # Fully connected layer
                    model.add(Dropout(0.3))  # Dropout for the dense layer
                elif model_type == "DNN":
                    # Flatten layer để chuyển đổi dữ liệu đầu vào từ 3D sang 2D (nếu cần)
                    model.add(Dense(units=128, activation='relu', input_shape=(trainX.shape[1], trainX.shape[2])))
                    model.add(Dropout(0.3))  # Dropout to reduce overfitting
                    model.add(Dense(units=64, activation='relu'))
                    model.add(Dropout(0.3))
                    model.add(Dense(units=32, activation='relu'))
                    model.add(Dropout(0.3))
                    model.add(Flatten()) # Add a Flatten layer to reshape the output

                model.add(Dense(1))
                model.compile(optimizer="adam", loss="mean_squared_error")

                # Early stopping
                early_stopping = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
                history = model.fit(trainX, trainY, batch_size=batch_size, epochs=epochs,
                                    validation_data=(testX, testY), callbacks=[early_stopping])

                # Dự đoán và đánh giá
                predictions = model.predict(testX)
                testY_full = scaler.inverse_transform(np.hstack([testY.reshape(-1, 1), np.zeros((testY.shape[0], data.shape[1] - 1))]))[:, 0]
                predictions_full = scaler.inverse_transform(np.hstack([predictions, np.zeros((predictions.shape[0], data.shape[1] - 1))]))[:, 0]
                
                # Xác định test_start_date
                if isinstance(data.index, pd.DatetimeIndex):
                    test_start_date = data.index[train_size]  # Ngày đầu tiên của tập dữ liệu kiểm tra
                else:
                    st.error("Data does not have a datetime index. Please include a 'Date' column.")
                    st.stop()
                
                # Tạo DataFrame hiển thị ngày và giá dự đoán
                dates = pd.date_range(start=test_start_date, periods=len(predictions_full), freq='B')  # 'B' để sử dụng ngày làm việc
                df_predictions = pd.DataFrame({
                    "Date": dates,
                    "Actual Price": testY_full,
                    "Predicted Price": predictions_full
                })
                
                
                mae = mean_absolute_error(testY_full, predictions_full)
                mse = mean_squared_error(testY_full, predictions_full)
                rmse = np.sqrt(mse)
                mape = np.mean(np.abs((testY_full - predictions_full) / testY_full)) * 100
                r2 = r2_score(testY_full, predictions_full)

                # Tạo bảng kết quả
                evaluation_metrics = {
                    "Metric": ["Mean Absolute Error (MAE)", 
                            "Mean Squared Error (MSE)", 
                            "Root Mean Squared Error (RMSE)", 
                            "Mean Absolute Percentage Error (MAPE)", 
                            "R² Score"],
                    "Value": [mae, mse, rmse, mape, r2]
                }

                df_metrics = pd.DataFrame(evaluation_metrics)

                # Hiển thị bảng kết quả
                st.subheader("Evaluation Metrics")
                st.dataframe(df_metrics)

                # Plot kết quả bằng Plotly
                st.subheader("Prediction Results")
                st.dataframe(df_predictions)

                # Tạo biểu đồ Plotly
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=dates, y=testY_full, mode='lines', name='Actual', line=dict(width=2)))
                fig.add_trace(go.Scatter(x=dates, y=predictions_full, mode='lines', name='Predicted', line=dict(width=2)))

                # Thêm tiêu đề và nhãn trục
                fig.update_layout(
                    title=f"{model_type} Prediction Results Chart",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    legend=dict(x=0, y=1),
                    template="plotly_white"  # Giao diện nền trắng
                )

                # Hiển thị biểu đồ
                st.plotly_chart(fig)
                
                            
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#

#Sentiment Analysis Tab
with sentiment_analysis:
    # Lưu mô hình và tokenizer vào bộ nhớ để tránh tải lại
    @st.cache_resource
    def load_model():
        tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        return tokenizer, model

    tokenizer, model = load_model()

    # Hàm phân tích cảm xúc
    def get_sentiment(text):
        if not text or text.strip() == "":  # Kiểm tra nếu văn bản rỗng
            return {'positive': 0.0, 'neutral': 0.0, 'negative': 0.0}

        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)

        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        scores = probabilities.detach().cpu().numpy()[0]

        # Thay thế NaN bằng 0 nếu cần
        scores = [0 if np.isnan(score) else score for score in scores]

        return {
            'positive': float(scores[0]),
            'negative': float(scores[1]),
            'neutral': float(scores[2])
        }

# Phân tích cảm xúc
    st.header("Analyszing sentiment score from news")
    user_input = st.text_area(" your input sentence in English:","Bitcoin’s Rally Stalls After Nearing the Historic $100,000 Level")
    if st.button("Submit", key="sentiment_analysis_submit"):
        if user_input.strip():
            sentiment_result = get_sentiment(user_input)

            # Hiển thị kết quả phân tích cảm xúc
            st.subheader("Results:")
            st.write(f"**Positive:** {sentiment_result['positive']:.2f}")
            st.write(f"**Negative:** {sentiment_result['negative']:.2f}")
            st.write(f"**Neutral:** {sentiment_result['neutral']:.2f}")

            # Tải kết quả dưới dạng Excel
            data = pd.DataFrame([sentiment_result])
            st.download_button(
                label="Download result as csv",
                data=data.to_csv(index=False),
                file_name="sentiment_analysis.csv",
                mime="text/csv",
            )
        else:
            st.warning("Please enter text to analyze!")
# Footer
st.markdown(
    """
    <footer style="text-align: center; margin-top: 50px; color: #9ca3af; padding: 10px; border-top: 1px solid #333333;">
        © 2024 Stock Dashboard | Powered by <a href="https://finance.yahoo.com/" target="_blank" style="color: #10b981;">Finance.yahoo.com</a>
    </footer>
    """,
    unsafe_allow_html=True
)
