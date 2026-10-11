from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Router, F
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters.callback_data import CallbackData

import database.requests as req

from aiogram.exceptions import TelegramBadRequest

from fluentogram import TranslatorRunner, TranslatorHub
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
async def change_language(
    callback: CallbackQuery,
    user_in_db: User,
    callback_data: LanguageCallback, 
    i18n: TranslatorRunner, 
    session: AsyncSession,
    hub: TranslatorHub
    ):
    code = callback_data.code
    text = i18n.get('ur_language')
    
    if code == user_in_db.language:
        await callback.answer(text)
        return
    
    success = await req.change_language(code, user_in_db, session)
    if not success:
        text = i18n.get('lang_error')
        await callback.answer(text)
        return

    new_i18n = hub.get_translator_by_locale(code)
    
    text = new_i18n.get('change_language')
    await callback.answer(text)
    
    text = new_i18n.get('set_language')

    try:
        if isinstance(callback.message, Message):
            await callback.message.edit_caption(
                caption=text,
                parse_mode='HTML',
                reply_markup=inl.language_choise(new_i18n, code)
            )
    except TelegramBadRequest as e:
        logger.warning(f'Помилка зміни зображення -> {e}')
        
        
@settings.callback_query(F.data == 'set:support')
async def support(callback: CallbackQuery, i18n: TranslatorRunner):
    text = i18n.get('support_text')
    media = InputMediaPhoto(
        media=config.MY_ACCOUNT['test'],
        caption=text,
        parse_mode='HTML'
    )
    if isinstance(callback.message, Message):
        await callback.message.edit_media(
            media=media,
            reply_markup=inl.back_settings(i18n)
        )
    await callback.answer()
    
    
@settings.callback_query(F.data == 'back_settings')
async def clb_back_settings(callback: CallbackQuery, i18n: TranslatorRunner):
    text = i18n.get('settings')
    media = InputMediaPhoto(
        media=config.MY_ACCOUNT['my_account'],
        caption=text,
        parse_mode='HTML'
    )
    if isinstance(callback.message, Message):
        await callback.message.edit_media(
            media=media,
            reply_markup=inl.settings(i18n)
        )
    await callback.answer()