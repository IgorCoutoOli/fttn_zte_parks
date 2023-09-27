from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from func.utils import channel_check
from func.command import menu
from conf.settings import information, MSG


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    INFO = await channel_check(update)
    
    if not INFO['PERMISSION']:
        return        
    
    query = update.callback_query.data

    button_cancel = [
        [InlineKeyboardButton(MSG[3] if query == 'return_menu' else MSG[4], callback_data='cancel')]
    ]

    information.pop('box', None)
    message = ""

    if query == 'provision_onu':
        information['status'] = 1
        message = MSG[12]
    elif query == 'deprovision_box':
        information['status'] = 2
        message = MSG[13]
    elif query == 'check_configuration_box':
        information['status'] = 3
        message = MSG[14]
    elif query == 'update_box':
        information['status'] = 4
        message = MSG[15]
    elif query == 'check_macs_connecteds':
        information['status'] = 5
        message = MSG[16]
    elif query == 'reboot_box':
        information['status'] = 6
        message = MSG[17]
    elif query == 'cancel':
        information['status'] = 0
        await menu(update, context)
        return
    
    await context.bot.send_message( chat_id=INFO['CHANNEL_ID'], message_thread_id=INFO['THEREAD_CHANNEL_ID'], text=message)
    await context.bot.send_message( chat_id=INFO['CHANNEL_ID'], message_thread_id=INFO['THEREAD_CHANNEL_ID'], text=MSG[18], reply_markup=InlineKeyboardMarkup(button_cancel))
