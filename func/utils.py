from conf.settings import CHANNEL_ID, THEREAD_CHANNEL_ID, DEBUG_MODE, DEBUG_CHANNEL_ID, DEBUG_THEREAD_CHANNEL_ID, THEREAD_CHANNEL, USER_OLT, PASS_OLT

from telegram import Update
from conf.settings import MSG


async def channel_check(update: Update):
    info = {}

    if DEBUG_MODE == 'True':
        info['CHANNEL_ID'] = int(DEBUG_CHANNEL_ID)
        info['THEREAD_CHANNEL_ID'] = int(DEBUG_THEREAD_CHANNEL_ID)
    else:
        info['CHANNEL_ID'] = int(CHANNEL_ID)
        info['THEREAD_CHANNEL_ID'] = int(THEREAD_CHANNEL_ID)

    if THEREAD_CHANNEL == 'True':
        thread_id = 0

        if hasattr(update, 'message') and hasattr(update.message, 'message_thread_id'):
            thread_id = update.message.message_thread_id
        elif hasattr(update, 'callback_query') and hasattr(update.callback_query.message, 'message_thread_id'):
            thread_id = update.callback_query.message.message_thread_id
                
        if update.effective_chat.id == info['CHANNEL_ID'] and thread_id == info['THEREAD_CHANNEL_ID']:
            info['PERMISSION'] = True
    else:
        if update.effective_chat.id == info['CHANNEL_ID']:
            info['PERMISSION'] = True
        
    if info.get('PERMISSION') is None:
        info['PERMISSION'] = False
                
    return info


async def olt_check(olt):
    info = {}
        
    if olt == "230":
        info['IP'] = "172.20.0.246"
    elif olt == "231":
        info['IP'] = "172.30.0.10"
    elif olt == "232":
        info['IP'] = "172.30.0.2"
    elif olt == "233":
        info['IP'] = "172.30.0.6"
    else:
        return 0
    
    info['USER'] = USER_OLT
    info['PASS'] = PASS_OLT
    
    return info


async def error_check(code):
    if code == 0:
        return None
    
    return MSG[int(code)+100]
