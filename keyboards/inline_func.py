from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner
import config.languages as config
import config.const as const
from keyboards.callback import LanguageCallback, StarsChoiceCallback


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

def settings(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=i18n.get('btn_language'),
        callback_data='set:language',
        icon_custom_emoji_id='4940645878684713890'
    )
    builder.button(
        text=i18n.get('btn_politic'),
        url='https://telegra.ph/Terms-of-Service--Privacy-Policy-10-10',
        icon_custom_emoji_id='5974229895906069525'
    )
    builder.button(
        text=i18n.get('btn_support'),
        callback_data='set:support',
        style='success',
        icon_custom_emoji_id='5443038326535759644'
    )
    
    builder.adjust(2, 1)
    
    return builder.as_markup()

def language_choise(new_i18n: TranslatorRunner, current_language: str | None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for code, text in config.AVAILABLE_LANGUAGES.items():
        text = f'•{text}' if code == current_language else text
        builder.button(
            text=text,
            callback_data=LanguageCallback(code=code).pack(),
        )
        
    builder.button(
        text=new_i18n.get('back'),
        callback_data='back_settings'
    )
    
    builder.adjust(2,1)
    
    return builder.as_markup()

def back_settings(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    text = i18n.get('btn_back_settings')
    builder.button(
        text=text,
        callback_data='back_settings'
    )
    
    return builder.as_markup()

def main_pay_menu(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=i18n.get('btn_stars'),
        callback_data='main:stars'
    )
    
    builder.button(
        text=i18n.get('btn_premium'),
        callback_data='main:premium'
    )
    
    builder.button(
        text=i18n.get('btn_gifts'),
        callback_data='main:gifts'
    )
    builder.button(
        text=i18n.get('btn_ton'),
        callback_data='main:ton'
    )
    builder.button(
        text=i18n.get('btn_reviews'),
        callback_data='reviews'
    )
    builder.adjust(2, 2, 1)
    return builder.as_markup()

def stars_choice(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for amount in const.STARS_CHOICE:
        builder.button(
            text=i18n.get(f'stars_{amount}'),
            callback_data=StarsChoiceCallback(amount=amount).pack()
        )
    builder.button(
        text=i18n.get('stars_other'),
        callback_data='stars:other'
    )
    
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()