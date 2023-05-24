import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

def scrape_paragen_data():
    url = "https://coinmarketcap.com/currencies/paragen/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data_elements = soup.find_all('div', class_='statsValue')

    if len(data_elements) >= 5:
        price = data_elements[0].text.strip()
        market_cap = data_elements[1].text.strip()
        volume_24h = data_elements[2].text.strip()
        total_supply = data_elements[3].text.strip()
        fully_diluted_market_cap = data_elements[4].text.strip()

        chart_image_url = soup.find('img', class_='cmc-chart-image').get('src')

        return price, market_cap, volume_24h, total_supply, fully_diluted_market_cap, chart_image_url
    else:
        return None, None, None, None, None, None

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Token Price Bot! Use /price to get the Paragen token information.")

def price(update: Update, context: CallbackContext):
    price, market_cap, volume_24h, total_supply, fully_diluted_market_cap, chart_image_url = scrape_paragen_data()

    if price and market_cap and volume_24h and total_supply and fully_diluted_market_cap and chart_image_url:
        response = f"🪙 <b>Token: Paragen</b> 🪙\n"
        response += f"💰 Price: {price}\n"
        response += f"💼 Market Cap: {market_cap}\n"
        response += f"📊 Volume (24h): {volume_24h}\n"
        response += f"🔢 Total Supply: {total_supply}\n"
        response += f"🌐 Fully Diluted Market Cap: {fully_diluted_market_cap}"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Buy", url="https://pancakeswap.finance/swap?outputCurrency=0x25382fb31e4b22e0ea09cb0761863df5ad97ed72")]
        ])
        update.message.reply_photo(chart_image_url, caption=response, reply_markup=keyboard, parse_mode='HTML')
    else:
        update.message.reply_text("Unable to fetch Paragen token data from CoinMarketCap.")

def main():
    bot_token = "6229379290:AAE4gWi4HrVb4Lh_GMkZy-_-OBMoVniswDI"
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("price", price))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
