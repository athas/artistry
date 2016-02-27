#!/usr/bin/env python

import png
import numpy
import sys
import melting_frames
import ctypes

i = 0

def write_image(d, w, h, i, pixels):
    f = open('%s/%d.png' % (d, i), 'wb')
    writer = png.Writer(w, h, greyscale=False, alpha=False, bitdepth=8)
    writer.write(f, numpy.reshape(pixels, (h, w*3)))

def main():
    reader = png.Reader(filename=sys.argv[1])
    (w,h,pixels,meta) = reader.asRGB8()
    pixels = numpy.reshape(numpy.array(list(pixels)), (h, w, 3))

    def write_frame(pixels):
        global i
        write_image('out', w, h, i, pixels)
        i = i + 1

    frames = melting_frames.main(10, pixels.astype(numpy.byte, copy=True))
    for frame in frames:
        write_frame(frame)

if __name__ == '__main__':
    main()