fun [[[u32,3],width],height] imgify([[[u8,3],width],height] a) =
  reshape((height,width,3), map(%256u32, map(u32, reshape((height*width*3), a))))

fun [u8,3] frob([u8,3] p) =
  let r = p[0] in
  let g = p[1] in
  let b = p[2] in
  if r < 255u8 || g < 255u8 || b < 255u8
  then [u8(f32(r) * 0.97f32), u8(f32(g) * 0.98f32), u8(f32(b) * 0.99f32)]
  else [r, g, b]

fun u8 u8max(u8 x, u8 y) =
  if x < y then y else x

fun [u8,3] new_pixel([[[u8,3],width],height] a, int i, int j) =
  unsafe
  let rn = if i == 0 then 0u8 else a[i-1, j, 0] in
  let rs = if i == height-1 then 0u8 else a[i+1, j, 0] in
  let rw = if j == 0 then 0u8 else a[i, j-1, 0] in
  let re = if j == width-1 then 0u8 else a[i, j+1, 0] in
  let nextr = u8max(u8max(u8max(rn, rs), rw), re) in
  let r = a[i,j,0] in
  let g = a[i,j,1] in
  let b = a[i,j,2] in
  let r' = if r > nextr then r
                        else r + (nextr - r) / 2u8 in
  [r', g, b]

fun [[[[u32,3],width],height],frames] main(int frames, [[[u8,3],width],height] a) =
  let out = replicate(frames, replicate(height, replicate(width, replicate(3, 0u32)))) in
  loop ({a,out}) = for i < frames do
    let a = map(fn [[u8,3],width] (int i) =>
                  map(new_pixel(a, i), iota(width)),
                iota(height)) in
    let out[i] = imgify(a) in
    {a, out} in
  out
