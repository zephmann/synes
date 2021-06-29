import pytest

import synes


@pytest.mark.parametrize(
    "wav_path,output_param,output_path",
    [
        ("/path/audio.wav", None, "/path/audio.png"),
        ("/path/audio.wav", "/custom/output.png", "/custom/output.png"),
    ]
)
def test_output_path(
    mocker, wav_path, output_param, output_path
):
    """Test output path."""
    opened_wave = mocker.patch("wave.open").return_value.__enter__.return_value
    opened_wave.getnchannels.return_value = 1
    opened_wave.getnframes.return_value = 1
    opened_wave.readframes.return_value = [0]

    # mock output for getter of img_in.load()
    opened_image = mocker.patch("PIL.Image.new")
    opened_image = opened_image.return_value.__enter__.return_value

    synes.translate_audio(wav_path, 44100, output_param)

    opened_image.save.assert_called_once_with(output_path)

# TODO add test for _group_pixels

# TODO test unsupported number of channels
