from aiogram import Router

from . import (
    basic,
    profile,
    settings,
    shop_logic
)


def get_routers() ->list:
    return [
        
        shop_logic.store,
        settings.settings,
        profile.profile,
        basic.basic,
    ]