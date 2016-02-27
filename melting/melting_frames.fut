fun [[[u32,3],width],height] imgify([[[u8,3],width],height] a) =
  reshape((height,width,3), map(%256u32, map(u32, reshape((height*width*3), a))))

fun u8 darken(u8 x) =
  u8(f32(x) * 0.95f32)

fun [[[[u32,3],width],height],frames] main(int frames, [[[u8,3],width],height] a) =
  let out = replicate(frames, replicate(height, replicate(width, replicate(3, 0u32)))) in
  loop ({a,out}) = for i < frames do
    let a = reshape((height,width,3), map(darken, reshape((3*width*height), a))) in
    let out[i] = imgify(a) in
    {a, out} in
  out
