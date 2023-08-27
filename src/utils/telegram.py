import asyncio
import os
import typing

import telegram

from src.settings import settings
from src.utils import filesystem

RoutineType = typing.Callable[[telegram.Bot], typing.Awaitable[None]]


def run_routine(routine: RoutineType):
    async def run_routine_entrypoint():
        bot = telegram.Bot(token=settings.telegram_bot_token, local_mode=True)
        async with bot:
            await routine(bot)

    asyncio.run(run_routine_entrypoint())


def get_stickerset_routine(stickerset_name: str, absolute_path: str) -> RoutineType:
    async def get_stickerset(bot: telegram.Bot):
        stickerset: telegram.StickerSet = await bot.get_sticker_set(stickerset_name)
        emoji: list[str] = []
        files: list[telegram.File] = []
        for sticker in stickerset.stickers:
            file = await bot.get_file(sticker)
            if isinstance(sticker.emoji, str) and isinstance(file, telegram.File):
                emoji.append(sticker.emoji)
                files.append(file)

        metadata = {"name": stickerset.name, "title": stickerset.title, "emoji": emoji}
        filesystem.save_json(metadata, absolute_path, filename="pack-metadata.json")

        for i, file in enumerate(files):
            filename = f"sticker-{i}.png"
            file_absolute_path = os.path.join(absolute_path, filename)
            await file.download_to_drive(file_absolute_path)

    return get_stickerset


def upload_stickerset_routine(absolute_path: str, custom_stickerset_name: str | None = None) -> RoutineType:
    async def upload_stickerset(bot: telegram.Bot):
        metadata = filesystem.load_json(absolute_path, filename="pack-metadata.json")
        if not ("name" in metadata and "title" in metadata and "emoji" in metadata):
            raise ValueError(f"Stickerset metadata is invalid for stickerset in {absolute_path}")
        stickerset_name = _create_stickerset_name(
            metadata["name"] if not custom_stickerset_name else custom_stickerset_name
        )
        stickerset_title = metadata["title"]

        input_stickers: list[telegram.InputSticker] = []
        for i, emoji in enumerate(metadata["emoji"]):
            sticker_bytes = filesystem.read_file_as_bytes(os.path.join(absolute_path, f"sticker-{i}.png"))
            input_stickers.append(telegram.InputSticker(sticker_bytes, [emoji[0]]))

        status = await bot.create_new_sticker_set(
            user_id=settings.telegram_user_id,
            name=stickerset_name,
            title=stickerset_title,
            stickers=input_stickers[:10],
            sticker_format=telegram.constants.StickerFormat.STATIC,
        )

        if status:
            print(f"Stickerset created. URL: {settings.telegram_addsticker_prefix}{stickerset_name}")
        else:
            print("Error. Stickerset not created")
            return
        
        for i in range(10, len(input_stickers)):
            print(f"Uploading images {i}")
            await bot.add_sticker_to_set(
                user_id=settings.telegram_user_id,
                name=stickerset_name,
                sticker=input_stickers[i],
            )

    return upload_stickerset


def _create_stickerset_name(name: str) -> str:
    return f"{name}_by_{settings.telegram_bot_name}"
