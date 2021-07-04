import pytest

import synes


@pytest.fixture
def opened_image(mocker):
    """Mock opening an image file for reading."""
    opened_image = mocker.patch("PIL.Image.open")
    opened_image = opened_image.return_value.__enter__.return_value
    opened_image.size = (1, 1)
    opened_image.mode = "L"

    return opened_image


@pytest.mark.parametrize(
    "img_path,output_param,output_path",
    [
        ("/path/image.png", None, "/path/image.wav"),
        ("/path/image.png", "/custom/output.wav", "/custom/output.wav"),
    ]
)
def test_output_path(
    mocker, opened_image, img_path, output_param, output_path
):
    """Test output path."""
    # mock output for getter of img_in.load()
    opened_image.load.return_value.__getitem__.return_value = 0

    # mock wave.open context
    opened_wave = mocker.patch("wave.open")

    synes.translate_image(img_path, 44100, output_param)

    opened_wave.assert_called_once_with(output_path, "wb")


@pytest.mark.parametrize(
    "pix_value,pix_list",
    [
        (0, [0]),
        ((0, 1, 2), [0, 1, 2]),
    ]
)
def test_compile_pixels(mocker, opened_image, pix_value, pix_list):
    """Test compiling image pixels."""
    # mock output for getter of img_in.load()
    opened_image.load.return_value.__getitem__.return_value = pix_value

    # mock wave.open context object
    opened_wave = mocker.patch("wave.open").return_value.__enter__.return_value

    synes.translate_image("/path/image.png", 44100)

    opened_wave.writeframes.assert_called_once_with(bytes(pix_list))


def test_compile_pixels_error(opened_image):
    """Test catching error when compiling image pixels."""
    # mock output for getter of img_in.load()
    opened_image.load.return_value.__getitem__.return_value = dict()

    with pytest.raises(RuntimeError) as exception_info:
        synes.translate_image("/path/image.png", 44100)

    exception_str = (
        "Unable to parse pixels, unrecognized pixel type '{}'.".format(dict)
    )
    assert exception_str in str(exception_info)


def test_unsupported_image_mode(mocker):
    opened_image = mocker.patch("PIL.Image.open")
    opened_image = opened_image.return_value.__enter__.return_value
    opened_image.mode = "UNSUPPORTED"

    with pytest.raises(RuntimeError) as exception_info:
        synes.translate_image("/path/image.png", 44100)

    exception_str = "Unable to parse image format 'UNSUPPORTED'."
    assert exception_str in str(exception_info)
