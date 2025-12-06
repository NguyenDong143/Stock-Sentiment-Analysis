# Script to fix Adj Close issue
with open(r'd:\stock_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic section
old_code = """                    # Kiểm tra cột 'Adj Close' tồn tại trước khi tính %Change
                    if 'Adj Close' in data.columns:
                        data["%Change"] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
                    else:
                        st.warning("'Adj Close' column not found. Skipping %Change calculation.")
                        data["%Change"] = 0  # Giá trị mặc định"""

new_code = """                    # Tính %Change - sử dụng Close vì auto_adjust=True
                    # Với auto_adjust=True, Close đã được điều chỉnh và không có Adj Close
                    if 'Close' in data.columns:
                        data["%Change"] = data['Close'] / data['Close'].shift(1) - 1
                    elif 'Adj Close' in data.columns:
                        data["%Change"] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
                    else:
                        st.warning("'Close' or 'Adj Close' column not found. Skipping %Change calculation.")
                        data["%Change"] = 0  # Giá trị mặc định"""

content = content.replace(old_code, new_code)

with open(r'd:\stock_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed successfully!")
