# :coding: utf-8

import logging
import os.path
import wave

from PIL import Image

from synes.constant import (
    IMAGE_MODE_TO_CHANNELS,
    DEFAULT_AUDIO_TYPE,
)

log = logging.getLogger()


def translate_image(image_path, sample_rate, output_path=None):
    """
    Write out a new audio file using the pixels from *image_path* as the
    audio samples.

    :param image_path: input image file path
    :param sample_rate: sample rate for output audio file
    :param output_path: optional file path for output audio file

    """
    # resolve audio output file path
    if output_path is None:
        image_dir, image_name = os.path.split(image_path)
        image_name = os.path.splitext(image_name)[0]
        output_path = os.path.join(image_dir, f"{image_name}.{DEFAULT_AUDIO_TYPE}")

    # TODO check that output path has correct extension

    log.info(f"Reading image file '{image_path}'.")
    with Image.open(image_path) as image_in:
        try:
            num_channels = IMAGE_MODE_TO_CHANNELS[image_in.mode]
        except KeyError:
            raise RuntimeError(f"Unable to parse image format '{image_in.mode}'.")

        width, height = image_in.size

        # TODO don't assume single bit
        bit_depth = 1

        pixels = image_in.load()

    # TODO better way to convert pixel samples into a list, maybe numpy
    log.info("Compiling pixel data.")
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
                    f"Unable to parse pixels, unrecognized pixel type '{type(pix)}'."
                )

    # TODO check if file already exists?

    duration = (width * height) / sample_rate

    log.info(f"Translating to audio file ({duration} secs x {sample_rate} hz).")
    with wave.open(output_path, "wb") as wave_out:
        wave_out.setnchannels(num_channels)
        wave_out.setsampwidth(bit_depth)
        wave_out.setframerate(sample_rate)

        wave_out.writeframes(bytes(pix_list))

    log.info("Image translated successfully.")

    return output_path
