# :coding: utf-8

import logging
import os.path
import wave

from PIL import Image

from synes.symbol import (
    IMAGE_MODE_TO_CHANNELS,
    DEFAULT_AUDIO_TYPE
)


def translate_image(img_path, sample_rate, output_path=None):
    """
    Write out a new audio file using the pixels from *img_path* as the 
    audio samples.

    :param img_path: input image file path
    :param sample_rate: sample rate for output audio file
    :param output_path: optional file path for output audio file

    """
    logger = logging.getLogger("image_to_audio")
    logger.setLevel(logging.INFO)

    # resolve audio output file path
    if output_path is None:
        img_dir, img_name = os.path.split(img_path)
        img_name = os.path.splitext(img_name)[0]
        output_path = os.path.join(
            img_dir, "{}.{}}".format(img_name, DEFAULT_AUDIO_TYPE)
        )

    # TODO check that output path has correct extension

    logger.info("Reading image file '{}'.".format(img_path))
    with Image.open(img_path) as img_in:
        try:
            num_channels = IMAGE_MODE_TO_CHANNELS[img_in.mode]
        except KeyError:
            raise RuntimeError(
                "Unable to parse image format '{}'.".format(img_in.mode)
            )

        width, height = img_in.size

        # TODO don't assume single bit
        bit_depth = 1

        pixels = img_in.load()

    logger.info("Compiling pixel data.")
    pix_list = []
    for y in range(height):
        for x in range(width):
            pix = pixels[x, y]
            if isinstance(pix, int):
                pix_list.append(pix)
            elif isinstance(pix, tuple):
                pix_list.extend(pix)
            else:
                raise RuntimeError(
                    "Unable to parse pixels, "
                    "unrecognized pixel type '{}'.".format(type(pix))
                )

    # TODO check if file already exists?

    duration = (width * height) / sample_rate

    logger.info(
        "Translating to audio file "
        "({} secs x {} hz).".format(duration, sample_rate)
    )
    with wave.open(output_path, "wb") as wave_out:
        wave_out.setnchannels(num_channels)
        wave_out.setsampwidth(bit_depth)
        wave_out.setframerate(sample_rate)

        wave_out.writeframes(bytes(pix_list))

    logger.info("Image translated successfully.")
