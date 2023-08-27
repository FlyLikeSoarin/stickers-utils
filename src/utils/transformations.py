import collections
import math

from PIL import Image, ImageFilter


def all_offsets_in_radius(radius: float) -> list[tuple[int, int]]:
    offsets = []
    grid_size = math.ceil(radius)
    squared_radius = radius**2
    for x in range(-grid_size, grid_size + 1):
        for y in range(-grid_size, grid_size + 1):
            if (x**2) + (y**2) < squared_radius:
                offsets.append((x, y))
    return offsets


def create_enlarged_background(img: Image.Image, radius: float) -> Image.Image:
    px = img.load()
    is_original = collections.defaultdict(lambda: False)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if px[x, y][3] > 25:
                is_original[(x, y)] = True
            else:
                is_original[(x, y)] = False

    offsets = all_offsets_in_radius(radius)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            px[x, y] = (0, 0, 0, 0)
            near_count = 0
            for x_offset, y_offset in offsets:
                if is_original[(x + x_offset, y + y_offset)] and px[x, y]:
                    near_count += 1
                if near_count > 10:
                    px[x, y] = (255, 255, 255, 255)
                    break

    return img.filter(ImageFilter.SMOOTH_MORE)
