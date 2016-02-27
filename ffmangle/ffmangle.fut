-- Mangle a Farbfeld image.

fun u32 u32be(u8 a, u8 b, u8 c, u8 d) =
  u32(a) << 24u32 | u32(b) << 16u32 | u32(c) << 8u32 | u32(d)

fun u16 u16be(u8 a, u8 b) =
  u16(a) << 8u16 | u16(b)

fun [[[u8,8],width],height] to_ff_bytes([[[u16,4],width],height] data) =
  reshape((height, width, 8),
          map(fn [u8,2] (u16 x) =>
                [u8(x>>8u16), u8(x)],
              reshape((height * width * 4), data)))

fun [[[u16,4],width],height] from_ff_bytes([[[u8,8],width],height] data) =
  reshape((height, width, 4),
          map(fn u16 ([u8] bytes) =>
                u16be(bytes[0], bytes[1]),
              reshape((height * width * 4, 2), data)))

fun u32 u32max(u32 x, u32 y) =
  if x < y then y else x

fun u32 u32min(u32 x, u32 y) =
  if x < y then x else y

fun [u16,4] desaturate_pixel([u16,4] pixel) =
  let r = pixel[0] in
  let g = pixel[1] in
  let b = pixel[2] in
  let a = pixel[3] in
  let x = r//u16(3) + g//u16(3) + b//u16(3) in
  [x, x, x, a]

fun [[[u16,4],width],height] transform([[[u16,4],width],height] pixels) =
  -- The variable f determines how we mangle the image.
  let f = 1 in
  if f == 0 -- Desaturate
  then
    reshape((width, height, 4),
            map(desaturate_pixel,
                reshape((width*height, 4), pixels)))
  else if f == 1 then -- Fuck around with the columns.
    map(fn [[u16,4],height] ([[u16]] row) =>
          let channels = transpose(row) in
          transpose([map(u16, scan(u32max, 0u32, map(u32, channels[0]))),
                     map(u16, scan(u32max, 0u32, map(u32, channels[1]))),
                     map(u16, scan(u32max, 0u32, map(u32, channels[2]))),
                     channels[3]]),
        pixels)
  else
    pixels

fun [u8] main([u8] img) =
  let {header_bytes, width_bytes, height_bytes, img_bytes} =
    split((8, 12, 16), img) in
  let width =
    u32be(width_bytes[0], width_bytes[1], width_bytes[2], width_bytes[3]) in
  let height =
    u32be(height_bytes[0], height_bytes[1], height_bytes[2], height_bytes[3]) in
  concat(header_bytes, width_bytes, height_bytes,
         reshape((i32(height*width) * 8),
                 to_ff_bytes(
                   transform(
                     from_ff_bytes(
                       reshape((i32(height), i32(width), 8),
                               img_bytes))))))
