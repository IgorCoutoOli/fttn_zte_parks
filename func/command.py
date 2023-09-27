from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from conf.settings import information, MSG
from func.utils import channel_check


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    INFO = await channel_check(update)
    information['status'] = 0
    
    if not INFO['PERMISSION']:
        return
        
    BUTTONS_MENU = [
        [InlineKeyboardButton(MSG[5], callback_data='provision_onu')],
        [InlineKeyboardButton(MSG[6], callback_data='deprovision_box')],
        [InlineKeyboardButton(MSG[7], callback_data='check_configuration_box')],
        [InlineKeyboardButton(MSG[8], callback_data='update_box')],
        [InlineKeyboardButton(MSG[9], callback_data='check_macs_connecteds')],
        [InlineKeyboardButton(MSG[10], callback_data='reboot_box')],
    ]
    await context.bot.send_message(chat_id=INFO['CHANNEL_ID'], message_thread_id=INFO['THEREAD_CHANNEL_ID'], text=MSG[11], reply_markup=InlineKeyboardMarkup(BUTTONS_MENU))
