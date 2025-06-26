import os

ASSETS_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "assets")

def image_path(name: str):
    return os.path.join(ASSETS_ROOT, "images", name)

def font_path(name: str):
    return os.path.join(ASSETS_ROOT, "fonts", name)

def music_path(name: str):
    return os.path.join(ASSETS_ROOT, "sounds", "music", name)

def sfx_path(name: str):
    return os.path.join(ASSETS_ROOT, "sounds", "sfx", name)