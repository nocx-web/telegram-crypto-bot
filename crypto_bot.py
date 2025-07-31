from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# Mappa simboli → ID CoinGecko
SYMBOL_MAP = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'DOGE': 'dogecoin',
    'ADA': 'cardano',
    'BNB': 'binancecoin',
    'XRP': 'ripple',
    'SOL': 'solana',
    'MATIC': 'matic-network'
}

# Recupera prezzo e variazione % della crypto
def get_crypto_data(coin_id, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}&include_24hr_change=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if coin_id in data and currency in data[coin_id]:
            price = data[coin_id][currency]
            change = data[coin_id].get(f"{currency}_24h_change", 0)
            return price, change
    return None, None

# Comando /crypto
async def crypto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usa il comando così: /crypto BTC [valuta]\nEsempio: /crypto ETH eur")
        return

    symbol = context.args[0].upper()
    currency = context.args[1].lower() if len(context.args) > 1 else 'usd'
    coin_id = SYMBOL_MAP.get(symbol)

    if not coin_id:
        await update.message.reply_text(f"❌ Crypto non supportata: {symbol}")
        return

    price, change = get_crypto_data(coin_id, currency)

    if price is not None:
        arrow = "📈" if change >= 0 else "📉"
        await update.message.reply_text(
            f"💰 Prezzo di {symbol} in {currency.upper()}:\n"
            f"{arrow} {price:.2f} ({change:.2f}% nelle ultime 24h)"
        )
    else:
        await update.message.reply_text("⚠️ Errore nel recupero dei dati.")

# Inserisci il tuo token
TOKEN = "8313527997:AAGI0Vb_91sPMTqxNu0FVVEbhkimkr814ro"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("crypto", crypto_command))

app.run_polling()
