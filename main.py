from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from decouple import config
from crypto_data import get_rates
from disk_usage import disk_usage
import json

def print_disk_usage(loc='/'):
     location, total, used = disk_usage(location=loc)
     return f"location: {location}\ntotal_disk: {total}G\nused_disk: {used}G"




API_ID=config('API_ID')
API_HASH=config('API_HASH')
BOT_TOKEN=config('BOT_TOKEN')


app = Client(name="test-bot", 
             api_id=API_ID, 
             api_hash=API_HASH, 
             bot_token=BOT_TOKEN)




@app.on_message(filters.command("start"))
def my_handler(client: Client, msg: Message):
    msg.reply_text(text="HI, Welcom to this bot.", 
                   reply_markup=InlineKeyboardMarkup(
                       [[InlineKeyboardButton(text='get_rates', callback_data="get_rates")],
                        [InlineKeyboardButton(text='disk_usage_root', callback_data="disk_usage_root")],
                        [InlineKeyboardButton(text='disk_usage_home', callback_data="disk_usage_home")],]
                   ))

@app.on_callback_query()
def on_callback(client: Client, call_back: CallbackQuery):
    if call_back.data == 'get_rates':
        call_back.message.reply_text(f"{json.dumps(get_rates(), indent=2)}\n based on EURO.")
    elif call_back.data == 'disk_usage_root':
        call_back.message.reply_text(print_disk_usage(loc='/'))
    elif call_back.data == 'disk_usage_home':
        call_back.message.reply_text(print_disk_usage(loc='/home'))




app.run()
