import glob
import json
import os
import typing
from distutils import dir_util

from PIL import Image

ALLOWED_FILE_EXTENSIONS = (".png",)

ImageModifierType = typing.Callable[[Image.Image], Image.Image]


def modify_images(input_path: str, output_path: str, executable: ImageModifierType):
    image_paths = get_absolute_paths_for_images(input_path)
    output_path = get_or_create_directory(output_path)

    for image_path in image_paths:
        image_basename = os.path.basename(image_path)
        print(f"Loading {image_basename}")
        image = load_image(image_path)
        print(f"Processing {image_basename}")
        image = executable(image)
        print(f"Saving {image_basename} to {output_path}")
        save_image(image, os.path.join(output_path, image_basename))


def get_absolute_paths_for_images(path: str) -> list[str]:
    absolute_path = os.path.join(get_working_directory(), path)
    if os.path.isdir(absolute_path):
        files = [
            os.path.join(absolute_path, basename)
            for basename in glob.glob("*", root_dir=absolute_path, recursive=False)
        ]
    else:
        files = [absolute_path]
    return [file for file in files if any(file.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS)]


def get_working_directory() -> str:
    return os.getcwd()


def get_or_create_directory(path: str) -> str:
    if path.startswith("/"):
        output_path = path
    else:
        output_path = os.path.join(get_working_directory(), path)

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    elif os.path.isfile(output_path):
        raise ValueError("Cannot output ot file. Output should be a directory")

    return output_path


def load_image(absolute_path: str) -> Image.Image:
    return Image.open(absolute_path)


def save_image(img: Image.Image, absolute_path: str):
    img.save(absolute_path)


def load_json(absolute_path: str, *, filename: str | None = None) -> typing.Any:
    path = absolute_path if filename is None else os.path.join(absolute_path, filename)
    with open(path, "r") as f:
        return json.load(f)


def save_json(data: typing.Any, absolute_path: str, *, filename: str | None = None):
    path = absolute_path if filename is None else os.path.join(absolute_path, filename)
    with open(path, "w") as f:
        json.dump(data, f)


def read_file_as_bytes(absolute_path: str):
    with open(absolute_path, "rb") as f:
        return f.read()


def copy_stickerset(original_path: str, copy_path: str, copy_postfix: str):
    dir_util.copy_tree(original_path, copy_path)
    metadata = load_json(copy_path, filename="pack-metadata.json")
    if not copy_postfix or not copy_postfix.startswith("_"):
        raise ValueError("new_name cannot be empty")
    metadata["name"] = metadata["name"] + copy_postfix
    save_json(metadata, copy_path, filename="pack-metadata.json")
