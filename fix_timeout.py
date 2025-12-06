# Script to fix timeout issue
with open(r'd:\stock_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix timeout in scrape_investing_news
content = content.replace(
    'response = requests.get(url, headers=headers, timeout=2)',
    'response = requests.get(url, headers=headers, timeout=10)'
)

# Also fix timeout in detail_response if exists
content = content.replace(
    'detail_response = requests.get(full_link, headers=headers, timeout=10)',
    'detail_response = requests.get(full_link, headers=headers, timeout=15)'
)

with open(r'd:\stock_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed timeout issues successfully!")
