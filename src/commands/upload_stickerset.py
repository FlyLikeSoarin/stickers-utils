from src.utils import filesystem, telegram


def run(stickerset_name: str):
    absolute_path = filesystem.get_or_create_directory(f"_results/{stickerset_name}")
    telegram.run_routine(telegram.upload_stickerset_routine(absolute_path))
