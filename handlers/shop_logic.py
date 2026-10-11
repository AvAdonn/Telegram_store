from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Router, F
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters.callback_data import
from keyboards.callback import StarsChoiceCallback

from aiogram.exceptions import TelegramBadRequest

import database.requests as req
from fluentogram import TranslatorRunner

import config.images as config

import keyboards.inline_func as inl

import logging 

store = Router(name='store')
logger = logging.getLogger(__name__)

@store.message(F.text == 'Stars & Gifts')
async def btn_stars_gifts(message: Message, i18n: TranslatorRunner):
    text = i18n.get('stars_gifts')
    try:
        await message.delete()
    except TelegramBadRequest:
        logger.error('Не вдалося видалити повідомлення', exc_info=True)
        pass
    
    await message.answer_photo(
        photo=config.MY_ACCOUNT['test'],
        caption=text,
        parse_mode='HTML',
        reply_markup=inl.main_pay_menu(i18n)
    )
    
@store.callback_query(F.data == 'main:stars')
async def main_stars(callback: CallbackQuery, i18n: TranslatorRunner):
    text = i18n.get('main_stars')
    
    media = InputMediaPhoto(
        media=config.MY_ACCOUNT['my_account'],
        caption=text,
        parse_mode='HTML'
    )
    
    if isinstance(callback.message, Message):
        await callback.message.edit_media(
            media=media,
            reply_markup=inl.stars_choice(i18n)
        )
    
@store.callback_query()