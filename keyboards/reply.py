from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Stars & Gifts', style='primary', icon_custom_emoji_id='5179278706941624825')],
    [KeyboardButton(text='Settings', icon_custom_emoji_id='5398095118735521227'),
     KeyboardButton(text='My Account', icon_custom_emoji_id='5397911500293683969')]
], resize_keyboard=True)