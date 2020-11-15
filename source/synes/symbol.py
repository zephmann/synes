# :coding: utf-8

#: Default image file type
DEFAULT_IMAGE_TYPE = "png"

#: Default audio file type
DEFAULT_AUDIO_TYPE = "wav"

#: Image Mode to Number of Audio Channes Hash Map
IMAGE_MODE_TO_CHANNELS = {
    "L": 1,     # grayscale
    "LA": 2,    # grayscale + alpha
    "RGB": 3,   # rgb
    "RGBA": 4,  # rgb + alpha
}

#: Image Mode to Number of Audio Channes Hash Map
CHANNELS_TO_IMAGE_MODE = {
    1: "L",
    2: "RGB",  # use 50% for blue
    3: "RGB",
    4: "RGBA",
}
