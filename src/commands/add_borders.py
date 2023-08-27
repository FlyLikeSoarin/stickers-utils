from src.utils import filesystem


def run(path: str):
    filesystem.modify_images(path, "_results", lambda x: x)
