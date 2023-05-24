import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

def get_token_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "X-CMC_PRO_API_KEY": "0a244b8b-3664-4305-842e-d0a8b8027e4a"
    }
    params = {
        "id": "18450",
        "convert_id": "2781",
        "aux": "num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,market_cap_by_total_supply,volume_24h_reported,volume_7d,volume_7d_reported,volume_30d,volume_30d_reported,is_active,is_fiat"
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if response.status_code == 200 and "data" in data:
        return data["data"]["18450"]
    else:
        return None

def get_chart_image_url():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "X-CMC_PRO_API_KEY": "0a244b8b-3664-4305-842e-d0a8b8027e4a"
    }
    params = {
        "id": "18450",
        "convert_id": "2781",
        "aux": "chart",
        "interval": "1d"
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if response.status_code == 200 and "data" in data:
        return data["data"]["18450"]["chart"]["1d"]
    else:
        return None

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Token Price Bot! Use /price to get token information.")

def price(update: Update, context: CallbackContext):
    token_data = get_token_data()
    chart_image_url = get_chart_image_url()

def price(update: Update, context: CallbackContext):
    token_data = get_token_data()

    if token_data:
        price = token_data["quote"]["2781"]["price"]
        price = "{:.8f}".format(price)  # Format price to 8 decimal places
        volume_24h = token_data["quote"]["2781"]["volume_24h"]
        total_supply = token_data["total_supply"]
        all_time_high = token_data["quote"]["2781"].get("ath", "N/A")

        response = "🪙 <b>Token: Paragen</b> 🪙\n"
        response += f"💰 Price: {price}\n"
        response += f"📊 Volume (24h): {volume_24h}\n"
        response += f"🌐 Total Supply: {total_supply}\n"
        response += f"🚀 All-time High: {all_time_high}\n\n"
        response += "Paragen is a chain agnostic launchpad and incubator native to the BSC network. Its goal is to offer an extremely fair tiered system with guaranteed allocations focused on gaming and metaverse projects. 🎮🌌\n"

        keyboard = [
            [
                InlineKeyboardButton("Paragen - 🌐", url="https://t.me/paragenio"),
                InlineKeyboardButton("Marketing - 💼", url="https://t.me/BullionDOT"),
                InlineKeyboardButton("Buy - 💰", url="https://pancakeswap.finance/swap?outputCurrency=0x25382fb31e4b22e0ea09cb0761863df5ad97ed72"),
            ],
            [
                InlineKeyboardButton("Website - 🌐", url="https://paragen.io/"),
                InlineKeyboardButton("Project - 📋", url="https://paragen.io/projects"),
                InlineKeyboardButton("CMC - 💎", url="https://coinmarketcap.com/dexscan/bsc/0x447ff4dd9cee7f751cf3eb253dbb3c227747b31c/"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(response, parse_mode='HTML', reply_markup=reply_markup)
    else:
        update.message.reply_text("Unable to fetch token data.")


def main():
    bot_token = "6229379290:AAFZ5WTSqW-H1jGlpsrsZFQRPS9JITHPsS0"
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("price", price))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
