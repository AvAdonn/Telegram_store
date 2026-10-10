from aiogram import Router

from . import (
    basic,
    profile,
    settings
)


def get_routers() ->list:
    return [
        
        settings.settings,
        profile.profile,
        basic.basic,
    ]