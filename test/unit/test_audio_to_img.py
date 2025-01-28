import pytest
from unittest import mock

import synes


@pytest.mark.parametrize(
    "wav_path,output_param,output_path",
    [
        ("/path/audio.wav", None, "/path/audio.png"),
        ("/path/audio.wav", "/custom/output.png", "/custom/output.png"),
    ],
)
def test_output_path(wav_path, output_param, output_path):
    """Test output path."""
    opened_wave = mock.MagicMock()
    opened_wave.getnchannels.return_value = 1
    opened_wave.getnframes.return_value = 1
    opened_wave.readframes.return_value = [0]

    opened_image = mock.MagicMock()

    with mock.patch("wave.open") as mock_wave_open:
        mock_wave_open.return_value.__enter__.return_value = opened_wave
        with mock.patch("PIL.Image.new") as mock_image_open:
            mock_image_open.return_value.__enter__.return_value = opened_image
            returned_path = synes.translate_audio(wav_path, 44100, output_param)

    opened_image.save.assert_called_once_with(output_path)
    assert output_path == returned_path
    if output_param:
        assert output_param == returned_path


@pytest.mark.parametrize(
    "samples,num_channels,output_pixels",
    [
        ([0, 128, 255], 1, [0, 128, 255]),
        (
            [0, 128, 128, 255, 255, 0],
            2,
            [(0, 128, 128), (128, 255, 128), (255, 0, 128)],
        ),
        (
            [0, 128, 255, 128, 255, 0, 255, 0, 128],
            3,
            [(0, 128, 255), (128, 255, 0), (255, 0, 128)],
        ),
        (
            [0, 128, 255, 0, 128, 255, 0, 128, 255, 0, 128, 255],
            4,
            [(0, 128, 255, 0), (128, 255, 0, 128), (255, 0, 128, 255)],
        ),
    ],
)
def test_group_pixels(samples, num_channels, output_pixels):
    pixels = synes.audio_to_image._group_pixels(samples, num_channels, 1)
    assert pixels == output_pixels


def test_unsupported_num_channels():
    opened_wave = mock.MagicMock()
    opened_wave.getnchannels.return_value = -1

    with mock.patch("wave.open") as mock_wave_open:
        mock_wave_open.return_value.__enter__.return_value = opened_wave
        with pytest.raises(RuntimeError) as exception_info:
            synes.translate_audio("/path/image.wav", 100)

    exception_str = "Unable to resolve image mode for '-1' channels."
    assert exception_str in str(exception_info)
