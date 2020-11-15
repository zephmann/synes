# :coding: utf-8

import os.path

import click

import synes


@click.command()
@click.argument("width", type=int)
@click.argument("input_path", type=click.Path(exists=True))
@click.option("-o", "--output_path", type=click.Path())
def main(input_path, width, output_path):
    ext = os.path.splitext(input_path)[1]
    if ext in (".png", ".jpg"):
        synes.translate_image(input_path, width, output_path)
    
    elif ext == ".wav":
        synes.translate_audio(input_path, width, output_path)

    else:
        raise RuntimeError(
            "Unable to translate file, unknown file type '{}'".format(ext)
        )
