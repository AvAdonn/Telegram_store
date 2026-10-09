from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

def my_account(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=i18n.get('btn_referral'),
        callback_data='aa',
        icon_custom_emoji_id='5472262490903554982'
    )
    builder.button(
        text=i18n.get('btn_calculate'),
        callback_data='ba',
        icon_custom_emoji_id='6003585735381225018'
    )
    builder.button(
        text=i18n.get('btn_cupon'),
        callback_data='ab',
        style='danger',
        icon_custom_emoji_id='5377599075237502153'
    )
    builder.adjust(2, 1)
    
    return builder.as_markup()