BOT_TOKEN = "8884280500:AAGRr9_I6ALbOv6-PkScvyWTHTIPHHhhhQbU"
CHANNEL = "@TSGOnlineTrading"
import requests, time, random
from datetime import datetime

# Pocket Option popular pairs (crypto + OTC)
SYMBOLS = {
    "BTCUSDT": "BTC/USD OTC",
    "ETHUSDT": "ETH/USD OTC", 
    "SOLUSDT": "SOL/USD OTC",
    "EURUSDT": "EUR/USD OTC",
    "GBPUSDT": "GBP/USD OTC"
}

def get_rsi(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=100"
    r = requests.get(url, timeout=10).json()
    closes = [float(x[4]) for x in r]
    gains = []; losses = []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        if diff >= 0: gains.append(diff); losses.append(0)
        else: gains.append(0); losses.append(abs(diff))
    avg_gain = sum(gains[:14]) / 14
    avg_loss = sum(losses[:14]) / 14
    for i in range(14, len(gains)):
        avg_gain = (avg_gain * 13 + gains[i]) / 14
        avg_loss = (avg_loss * 13 + losses[i]) / 14
    if avg_loss == 0:
        return 100, closes[-1]
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi, closes[-1]

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL, "text": text, "parse_mode": "Markdown"})

send("✅ *POCKET OPTION BOT ONLINE*\n\n📊 Channel: @TSGOnlineTrading\n⏰ Timeframe: 5M\n🎯 Strategy: RSI Reversal\n🔄 Scanning 24/7 OTC...")

while True:
    for binance_symbol, po_pair in SYMBOLS.items():
        try:
            rsi, price = get_rsi(binance_symbol)
            now = datetime.now().strftime("%H:%M:%S")
            
            if rsi <= 30:
                msg = f"""🟢 *POCKET OPTION SIGNAL* 🟢

💱 Pair: `{po_pair}`
📈 Action: *BUY / CALL* ⬆️
⏰ Expiry: *5 Minutes*
💰 Price: `${price:,.2f}`
📊 RSI: `{rsi:.1f}` - *OVERSOLD*

✅ Strategy: RSI Reversal
⚡️ Valid till: {now}
🔗 @TSGOnlineTrading"""
                send(msg)

            elif rsi >= 70:
                msg = f"""🔴 *POCKET OPTION SIGNAL* 🔴

💱 Pair: `{po_pair}`
📉 Action: *SELL / PUT* ⬇️
⏰ Expiry: *5 Minutes*
💰 Price: `${price:,.2f}`
📊 RSI: `{rsi:.1f}` - *OVERBOUGHT*

✅ Strategy: RSI Reversal
⚡️ Valid till: {now}
🔗 @TSGOnlineTrading"""
                send(msg)

        except Exception as e:
            print(f"Error {binance_symbol}: {e}")
            
    time.sleep(180)  # Check every 3 minutes
