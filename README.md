# synes

A python library to translate image files to audio and vice versa. Includes a command line interface that needs an input file and either an output width or output sample rate.

## Examples
Convert a .png file to a .wav file with a sample rate of 44100.

```synes 44100 ~/Desktop/a4_gradient.png```

Convert a .wav file to a .png file with a width of 100.

```synes 100 ~/Desktop/a4_test.wav```

Optional output path argument.

```synes 44100 ~/Desktop/a4_gradient.png -o ~/Desktop/output_file.wav```
