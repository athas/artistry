fun [[[u32,3],width],height] imgify([[[u8,3],width],height] a) =
  reshape((height,width,3), map(%256u32, map(u32, reshape((height*width*3), a))))

fun [u8,3] frob([u8,3] p) =
  let r = p[0] in
  let g = p[1] in
  let b = p[2] in
  if r < 255u8 || g < 255u8 || b < 255u8
  then [u8(f32(r) * 0.97f32), u8(f32(g) * 0.98f32), u8(f32(b) * 0.99f32)]
  else [r, g, b]

fun [u8,3] new_pixel([[[u8,3],width],height] a, int i, int j) =
  unsafe
  if i == height / 2 || j == width / 2 then [255u8,255u8,255u8] else
  if i < height / 2
  then if j < width / 2
       then a[i+1,j+1]
       else a[i+1,j-1]
  else if j < width / 2
       then a[i-1,j+1]
       else a[i-1,j-1]

fun [[[[u32,3],width],height],frames] main(int frames, [[[u8,3],width],height] a) =
  let out = replicate(frames, replicate(height, replicate(width, replicate(3, 0u32)))) in
  loop ({a,out}) = for i < frames do
    let a = map(fn [[u8,3],width] (int i) =>
                  map(frob,map(new_pixel(a, i), iota(width))),
                iota(height)) in
    let out[i] = imgify(a) in
    {a, out} in
  out
