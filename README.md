# synes

A python library to translate image files to audio and vice versa. Includes a command line interface that needs an input file and either an output width or output sample rate.

## Example Usage
Convert a .png file to a .wav file with a sample rate of 44100.

```synes 44100 resource/a4_image.png```

Convert a .wav file to a .png file with a width of 100.

```synes 100 resource/a4_audio.wav```

Optional output path argument.

```synes 44100 resource/a4.png -o ~/Desktop/synes_output.wav```
