# :coding: utf-8

import logging
import math
import os.path
import wave

from PIL import Image

from synes.constant import CHANNELS_TO_IMAGE_MODE, DEFAULT_IMAGE_TYPE

log = logging.getLogger()


def translate_audio(audio_path, width, output_path=None):
    """
    Write out a new image file using the samples from *audio_path* as the
    image pixels.

    :param audio_path: input audio file path
    :param width: width in pixels for output image file
    :param output_path: optional file path for output image file

    """
    if output_path is None:
        audio_dir, audio_name = os.path.split(audio_path)
        audio_name = os.path.splitext(audio_name)[0]
        output_path = os.path.join(audio_dir, f"{audio_name}.{DEFAULT_IMAGE_TYPE}")

    # TODO check that output path has correct extension

    log.info(f"Reading audio from file '{audio_path}'")
    with wave.open(audio_path, "rb") as audio_in:
        num_channels = audio_in.getnchannels()

        try:
            image_mode = CHANNELS_TO_IMAGE_MODE[num_channels]
        except KeyError:
            raise RuntimeError(
                f"Unable to resolve image mode for '{audio_in.getnchannels()}' channels."
            )

        num_samples = audio_in.getnframes()

        # TODO don't assume single bit
        # bit_depth = 1

        height = math.ceil(num_samples / width)

        # TODO ensure size matches input width x height

        log.info("Loading audio samples.")

        samples = audio_in.readframes(num_samples)

    pixels = _group_pixels(samples, num_channels, num_samples)

    # TODO check if file already exists?

    log.info("Writing image file.")
    with Image.new(image_mode, (width, height)) as image_out:
        image_out.putdata(pixels)
        image_out.save(output_path)

    log.info("Image translated successfully.")

    return output_path


def _group_pixels(samples, num_channels, num_samples):
    if num_channels == 1:
        return samples

    # if only 2 channels, use 128 for blue
    if num_channels == 2:

        def _blue():
            while True:
                yield 128

        p = iter(samples)
        b = iter(_blue())
        return list(zip(p, p, b))

    return list(zip(*[iter(samples)] * num_channels))
