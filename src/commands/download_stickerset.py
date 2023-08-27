from src.settings import settings
from src.utils import filesystem, telegram


def run(stickerset_name: str):
    if stickerset_name.startswith(settings.telegram_addsticker_prefix):
        stickerset_name = stickerset_name[len(settings.telegram_addsticker_prefix):]
    telegram.run_routine(
        telegram.get_stickerset_routine(
            stickerset_name, filesystem.get_or_create_directory(f"_results/{stickerset_name}")
        ),
    )
