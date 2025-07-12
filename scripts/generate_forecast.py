import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os

# 股票清單
stocks = {
    "2330.TW": "台積電",
    "3711.TW": "日月光",
    "6683.TWO": "雍智科技"
}

today = datetime.date.today()
start_date = today - datetime.timedelta(days=120)

# 建立資料夾
os.makedirs("data", exist_ok=True)
os.makedirs("charts", exist_ok=True)

summary_html = "<h1>📈 台股預測報告</h1>\n"

for symbol, name in stocks.items():
    df = yf.download(symbol, start=start_date, end=today)
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA20"] = df["Close"].rolling(20).mean()

    df.to_csv(f"data/{symbol}.csv")

    # 繪圖
    plt.figure(figsize=(10, 5))
    plt.plot(df["Close"], label="Close Price")
    plt.plot(df["MA5"], label="MA5")
    plt.plot(df["MA20"], label="MA20")
    plt.title(f"{name}（{symbol}）技術分析")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    chart_path = f"charts/{symbol}.png"
    plt.savefig(chart_path)
    plt.close()

    # 預測（簡單 rule-based 模型）
    last = df.iloc[-1]
    ma_signal = "看多 📈" if last["MA5"] > last["MA20"] else "偏空 📉"
    summary_html += f"""
    <h2>{name}（{symbol}）</h2>
    <img src="{chart_path}" width="600">
    <p>收盤價：{last['Close']:.2f} 元<br>
    MA5：{last['MA5']:.2f} / MA20：{last['MA20']:.2f} → <b>{ma_signal}</b></p>
    <hr>
    """

# 儲存 index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"""
    <html>
    <head><meta charset="UTF-8"><title>每日預測</title></head>
    <body style="font-family:sans-serif;">
    {summary_html}
    <p>每日早上 07:00 自動更新（資料來源：Yahoo Finance）</p>
    </body></html>
    """)
