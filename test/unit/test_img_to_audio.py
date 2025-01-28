import pytest
from unittest import mock

import synes


@pytest.fixture
def opened_image():
    """Mock opening an image file for reading."""
    opened_image = mock.MagicMock()
    opened_image.size = (1, 1)
    opened_image.mode = "L"
    return opened_image


@pytest.mark.parametrize(
    "image_path,output_param,output_path",
    [
        ("/path/image.png", None, "/path/image.wav"),
        ("/path/image.png", "/custom/output.wav", "/custom/output.wav"),
    ],
)
def test_output_path(opened_image, image_path, output_param, output_path):
    """Test output path."""
    with mock.patch("PIL.Image.open") as mock_image_open:
        mock_image_open.return_value.__enter__.return_value = opened_image
        opened_image.load.return_value.__getitem__.return_value = 0

        with mock.patch("wave.open"):
            returned_path = synes.translate_image(image_path, 44100, output_param)

    assert output_path == returned_path
    if output_param:
        assert output_param == returned_path


@pytest.mark.parametrize(
    "pix_value,pix_list",
    [
        (0, [0]),
        ((0, 1, 2), [0, 1, 2]),
    ],
)
def test_compile_pixels(opened_image, pix_value, pix_list):
    """Test compiling image pixels."""
    opened_wave = mock.MagicMock()

    with mock.patch("PIL.Image.open") as mock_image_open:
        mock_image_open.return_value.__enter__.return_value = opened_image
        opened_image.load.return_value.__getitem__.return_value = pix_value

        with mock.patch("wave.open") as mock_wave_open:
            mock_wave_open.return_value.__enter__.return_value = opened_wave

            synes.translate_image("/path/image.png", 44100)

    opened_wave.writeframes.assert_called_once_with(bytes(pix_list))


def test_compile_pixels_error(opened_image):
    """Test catching error when compiling image pixels."""
    with mock.patch("PIL.Image.open") as mock_image_open:
        mock_image_open.return_value.__enter__.return_value = opened_image
        opened_image.load.return_value.__getitem__.return_value = dict()

        with pytest.raises(RuntimeError) as exception_info:
            synes.translate_image("/path/image.png", 44100)

    exception_str = f"Unable to parse pixels, unrecognized pixel type '{dict}'."
    assert exception_str in str(exception_info)


def test_unsupported_image_mode():
    with mock.patch("PIL.Image.open") as mock_open_image:
        mock_open_image.return_value.__enter__.return_value.mode = "UNSUPPORTED"

        with pytest.raises(RuntimeError) as exception_info:
            synes.translate_image("/path/image.png", 44100)

    exception_str = "Unable to parse image format 'UNSUPPORTED'."
    assert exception_str in str(exception_info)
