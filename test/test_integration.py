import filecmp
import os.path
import tempfile

import pytest

import synes

RESOURCE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.realpath(synes.__file__)
    ))),
    "resource"
)
RESOURCE_IMAGE = os.path.join(RESOURCE_PATH, "a4_image.png")
RESOURCE_WIDTH = 100
RESOURCE_WAVE = os.path.join(RESOURCE_PATH, "a4_audio.wav")
RESOURCE_SAMPLE_RATE = 44100


def test_img_to_audio_round_trip():
    """Test translating an image to audio and back to an image."""
    output_wave = os.path.join(tempfile.gettempdir(), "test_output.wav")
    try:
        synes.translate_image(
            RESOURCE_IMAGE, RESOURCE_SAMPLE_RATE, output_path=output_wave
        )
    except Exception as exc:
        assert False, "Image-to-audio translation failed.\n{}".format(exc)

    message = "Translated audio doesn't match resource wave file."
    assert filecmp.cmp(RESOURCE_WAVE, output_wave), message

    try:
        output_image = synes.translate_image(output_wave, RESOURCE_WIDTH)
    except Exception as exc:
        assert False, "Audio-to-image translation failed.\n{}".format(exc)

    message = "Translated image doesn't match original png file."
    assert filecmp.cmp(RESOURCE_IMAGE, output_image), message


def test_audio_to_img_round_trip():
    """Test translating audio to an image and back to audio."""
    output_image = os.path.join(tempfile.gettempdir(), "test_output.wav")
    try:
        synes.translate_audio(
            RESOURCE_WAVE, RESOURCE_WIDTH, output_path=output_image
        )
    except Exception as exc:
        assert False, "Audio-to-image translation failed.\n{}".format(exc)

    message = "Translated image doesn't match resource png file."
    assert filecmp.cmp(RESOURCE_IMAGE, output_image), message

    try:
        output_wave = synes.translate_image(output_image, RESOURCE_WIDTH)
    except Exception as exc:
        assert False, "Image-to-audio translation failed.\n{}".format(exc)

    message = "Translated audio doesn't match original wave file."
    assert filecmp.cmp(RESOURCE_IMAGE, output_wave), message
