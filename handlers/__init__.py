from aiogram import Router

from . import (
    basic,
    profile
)


def get_routers() ->list:
    return [
        profile.profile,
        basic.basic,
    ]