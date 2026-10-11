import aiogram
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession


from aiogram.exceptions import TelegramBadRequest

from fluentogram import TranslatorRunner
import config.images as config

import keyboards.inline_func as inl

import logging

logger = logging.getLogger(__name__)
profile = Router(name='profile')

@profile.message(F.text == 'My Account')
async def my_account(
    message: Message,
    user_in_db: User,
    i18n: TranslatorRunner
):
    logger.debug('Команда: My Account')
    guest = i18n.get('guest')
    if message.from_user and message.from_user.username:
        username = message.from_user.username
    else:
        username = guest
         
    text = i18n.get(
        'my_account',
        username=username,
        user_id=str(user_in_db.tg_id).strip(),
        stars=user_in_db.stars,
        gifts=user_in_db.gifts,
        premium=user_in_db.premium,
        date=user_in_db.created
    )
    try:
        await message.delete()
    except TelegramBadRequest:
        pass
    logger.warning(
        "PROFILE I18N: object=%s, caption=%r, referral=%r, "
        "calculate=%r, coupon=%r",
        id(i18n),
        i18n.get("btn_referral"),
        i18n.get("btn_calculate"),
        i18n.get("btn_cupon"),
    )
    await message.answer_photo(
        photo=config.MY_ACCOUNT['my_account'],
        caption=text,
        parse_mode='HTML',
        reply_markup=inl.my_account(i18n)
    )
