import aiogram
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Router, F
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters.callback_data import CallbackData

import database.requests as req

from aiogram.exceptions import TelegramBadRequest

from fluentogram import TranslatorRunner
import config.images as config

from keyboards.callback import LanguageCallback

import keyboards.inline_func as inl

import logging

logger = logging.getLogger(__name__)
settings = Router(name='settings')

@settings.message(F.text == 'Settings')
async def btn_settings(message: Message, i18n: TranslatorRunner):
    text = i18n.get('settings')
    try:
        await message.delete()
    except TelegramBadRequest:
        pass
    await message.answer_photo(
        photo=config.MY_ACCOUNT['my_account'],
        caption=text,
        parse_mode='HTML',
        reply_markup=inl.settings(i18n)
    )

@settings.callback_query(F.data == 'set:language')
async def set_language(callback: CallbackQuery, user_in_db: User, i18n: TranslatorRunner):
    text = i18n.get('set_language')

    current_language = user_in_db.language
    media = InputMediaPhoto(
        media=config.MY_ACCOUNT['test'],
        caption=text,
        parse_mode="HTML",
    )
    try:
        if isinstance(callback.message, Message):
            await callback.message.edit_media(
                media=media,
                reply_markup=inl.language_choise(i18n, current_language)
            )
    except TelegramBadRequest as e:
        logger.warning(f'Помилка зміни зображення -> {e}')
        

@settings.callback_query(LanguageCallback.filter())
async def change_language(callback: CallbackQuery, user_in_db: User, callback_data: LanguageCallback, i18n: TranslatorRunner, session: AsyncSession):
    code = callback_data.code
    text = i18n.get('ur_language', locale=code)
    
    if code == user_in_db.language:
        await callback.answer(text)
        return
    
    text = i18n.get('change_language', locale=code)
    success = await req.change_language(code, user_in_db, session)
    if not success:
        text = i18n.get('lang_error', locale=code)
        await callback.answer(text)
        return
    
    await callback.answer(text)
    
    text = i18n.get('set_language', locale=code)

    try:
        if isinstance(callback.message, Message):
            await callback.message.edit_caption(
                caption=text,
                parse_mode='HTML',
                reply_markup=inl.language_choise(i18n, code)
            )
    except TelegramBadRequest as e:
        logger.warning(f'Помилка зміни зображення -> {e}')