Mangle farbfeld[1] images
=========================

This directory contains a Futhark program that can mangle Farbfeld
images in various ways.  You can compile the Futhark program as such:

    futhark-c ffmangle.fut

You'll also need to compile two small utility programs:

    gcc bytes2fut.c -o bytes2fut
    gcc fut2bytes.c -o fut2bytes

And then use it to transform a PNG image as such (requires the farbfeld tools):

    cat troels.png | png2ff | ./bytes2fut | ./ffmangle | ./fut2bytes | ff2png > troels-out.png

The specific mangling used is controlled by a constant in `ffmangle.fut`.

[1]: http://tools.suckless.org/farbfeld/
