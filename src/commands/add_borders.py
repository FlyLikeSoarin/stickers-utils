from PIL import Image

from src.utils import filesystem, transformations


def run(stickerset_name: str):
    copy_postfix = "_wb"
    original_path = filesystem.get_or_create_directory(f"_results/{stickerset_name}")
    copy_path = filesystem.get_or_create_directory(f"_results/{stickerset_name}{copy_postfix}")
    filesystem.copy_stickerset(original_path, copy_path, copy_postfix)
    filesystem.modify_images(copy_path, copy_path, routine)


def routine(img: Image.Image) -> Image.Image:
    background_img_size = (512 + 32, 512 + 32)
    img_position = (
        int(16 + (512 - img.size[0]) / 2),
        int(16 + (512 - img.size[1]) / 2),
    )
    try:
        background_img = Image.new("RGBA", background_img_size)
        background_img.paste(img, img_position, img)
        background_img = transformations.create_enlarged_background(background_img, 9.0)
    except (IndexError, ValueError):
        return img
    background_img.paste(img, img_position, img)
    return background_img.resize((512, 512))
