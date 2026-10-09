import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from fluentogram import TranslatorRunner
import database.requests as req

from keyboards.reply import main_kb

logger = logging.getLogger(__name__)
basic = Router(name='basic')

@basic.message(CommandStart())
async def cmd_start(
    message: Message,
    session: AsyncSession,
    command: CommandObject,
    user_in_db: User | None,
    i18n: TranslatorRunner
):
    if user_in_db:
        text = i18n.get('hello_user')
        await message.answer(text, reply_markup=main_kb)
        
        return

    if not message.from_user:
        return
    
    user_id = message.from_user.id
    
    args = command.args
    referral_id = None
    
    if args and args.isdigit():
        parsed_args = int(args)
        if parsed_args != user_id:
            referral_id = parsed_args
        else:
            logger.info('Спроба самореферала!')
            
    language = message.from_user.language_code or 'en'
    logger.info(f'User {user_id}: Telegram language_code: {language}')
    
    await req.add_user(session, user_id, referral_id=referral_id, language=language)
    text = i18n.get('hello_db')
    await message.answer(text, reply_markup=main_kb)
    

@basic.message(F.photo)
async def photo_info(message: Message):
    file_id = message.photo[-1].file_id if message.photo else 'Nimaphoto'
    await message.reply(f'<code>{file_id}</code>', parse_mode='HTML')    

@basic.message()
async def emoji_info(message: Message):
    if not message.entities:
        return
    
    for entity in message.entities:
        if entity.type == 'custom_emoji':
            await message.reply(f'<code>{entity.custom_emoji_id}</code>', parse_mode='HTML')
