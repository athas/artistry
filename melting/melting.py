#!/usr/bin/env python

import png
import numpy
import sys
import melting_frames
import ctypes
import time

i = 0
outdir='out'

def main():
    reader = png.Reader(filename=sys.argv[1])
    (w,h,pixels,meta) = reader.asRGB8()
    pixels = numpy.reshape(numpy.array(list(pixels), dtype=numpy.byte), (h, w, 3))

    def write_frame(pixels):
        global i
        pixels.astype(dtype=numpy.byte, copy=True).tofile('%s/%d.rgb' % (outdir, i))
        i = i + 1

    frames_remaining = 1000
    chunksize = 100
    while frames_remaining > 0:
        render = min(frames_remaining, chunksize)
        time_start = time.time()
        frames = melting_frames.main(render, pixels)
        time_end = time.time()
        print('Generated %d frames in %dms' % (render, (time_end-time_start)*1000))
        for frame in frames:
            time_start = time.time()
            write_frame(frame)
            time_end = time.time()
            print('Wrote frame to disk in %dms' % ((time_end-time_start)*1000,))
        frames_remaining = max(0, frames_remaining - chunksize)
        pixels=frames[render-1].astype(dtype=numpy.byte, copy=True)
    print('width: %d, height: %d' % (w, h))

if __name__ == '__main__':
    main()
