# :coding: utf-8

import logging
import os.path
import wave

from PIL import Image

from synes.symbol import CHANNELS_TO_IMAGE_MODE


def translate_wave(wave_path, height):
    logger = logging.getLogger("audio_to_image")
    logger.setLevel(logging.INFO)

    logger.info("Reading audio from file '{}'".format(wave_path_path))
    with wave.open(wave_path, "rd") as wave_in:
        try:
            image_mode = CHANNELS_TO_IMAGE_MODE[wave_in.getnchannels()]
        except KeyError:
            raise RuntimeError(
                "Unable to resolve image mode for "
                "'{}' channels.".format(wave_in.getnchannels())
            )

        num_samples = wave_in.getnframes()

        # TODO don't assume single bit
        bit_depth = 1

    width = ceil(num_samples / height)
    
    logger.info("Loading audio samples.")
    samples = wave_in.readframes(num_samples)

    # TODO ensure size matches input width x height

    # resolve image output file path
    wave_dir, wave_name = os.path.split(wave_path)
    wave_name = os.path.splitext(wave_name)[0]
    img_path = os.path.join(wave_dir, "{}.png".format(wave_name))

    # TODO check if file already exists?

    logger.info("Writing image file.")
    with Image.new(image_mode, (width, height)) as img_out:
        img_out.putdata(samples)
        img_out.save(img_path)

    logger.info("Image translated successfully.")
