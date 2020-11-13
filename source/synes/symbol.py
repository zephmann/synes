# :coding: utf-8

#: Image Mode to Number of Audio Channes Hash Map
IMAGE_MODE_TO_CHANNELS = {
    "L": 1,     # grayscale
    "LA": 2,    # grayscale + alpha
    "RGB": 3,   # rgb
    "RGBA": 4,  # rgb + alpha
}

#: Image Mode to Number of Audio Channes Hash Map
CHANNELS_TO_IMAGE_MODE = {
    channels: img_mode for img_mode, channels in IMAGE_MODE_TO_CHANNELS.items()
}
