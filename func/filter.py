from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from conf.settings import information, MSG
from func.utils import channel_check

from func.script import check_info, check_macs, reboot_box, remove_box, adding_box, update_box


async def filter_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    INFO = await channel_check(update)

    if not INFO['PERMISSION'] or information['status'] < 1:
        return

    result = {}

    if 'box' not in information:
        information['box'] = update.message.text.lower()

        if len(information['box']) != 7:
            result['message'] = MSG[2]
            information.pop('box', None)
        elif information['status'] == 1 or information['status'] == 2:
            result['message'] = MSG[19]
        elif information['status'] == 3:  # Verificar configurações
            result = await check_info()
        elif information['status'] == 4:  # Atualizar caixa
            result = await update_box()
        elif information['status'] == 5:  # Verificar MAC's conectados
            result = await check_macs()
        elif information['status'] == 6:  # Reiniciar caixa
            result = await reboot_box()
    else:
        information['serial'] = update.message.text.lower()

        if information['status'] == 1:  # Provisionamento
            result = await adding_box()
        elif information['status'] == 2:  # Desprovisionamento
            result = await remove_box()

    button_cancel = [
        [InlineKeyboardButton(MSG[4] if not result.get('status', None) else MSG[3], callback_data='cancel')]
    ]

    await context.bot.send_message(chat_id=INFO['CHANNEL_ID'], message_thread_id=INFO['THEREAD_CHANNEL_ID'],
                                   text=result['message'], reply_markup=InlineKeyboardMarkup(button_cancel))
