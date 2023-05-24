from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from bs4 import BeautifulSoup
import requests

def start(update: Update, context: CallbackContext):
    """Handler for the /start command"""
    update.message.reply_text("Welcome to the Crypto Bot! Use the /price command to get information about Paragen token.")

def price(update: Update, context: CallbackContext):
    """Handler for the /price command"""
    url = "https://coinmarketcap.com/currencies/paragen/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting the required data
    price = soup.find(class_="priceValue___11gHJ").text.strip()
    market_cap = soup.find(text="Market Cap").find_next(class_="statsValue___2iaoZ").text.strip()
    volume_24h = soup.find(text="Volume (24h)").find_next(class_="statsValue___2iaoZ").text.strip()
    total_supply = soup.find(text="Total Supply").find_next(class_="statsValue___2iaoZ").text.strip()
    fully_diluted_market_cap = soup.find(text="Fully Diluted Market Cap").find_next(class_="statsValue___2iaoZ").text.strip()

    # Building the response
    response = "PARAGEN Token Information:\n\n"
    response += "💰 Price: {}\n".format(price)
    response += "📊 Market Cap: {}\n".format(market_cap)
    response += "🔄 Volume (24h): {}\n".format(volume_24h)
    response += "🔢 Total Supply: {}\n".format(total_supply)
    response += "💼 Fully Diluted Market Cap: {}\n".format(fully_diluted_market_cap)

    # Adding the inline button
    button_url = "https://pancakeswap.finance/swap?outputCurrency=0x25382fb31e4b22e0ea09cb0761863df5ad97ed72"
    response += "\nBuy PARAGEN on PancakeSwap: [Buy]({})".format(button_url)

    # Sending the response to the user
    update.message.reply_markdown(response)

def main():
    bot_token = "6229379290:AAE4gWi4HrVb4Lh_GMkZy-_-OBMoVniswDI"  # Replace with your actual bot token
    updater = Updater(bot_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("price", price))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
