import glob
import os
import typing

from PIL import Image

ALLOWED_FILE_EXTENSIONS = (".png",)

ImageModifierType = typing.Callable[[Image.Image], Image.Image]


def modify_images(input_path: str, output_path: str, executable: ImageModifierType):
    image_paths = get_absolute_paths_for_images(input_path)
    output_path = os.path.join(get_working_directory(), output_path)

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    elif os.path.isfile():
        raise ValueError("Cannot output ot file. Output should be a directory")

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
        files = glob.glob("*", root_dir=absolute_path, recursive=False)
    else:
        files = [absolute_path]
    return [
        file
        for file in files
        if any(file.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS)
    ]


def get_working_directory() -> str:
    return os.getcwd()


def load_image(absolute_path: str) -> Image.Image:
    return Image.open(absolute_path)


def save_image(img: Image.Image, absolute_path: str):
    img.save(absolute_path)
