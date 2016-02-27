import sys
from numpy import *
from ctypes import *
import pyopencl as cl
import time
import argparse
FUT_BLOCK_DIM = 16
ctx=0
program=0
queue=0
synchronous=False

def signed(x):
  if type(x) == uint8:
    return int8(x)
  elif type(x) == uint16:
    return int16(x)
  elif type(x) == uint32:
    return int32(x)
  else:
    return int64(x)

def unsigned(x):
  if type(x) == int8:
    return uint8(x)
  elif type(x) == int16:
    return uint16(x)
  elif type(x) == int32:
    return uint32(x)
  else:
    return uint64(x)

def shlN(x,y):
  return x << y

def ashrN(x,y):
  return x >> y

def sdivN(x,y):
  return x / y

def smodN(x,y):
  return x % y

def udivN(x,y):
  return signed(unsigned(x) / unsigned(y))

def umodN(x,y):
  return signed(unsigned(x) % unsigned(y))

def squotN(x,y):
  return int32(float(x) / float(y))

def sremN(x,y):
  return fmod(x,y)

def powN(x,y):
  return x ** y

def fpowN(x,y):
  return x ** y

def sleN(x,y):
  return x <= y

def sltN(x,y):
  return x < y

def uleN(x,y):
  return unsigned(x) <= unsigned(y)

def ultN(x,y):
  return unsigned(x) < unsigned(y)

def lshr8(x,y):
  return int8(uint8(x) >> uint8(y))

def lshr16(x,y):
  return int16(uint16(x) >> uint16(y))

def lshr32(x,y):
  return int32(uint32(x) >> uint32(y))

def lshr64(x,y):
  return int64(uint64(x) >> uint64(y))

def sext_T_i8(x):
  return int8(x)

def sext_T_i16(x):
  return int16(x)

def sext_T_i32(x):
  return int32(x)

def sext_T_i64(x):
  return int32(x)

def zext_i8_i8(x):
  return int8(uint8(x))

def zext_i8_i16(x):
  return int16(uint8(x))

def zext_i8_i32(x):
  return int32(uint8(x))

def zext_i8_i64(x):
  return int64(uint8(x))

def zext_i16_i8(x):
  return int8(uint16(x))

def zext_i16_i16(x):
  return int16(uint16(x))

def zext_i16_i32(x):
  return int32(uint16(x))

def zext_i16_i64(x):
  return int64(uint16(x))

def zext_i32_i8(x):
  return int8(uint32(x))

def zext_i32_i16(x):
  return int16(uint32(x))

def zext_i32_i32(x):
  return int32(uint32(x))

def zext_i32_i64(x):
  return int64(uint32(x))

def zext_i64_i8(x):
  return int8(uint64(x))

def zext_i64_i16(x):
  return int16(uint64(x))

def zext_i64_i32(x):
  return int32(uint64(x))

def zext_i64_i64(x):
  return int64(uint64(x))

shl8 = shl16 = shl32 = shl64 = shlN
ashr8 = ashr16 = ashr32 = ashr64 = ashrN
sdiv8 = sdiv16 = sdiv32 = sdiv64 = sdivN
smod8 = smod16 = smod32 = smod64 = smodN
udiv8 = udiv16 = udiv32 = udiv64 = udivN
umod8 = umod16 = umod32 = umod64 = umodN
squot8 = squot16 = squot32 = squot64 = squotN
srem8 = srem16 = srem32 = srem64 = sremN
pow8 = pow16 = pow32 = pow64 = powN
fpow32 = fpow64 = fpowN
sle8 = sle16 = sle32 = sle64 = sleN
slt8 = slt16 = slt32 = slt64 = sltN
ule8 = ule16 = ule32 = ule64 = uleN
ult8 = ult16 = ult32 = ult64 = ultN
sext_i8_i8 = sext_i16_i8 = sext_i32_i8 = sext_i64_i8 = sext_T_i8
sext_i8_i16 = sext_i16_i16 = sext_i32_i16 = sext_i64_i16 = sext_T_i16
sext_i8_i32 = sext_i16_i32 = sext_i32_i32 = sext_i64_i32 = sext_T_i32
sext_i8_i64 = sext_i16_i64 = sext_i32_i64 = sext_i64_i64 = sext_T_i64

def ssignum(x):
  return sign(x)

def usignum(x):
  if x < 0:
    return ssignum(-x)
  else:
    return ssignum(x)

def sitofp_T_f32(x):
  return float32(x)
sitofp_i8_f32 = sitofp_i16_f32 = sitofp_i32_f32 = sitofp_i64_f32 = sitofp_T_f32

def sitofp_T_f64(x):
  return float64(x)
sitofp_i8_f64 = sitofp_i16_f64 = sitofp_i32_f64 = sitofp_i64_f64 = sitofp_T_f64

def uitofp_T_f32(x):
  return float32(unsigned(x))
uitofp_i8_f32 = uitofp_i16_f32 = uitofp_i32_f32 = uitofp_i64_f32 = uitofp_T_f32

def uitofp_T_f64(x):
  return float64(unsigned(x))
uitofp_i8_f64 = uitofp_i16_f64 = uitofp_i32_f64 = uitofp_i64_f64 = uitofp_T_f64

def fptosi_T_i8(x):
  return int8(trunc(x))
fptosi_f32_i8 = fptosi_f64_i8 = fptosi_T_i8

def fptosi_T_i16(x):
  return int16(trunc(x))
fptosi_f32_i16 = fptosi_f64_i16 = fptosi_T_i16

def fptosi_T_i32(x):
  return int32(trunc(x))
fptosi_f32_i32 = fptosi_f64_i32 = fptosi_T_i32

def fptosi_T_i64(x):
  return int64(trunc(x))
fptosi_f32_i64 = fptosi_f64_i64 = fptosi_T_i64

def fptoui_T_i8(x):
  return uint8(trunc(x))
fptoui_f32_i8 = fptoui_f64_i8 = fptoui_T_i8

def fptoui_T_i16(x):
  return uint16(trunc(x))
fptoui_f32_i16 = fptoui_f64_i16 = fptoui_T_i16

def fptoui_T_i32(x):
  return uint32(trunc(x))
fptoui_f32_i32 = fptoui_f64_i32 = fptoui_T_i32

def fptoui_T_i64(x):
  return uint64(trunc(x))
fptoui_f32_i64 = fptoui_f64_i64 = fptoui_T_i64

def fpconv_f32_f64(x):
  return float64(x)

def fpconv_f64_f32(x):
  return float32(x)

def futhark_log64(x):
  return float64(log(x))

def futhark_sqrt64(x):
  return sqrt(x)

def futhark_exp64(x):
  return exp(x)

def futhark_cos64(x):
  return cos(x)

def futhark_sin64(x):
  return sin(x)

def futhark_log32(x):
  return float32(log(x))

def futhark_sqrt32(x):
  return float32(sqrt(x))

def futhark_exp32(x):
  return exp(x)

def futhark_cos32(x):
  return cos(x)

def futhark_sin32(x):
  return sin(x)


lookahead_buffer = []

def reset_lookahead():
    global lookahead_buffer
    lookahead_buffer = []

def get_char(f):
    global lookahead_buffer
    if len(lookahead_buffer) == 0:
        return f.read(1)
    else:
        c = lookahead_buffer[0]
        lookahead_buffer = lookahead_buffer[1:]
        return c

def unget_char(f, c):
    global lookahead_buffer
    lookahead_buffer = [c] + lookahead_buffer

def peek_char(f):
    c = get_char(f)
    if c:
        unget_char(f, c)
    return c

def skip_spaces(f):
    c = get_char(f)
    while c != None:
        if c.isspace():
            c = get_char(f)
        elif c == '-':
          # May be line comment.
          if peek_char(f) == '-':
            # Yes, line comment. Skip to end of line.
            while (c != '\n' and c != None):
              c = get_char(f)
          else:
            break
        else:
          break
    if c:
        unget_char(f, c)

def parse_specific_char(f, expected):
    got = get_char(f)
    if got != expected:
        unget_char(f, got)
        raise ValueError
    return True

def parse_specific_string(f, s):
    for c in s:
        parse_specific_char(f, c)
    return True

def optional(p, *args):
    try:
        return p(*args)
    except ValueError:
        return None

def sepBy(p, sep, *args):
    elems = []
    x = optional(p, *args)
    if x != None:
        elems += [x]
        while optional(sep, *args) != None:
            x = p(*args)
            elems += [x]
    return elems

def parse_int(f):
    s = ''
    c = get_char(f)
    while c != None:
        if c.isdigit():
            s += c
            c = get_char(f)
        else:
            unget_char(f, c)
            break
    optional(read_int_trailer, f)
    return s

def parse_int_signed(f):
    s = ''
    c = get_char(f)

    if c == '-' and peek_char(f).isdigit():
      s = c + parse_int(f)
    else:
      unget_char(f, c)
      s = parse_int(f)

    return s

def read_int_trailer(f):
  parse_specific_char(f, 'i')
  while peek_char(f).isdigit():
    get_char(f)

def read_comma(f):
    skip_spaces(f)
    parse_specific_char(f, ',')
    return ','

def read_int(f):
    skip_spaces(f)
    return int(parse_int_signed(f))

def read_char(f):
    skip_spaces(f)
    parse_specific_char(f, '\'')
    c = get_char(f)
    parse_specific_char(f, '\'')
    return c

def read_double(f):
    skip_spaces(f)
    c = get_char(f)
    if (c == '-'):
      sign = '-'
    else:
      unget_char(f,c)
      sign = ''
    bef = optional(parse_int, f)
    if bef == None:
        bef = '0'
        parse_specific_char(f, '.')
        aft = parse_int(f)
    elif optional(parse_specific_char, f, '.'):
        aft = parse_int(f)
    else:
        aft = '0'
    if (optional(parse_specific_char, f, 'E') or
        optional(parse_specific_char, f, 'e')):
        expt = parse_int_signed(f)
    else:
        expt = '0'
    optional(read_float_trailer, f)
    return float(sign + bef + '.' + aft + 'E' + expt)

def read_float(f):
    return read_double(f)

def read_float_trailer(f):
  parse_specific_char(f, 'f')
  while peek_char(f).isdigit():
    get_char(f)

def read_bool(f):
    skip_spaces(f)
    if peek_char(f) == 'T':
        parse_specific_string(f, 'True')
        return True
    elif peek_char(f) == 'F':
        parse_specific_string(f, 'False')
        return False
    else:
        raise ValueError

def read_array_elems(f, elem_reader):
    skip_spaces(f)
    parse_specific_char(f, '[')
    xs = sepBy(elem_reader, read_comma, f)
    skip_spaces(f)
    parse_specific_char(f, ']')
    return xs

def read_array_helper(f, elem_reader, rank):
    def nested_row_reader(_):
        return read_array_helper(f, elem_reader, rank-1)
    if rank == 1:
        row_reader = elem_reader
    else:
        row_reader = nested_row_reader
    return read_array_elems(f, row_reader)

def expected_array_dims(l, rank):
  if rank > 1:
      n = len(l)
      if n == 0:
          elem = []
      else:
          elem = l[0]
      return [n] + expected_array_dims(elem, rank-1)
  else:
      return [len(l)]

def verify_array_dims(l, dims):
    if dims[0] != len(l):
        raise ValueError
    if len(dims) > 1:
        for x in l:
            verify_array_dims(x, dims[1:])

def read_double_signed(f):

    skip_spaces(f)
    c = get_char(f)

    if c == '-' and peek_char(f).isdigit():
      v = -1 * read_double(f)
    else:
      unget_char(f, c)
      v = read_double(f)

    return v

def read_array(f, elem_reader, rank, bt):
    elems = read_array_helper(f, elem_reader, rank)
    dims = expected_array_dims(elems, rank)
    verify_array_dims(elems, dims)
    return array(elems, dtype=bt)

def write_chars(f, arr):
    f.write("\"")
    for x in arr:
      f.write(x.decode())
    f.write("\"")

def write_array(f, arr, bt):
    if arr.size == 0:
        print("empty({})".format(bt))
    else:
        print(arr.tolist())

fut_opencl_src = """
typedef char int8_t;
typedef short int16_t;
typedef int int32_t;
typedef long int64_t;
typedef uchar uint8_t;
typedef ushort uint16_t;
typedef uint uint32_t;
typedef ulong uint64_t;
static inline int8_t add8 (int8_t x, int8_t y)
{
    return x + y;
}
static inline int16_t add16 (int16_t x, int16_t y)
{
    return x + y;
}
static inline int32_t add32 (int32_t x, int32_t y)
{
    return x + y;
}
static inline int64_t add64 (int64_t x, int64_t y)
{
    return x + y;
}
static inline int8_t sub8 (int8_t x, int8_t y)
{
    return x - y;
}
static inline int16_t sub16 (int16_t x, int16_t y)
{
    return x - y;
}
static inline int32_t sub32 (int32_t x, int32_t y)
{
    return x - y;
}
static inline int64_t sub64 (int64_t x, int64_t y)
{
    return x - y;
}
static inline int8_t mul8 (int8_t x, int8_t y)
{
    return x * y;
}
static inline int16_t mul16 (int16_t x, int16_t y)
{
    return x * y;
}
static inline int32_t mul32 (int32_t x, int32_t y)
{
    return x * y;
}
static inline int64_t mul64 (int64_t x, int64_t y)
{
    return x * y;
}
static inline uint8_t udiv8 (uint8_t x, uint8_t y)
{
    return x / y;
}
static inline uint16_t udiv16 (uint16_t x, uint16_t y)
{
    return x / y;
}
static inline uint32_t udiv32 (uint32_t x, uint32_t y)
{
    return x / y;
}
static inline uint64_t udiv64 (uint64_t x, uint64_t y)
{
    return x / y;
}
static inline uint8_t umod8 (uint8_t x, uint8_t y)
{
    return x % y;
}
static inline uint16_t umod16 (uint16_t x, uint16_t y)
{
    return x % y;
}
static inline uint32_t umod32 (uint32_t x, uint32_t y)
{
    return x % y;
}
static inline uint64_t umod64 (uint64_t x, uint64_t y)
{
    return x % y;
}
static inline int8_t sdiv8 (int8_t x, int8_t y)
{
    int8_t q = x / y;
    int8_t r = x % y;
    
    return q - (r != 0 && r < 0 != y < 0 ? 1 : 0);
}
static inline int16_t sdiv16 (int16_t x, int16_t y)
{
    int16_t q = x / y;
    int16_t r = x % y;
    
    return q - (r != 0 && r < 0 != y < 0 ? 1 : 0);
}
static inline int32_t sdiv32 (int32_t x, int32_t y)
{
    int32_t q = x / y;
    int32_t r = x % y;
    
    return q - (r != 0 && r < 0 != y < 0 ? 1 : 0);
}
static inline int64_t sdiv64 (int64_t x, int64_t y)
{
    int64_t q = x / y;
    int64_t r = x % y;
    
    return q - (r != 0 && r < 0 != y < 0 ? 1 : 0);
}
static inline int8_t smod8 (int8_t x, int8_t y)
{
    int8_t r = x % y;
    
    return r + (r == 0 || x > 0 && y > 0 || x < 0 && y < 0 ? 0 : y);
}
static inline int16_t smod16 (int16_t x, int16_t y)
{
    int16_t r = x % y;
    
    return r + (r == 0 || x > 0 && y > 0 || x < 0 && y < 0 ? 0 : y);
}
static inline int32_t smod32 (int32_t x, int32_t y)
{
    int32_t r = x % y;
    
    return r + (r == 0 || x > 0 && y > 0 || x < 0 && y < 0 ? 0 : y);
}
static inline int64_t smod64 (int64_t x, int64_t y)
{
    int64_t r = x % y;
    
    return r + (r == 0 || x > 0 && y > 0 || x < 0 && y < 0 ? 0 : y);
}
static inline int8_t squot8 (int8_t x, int8_t y)
{
    return x / y;
}
static inline int16_t squot16 (int16_t x, int16_t y)
{
    return x / y;
}
static inline int32_t squot32 (int32_t x, int32_t y)
{
    return x / y;
}
static inline int64_t squot64 (int64_t x, int64_t y)
{
    return x / y;
}
static inline int8_t srem8 (int8_t x, int8_t y)
{
    return x % y;
}
static inline int16_t srem16 (int16_t x, int16_t y)
{
    return x % y;
}
static inline int32_t srem32 (int32_t x, int32_t y)
{
    return x % y;
}
static inline int64_t srem64 (int64_t x, int64_t y)
{
    return x % y;
}
static inline uint8_t shl8 (uint8_t x, uint8_t y)
{
    return x << y;
}
static inline uint16_t shl16 (uint16_t x, uint16_t y)
{
    return x << y;
}
static inline uint32_t shl32 (uint32_t x, uint32_t y)
{
    return x << y;
}
static inline uint64_t shl64 (uint64_t x, uint64_t y)
{
    return x << y;
}
static inline uint8_t lshr8 (uint8_t x, uint8_t y)
{
    return x >> y;
}
static inline uint16_t lshr16 (uint16_t x, uint16_t y)
{
    return x >> y;
}
static inline uint32_t lshr32 (uint32_t x, uint32_t y)
{
    return x >> y;
}
static inline uint64_t lshr64 (uint64_t x, uint64_t y)
{
    return x >> y;
}
static inline int8_t ashr8 (int8_t x, int8_t y)
{
    return x >> y;
}
static inline int16_t ashr16 (int16_t x, int16_t y)
{
    return x >> y;
}
static inline int32_t ashr32 (int32_t x, int32_t y)
{
    return x >> y;
}
static inline int64_t ashr64 (int64_t x, int64_t y)
{
    return x >> y;
}
static inline uint8_t and8 (uint8_t x, uint8_t y)
{
    return x & y;
}
static inline uint16_t and16 (uint16_t x, uint16_t y)
{
    return x & y;
}
static inline uint32_t and32 (uint32_t x, uint32_t y)
{
    return x & y;
}
static inline uint64_t and64 (uint64_t x, uint64_t y)
{
    return x & y;
}
static inline uint8_t or8 (uint8_t x, uint8_t y)
{
    return x | y;
}
static inline uint16_t or16 (uint16_t x, uint16_t y)
{
    return x | y;
}
static inline uint32_t or32 (uint32_t x, uint32_t y)
{
    return x | y;
}
static inline uint64_t or64 (uint64_t x, uint64_t y)
{
    return x | y;
}
static inline uint8_t xor8 (uint8_t x, uint8_t y)
{
    return x ^ y;
}
static inline uint16_t xor16 (uint16_t x, uint16_t y)
{
    return x ^ y;
}
static inline uint32_t xor32 (uint32_t x, uint32_t y)
{
    return x ^ y;
}
static inline uint64_t xor64 (uint64_t x, uint64_t y)
{
    return x ^ y;
}
static inline char ult8 (uint8_t x, uint8_t y)
{
    return x < y;
}
static inline char ult16 (uint16_t x, uint16_t y)
{
    return x < y;
}
static inline char ult32 (uint32_t x, uint32_t y)
{
    return x < y;
}
static inline char ult64 (uint64_t x, uint64_t y)
{
    return x < y;
}
static inline char ule8 (uint8_t x, uint8_t y)
{
    return x <= y;
}
static inline char ule16 (uint16_t x, uint16_t y)
{
    return x <= y;
}
static inline char ule32 (uint32_t x, uint32_t y)
{
    return x <= y;
}
static inline char ule64 (uint64_t x, uint64_t y)
{
    return x <= y;
}
static inline char slt8 (int8_t x, int8_t y)
{
    return x < y;
}
static inline char slt16 (int16_t x, int16_t y)
{
    return x < y;
}
static inline char slt32 (int32_t x, int32_t y)
{
    return x < y;
}
static inline char slt64 (int64_t x, int64_t y)
{
    return x < y;
}
static inline char sle8 (int8_t x, int8_t y)
{
    return x <= y;
}
static inline char sle16 (int16_t x, int16_t y)
{
    return x <= y;
}
static inline char sle32 (int32_t x, int32_t y)
{
    return x <= y;
}
static inline char sle64 (int64_t x, int64_t y)
{
    return x <= y;
}
static inline int8_t pow8 (int8_t x, int8_t y)
{
    int8_t res = 1, rem = y;
    
    while (rem != 0) {
        if (rem & 1) {
            res *= x;
        }
        rem >>= 1;
        x *= x;
    }
    return res;
}
static inline int16_t pow16 (int16_t x, int16_t y)
{
    int16_t res = 1, rem = y;
    
    while (rem != 0) {
        if (rem & 1) {
            res *= x;
        }
        rem >>= 1;
        x *= x;
    }
    return res;
}
static inline int32_t pow32 (int32_t x, int32_t y)
{
    int32_t res = 1, rem = y;
    
    while (rem != 0) {
        if (rem & 1) {
            res *= x;
        }
        rem >>= 1;
        x *= x;
    }
    return res;
}
static inline int64_t pow64 (int64_t x, int64_t y)
{
    int64_t res = 1, rem = y;
    
    while (rem != 0) {
        if (rem & 1) {
            res *= x;
        }
        rem >>= 1;
        x *= x;
    }
    return res;
}
static inline int8_t sext_i8_i8 (int8_t x)
{
    return x;
}
static inline int16_t sext_i8_i16 (int8_t x)
{
    return x;
}
static inline int32_t sext_i8_i32 (int8_t x)
{
    return x;
}
static inline int64_t sext_i8_i64 (int8_t x)
{
    return x;
}
static inline int8_t sext_i16_i8 (int16_t x)
{
    return x;
}
static inline int16_t sext_i16_i16 (int16_t x)
{
    return x;
}
static inline int32_t sext_i16_i32 (int16_t x)
{
    return x;
}
static inline int64_t sext_i16_i64 (int16_t x)
{
    return x;
}
static inline int8_t sext_i32_i8 (int32_t x)
{
    return x;
}
static inline int16_t sext_i32_i16 (int32_t x)
{
    return x;
}
static inline int32_t sext_i32_i32 (int32_t x)
{
    return x;
}
static inline int64_t sext_i32_i64 (int32_t x)
{
    return x;
}
static inline int8_t sext_i64_i8 (int64_t x)
{
    return x;
}
static inline int16_t sext_i64_i16 (int64_t x)
{
    return x;
}
static inline int32_t sext_i64_i32 (int64_t x)
{
    return x;
}
static inline int64_t sext_i64_i64 (int64_t x)
{
    return x;
}
static inline uint8_t zext_i8_i8 (uint8_t x)
{
    return x;
}
static inline uint16_t zext_i8_i16 (uint8_t x)
{
    return x;
}
static inline uint32_t zext_i8_i32 (uint8_t x)
{
    return x;
}
static inline uint64_t zext_i8_i64 (uint8_t x)
{
    return x;
}
static inline uint8_t zext_i16_i8 (uint16_t x)
{
    return x;
}
static inline uint16_t zext_i16_i16 (uint16_t x)
{
    return x;
}
static inline uint32_t zext_i16_i32 (uint16_t x)
{
    return x;
}
static inline uint64_t zext_i16_i64 (uint16_t x)
{
    return x;
}
static inline uint8_t zext_i32_i8 (uint32_t x)
{
    return x;
}
static inline uint16_t zext_i32_i16 (uint32_t x)
{
    return x;
}
static inline uint32_t zext_i32_i32 (uint32_t x)
{
    return x;
}
static inline uint64_t zext_i32_i64 (uint32_t x)
{
    return x;
}
static inline uint8_t zext_i64_i8 (uint64_t x)
{
    return x;
}
static inline uint16_t zext_i64_i16 (uint64_t x)
{
    return x;
}
static inline uint32_t zext_i64_i32 (uint64_t x)
{
    return x;
}
static inline uint64_t zext_i64_i64 (uint64_t x)
{
    return x;
}
static inline float fdiv32 (float x, float y)
{
    return x / y;
}
static inline float fadd32 (float x, float y)
{
    return x + y;
}
static inline float fsub32 (float x, float y)
{
    return x - y;
}
static inline float fmul32 (float x, float y)
{
    return x * y;
}
static inline float fpow32 (float x, float y)
{
    return pow(x, y);
}
static inline char cmplt32 (float x, float y)
{
    return x < y;
}
static inline char cmple32 (float x, float y)
{
    return x <= y;
}
static inline float sitofp_i8_f32 (int8_t x)
{
    return x;
}
static inline float sitofp_i16_f32 (int16_t x)
{
    return x;
}
static inline float sitofp_i32_f32 (int32_t x)
{
    return x;
}
static inline float sitofp_i64_f32 (int64_t x)
{
    return x;
}
static inline float uitofp_i8_f32 (uint8_t x)
{
    return x;
}
static inline float uitofp_i16_f32 (uint16_t x)
{
    return x;
}
static inline float uitofp_i32_f32 (uint32_t x)
{
    return x;
}
static inline float uitofp_i64_f32 (uint64_t x)
{
    return x;
}
static inline int8_t fptosi_f32_i8 (float x)
{
    return x;
}
static inline int16_t fptosi_f32_i16 (float x)
{
    return x;
}
static inline int32_t fptosi_f32_i32 (float x)
{
    return x;
}
static inline int64_t fptosi_f32_i64 (float x)
{
    return x;
}
static inline uint8_t tptoui_f32_i8 (float x)
{
    return x;
}
static inline uint16_t tptoui_f32_i16 (float x)
{
    return x;
}
static inline uint32_t tptoui_f32_i32 (float x)
{
    return x;
}
static inline uint64_t tptoui_f32_i64 (float x)
{
    return x;
}

__kernel void map_kernel_405 (__global unsigned char * mem_379)
{
    const uint global_thread_index_405 = get_global_id(0);
    
    if (global_thread_index_405 >= 3)
        return;
    
    
    int32_t i_406;
    
    // compute thread index
    {
        i_406 = global_thread_index_405;
    }
    // read kernel parameters
    { }
    // write kernel result
    {
        *(__global int32_t *) &mem_379[i_406 * 4] = 0;
    }
}
__kernel void map_kernel_409 (__global unsigned char * mem_379,
                              int32_t width_323, __global
                              unsigned char * mem_382)
{
    const uint global_thread_index_409 = get_global_id(0);
    
    if (global_thread_index_409 >= width_323 * 3)
        return;
    
    
    int32_t i_410;
    int32_t j_411;
    int32_t input_412;
    
    // compute thread index
    {
        i_410 = squot32(global_thread_index_409, 3);
        j_411 = global_thread_index_409 - squot32(global_thread_index_409, 3) *
            3;
    }
    // read kernel parameters
    {
        input_412 = *(__global int32_t *) &mem_379[j_411 * 4];
    }
    // write kernel result
    {
        *(__global int32_t *) &mem_382[(i_410 * 3 + j_411) * 4] = input_412;
    }
}
__kernel void map_kernel_415 (int32_t height_322, __global
                              unsigned char * mem_382, int32_t width_323,
                              __global unsigned char * mem_386)
{
    const uint global_thread_index_415 = get_global_id(0);
    
    if (global_thread_index_415 >= height_322 * width_323 * 3)
        return;
    
    
    int32_t i_416;
    int32_t j_417;
    int32_t j_418;
    int32_t input_419;
    
    // compute thread index
    {
        i_416 = squot32(global_thread_index_415, width_323 * 3);
        j_417 = squot32(global_thread_index_415 -
                        squot32(global_thread_index_415, width_323 * 3) *
                        (width_323 * 3), 3);
        j_418 = global_thread_index_415 - squot32(global_thread_index_415,
                                                  width_323 * 3) * (width_323 *
                                                                    3) -
            squot32(global_thread_index_415 - squot32(global_thread_index_415,
                                                      width_323 * 3) *
                    (width_323 * 3), 3) * 3;
    }
    // read kernel parameters
    {
        input_419 = *(__global int32_t *) &mem_382[(j_417 * 3 + j_418) * 4];
    }
    // write kernel result
    {
        *(__global int32_t *) &mem_386[(i_416 * (width_323 * 3) + (j_417 * 3 +
                                                                   j_418)) *
                                       4] = input_419;
    }
}
__kernel void map_kernel_422 (int32_t frames_324, __global
                              unsigned char * mem_386, int32_t height_322,
                              int32_t width_323, __global
                              unsigned char * mem_391)
{
    const uint global_thread_index_422 = get_global_id(0);
    
    if (global_thread_index_422 >= frames_324 * height_322 * width_323 * 3)
        return;
    
    
    int32_t i_423;
    int32_t j_424;
    int32_t j_425;
    int32_t j_426;
    int32_t input_427;
    
    // compute thread index
    {
        i_423 = squot32(global_thread_index_422, height_322 * width_323 * 3);
        j_424 = squot32(global_thread_index_422 -
                        squot32(global_thread_index_422, height_322 *
                                width_323 * 3) * (height_322 * width_323 * 3),
                        width_323 * 3);
        j_425 = squot32(global_thread_index_422 -
                        squot32(global_thread_index_422, height_322 *
                                width_323 * 3) * (height_322 * width_323 * 3) -
                        squot32(global_thread_index_422 -
                                squot32(global_thread_index_422, height_322 *
                                        width_323 * 3) * (height_322 *
                                                          width_323 * 3),
                                width_323 * 3) * (width_323 * 3), 3);
        j_426 = global_thread_index_422 - squot32(global_thread_index_422,
                                                  height_322 * width_323 * 3) *
            (height_322 * width_323 * 3) - squot32(global_thread_index_422 -
                                                   squot32(global_thread_index_422,
                                                           height_322 *
                                                           width_323 * 3) *
                                                   (height_322 * width_323 * 3),
                                                   width_323 * 3) * (width_323 *
                                                                     3) -
            squot32(global_thread_index_422 - squot32(global_thread_index_422,
                                                      height_322 * width_323 *
                                                      3) * (height_322 *
                                                            width_323 * 3) -
                    squot32(global_thread_index_422 -
                            squot32(global_thread_index_422, height_322 *
                                    width_323 * 3) * (height_322 * width_323 *
                                                      3), width_323 * 3) *
                    (width_323 * 3), 3) * 3;
    }
    // read kernel parameters
    {
        input_427 = *(__global int32_t *) &mem_386[(j_424 * (width_323 * 3) +
                                                    (j_425 * 3 + j_426)) * 4];
    }
    // write kernel result
    {
        *(__global int32_t *) &mem_391[(i_423 * (height_322 * (width_323 * 3)) +
                                        (j_424 * (width_323 * 3) + (j_425 * 3 +
                                                                    j_426))) *
                                       4] = input_427;
    }
}
__kernel void map_kernel_364 (__global unsigned char * a_mem_393,
                              int32_t shape_331, int32_t width_323, __global
                              unsigned char * mem_395)
{
    const uint kernel_thread_index_364 = get_global_id(0);
    
    if (kernel_thread_index_364 >= shape_331)
        return;
    
    
    int32_t i_365;
    int8_t not_curried_366;
    
    // compute thread index
    {
        i_365 = kernel_thread_index_364;
    }
    // read kernel parameters
    {
        not_curried_366 = *(__global int8_t *) &a_mem_393[squot32(i_365,
                                                                  width_323 *
                                                                  3) *
                                                          (width_323 * 3) +
                                                          (squot32(i_365 -
                                                                   squot32(i_365,
                                                                           width_323 *
                                                                           3) *
                                                                   (width_323 *
                                                                    3), 3) * 3 +
                                                           (i_365 -
                                                            squot32(i_365,
                                                                    width_323 *
                                                                    3) *
                                                            (width_323 * 3) -
                                                            squot32(i_365 -
                                                                    squot32(i_365,
                                                                            width_323 *
                                                                            3) *
                                                                    (width_323 *
                                                                     3), 3) *
                                                            3))];
    }
    
    float x_367 = uitofp_i8_f32(not_curried_366);
    float trunc_arg_368 = x_367 * 0.949999988079071F;
    int8_t res_369 = fptoui_f32_i8(trunc_arg_368);
    
    // write kernel result
    {
        *(__global int8_t *) &mem_395[i_365] = res_369;
    }
}
__kernel void map_kernel_371 (int32_t shape_333, __global
                              unsigned char * mem_395, __global
                              unsigned char * mem_397)
{
    const uint kernel_thread_index_371 = get_global_id(0);
    
    if (kernel_thread_index_371 >= shape_333)
        return;
    
    
    int32_t i_372;
    int8_t unop_param_373;
    
    // compute thread index
    {
        i_372 = kernel_thread_index_371;
    }
    // read kernel parameters
    {
        unop_param_373 = *(__global int8_t *) &mem_395[i_372];
    }
    
    int32_t res_374 = zext_i8_i32(unop_param_373);
    int32_t res_375 = umod32(res_374, 256);
    
    // write kernel result
    {
        *(__global int32_t *) &mem_397[i_372 * 4] = res_375;
    }
}"""
cl_group_size = 512


def setup_opencl(context_set, queue_set):
  global ctx
  global queue
  global program
  global map_kernel_405_var
  global map_kernel_409_var
  global map_kernel_415_var
  global map_kernel_422_var
  global map_kernel_364_var
  global map_kernel_371_var

  ctx = context_set
  queue = queue_set

  # Some drivers complain if we compile empty programs, so bail out early if so.
  if (len(fut_opencl_src) == 0):
    assert True

  program = cl.Program(ctx, fut_opencl_src).build(["-DFUT_BLOCK_DIM={}".format(FUT_BLOCK_DIM), "-DWAVE_SIZE=32"])

  map_kernel_405_var = program.map_kernel_405
  map_kernel_409_var = program.map_kernel_409
  map_kernel_415_var = program.map_kernel_415
  map_kernel_422_var = program.map_kernel_422
  map_kernel_364_var = program.map_kernel_364
  map_kernel_371_var = program.map_kernel_371

def _futhark_main(a_mem_size_376, a_mem_377, height_322, width_323, frames_324):
  mem_379 = cl.Buffer(ctx, cl.mem_flags.READ_WRITE,
                      int32(12) if (int32(int32(12)) > int32(0)) else int32(1))
  group_size_407 = int32(512)
  num_groups_408 = squot32(((int32(int32(3)) + group_size_407) - int32(int32(1))),
                           group_size_407)
  if ((int32(1) * (num_groups_408 * group_size_407)) != int32(0)):
    map_kernel_405_var.set_args(mem_379)
    cl.enqueue_nd_range_kernel(queue, map_kernel_405_var,
                               (asscalar((num_groups_408 * group_size_407)),),
                               (group_size_407,))
    if synchronous:
      queue.finish()
  x_381 = (int32(int32(4)) * width_323)
  bytes_380 = (x_381 * int32(int32(3)))
  mem_382 = cl.Buffer(ctx, cl.mem_flags.READ_WRITE,
                      asscalar(bytes_380) if (bytes_380 > int32(0)) else int32(1))
  group_size_413 = int32(512)
  num_groups_414 = squot32((((width_323 * int32(int32(3))) + group_size_413) - int32(int32(1))),
                           group_size_413)
  if ((int32(1) * (num_groups_414 * group_size_413)) != int32(0)):
    map_kernel_409_var.set_args(mem_379, int32(width_323), mem_382)
    cl.enqueue_nd_range_kernel(queue, map_kernel_409_var,
                               (asscalar((num_groups_414 * group_size_413)),),
                               (group_size_413,))
    if synchronous:
      queue.finish()
  x_384 = (int32(int32(4)) * height_322)
  x_385 = (x_384 * width_323)
  bytes_383 = (x_385 * int32(int32(3)))
  mem_386 = cl.Buffer(ctx, cl.mem_flags.READ_WRITE,
                      asscalar(bytes_383) if (bytes_383 > int32(0)) else int32(1))
  group_size_420 = int32(512)
  num_groups_421 = squot32(((((height_322 * width_323) * int32(int32(3))) + group_size_420) - int32(int32(1))),
                           group_size_420)
  if ((int32(1) * (num_groups_421 * group_size_420)) != int32(0)):
    map_kernel_415_var.set_args(int32(height_322), mem_382, int32(width_323),
                                mem_386)
    cl.enqueue_nd_range_kernel(queue, map_kernel_415_var,
                               (asscalar((num_groups_421 * group_size_420)),),
                               (group_size_420,))
    if synchronous:
      queue.finish()
  x_388 = (int32(int32(4)) * frames_324)
  x_389 = (x_388 * height_322)
  x_390 = (x_389 * width_323)
  bytes_387 = (x_390 * int32(int32(3)))
  mem_391 = cl.Buffer(ctx, cl.mem_flags.READ_WRITE,
                      asscalar(bytes_387) if (bytes_387 > int32(0)) else int32(1))
  group_size_428 = int32(512)
  num_groups_429 = squot32((((((frames_324 * height_322) * width_323) * int32(int32(3))) + group_size_428) - int32(int32(1))),
                           group_size_428)
  if ((int32(1) * (num_groups_429 * group_size_428)) != int32(0)):
    map_kernel_422_var.set_args(int32(frames_324), mem_386, int32(height_322),
                                int32(width_323), mem_391)
    cl.enqueue_nd_range_kernel(queue, map_kernel_422_var,
                               (asscalar((num_groups_429 * group_size_428)),),
                               (group_size_428,))
    if synchronous:
      queue.finish()
  x_330 = (int32(int32(3)) * width_323)
  shape_331 = (x_330 * height_322)
  x_332 = (height_322 * width_323)
  shape_333 = (x_332 * int32(int32(3)))
  bytes_396 = (int32(int32(4)) * shape_333)
  mem_397 = cl.Buffer(ctx, cl.mem_flags.READ_WRITE,
                      asscalar(bytes_396) if (bytes_396 > int32(0)) else int32(1))
  double_buffer_mem_401 = cl.Buffer(ctx, cl.mem_flags.READ_WRITE,
                                    asscalar(shape_331) if (shape_331 > int32(0)) else int32(1))
  mem_395 = cl.Buffer(ctx, cl.mem_flags.READ_WRITE,
                      asscalar(shape_331) if (shape_331 > int32(0)) else int32(1))
  a_mem_size_392 = a_mem_size_376
  a_mem_393 = a_mem_377
  for i_336 in range(frames_324):
    i_336 = int32(i_336)
    group_size_434 = int32(512)
    num_groups_435 = squot32(((shape_331 + group_size_434) - int32(int32(1))),
                             group_size_434)
    if ((int32(1) * (num_groups_435 * group_size_434)) != int32(0)):
      map_kernel_364_var.set_args(a_mem_393, int32(shape_331), int32(width_323),
                                  mem_395)
      cl.enqueue_nd_range_kernel(queue, map_kernel_364_var,
                                 (asscalar((num_groups_435 * group_size_434)),),
                                 (group_size_434,))
      if synchronous:
        queue.finish()
    group_size_436 = int32(512)
    num_groups_437 = squot32(((shape_333 + group_size_436) - int32(int32(1))),
                             group_size_436)
    if ((int32(1) * (num_groups_437 * group_size_436)) != int32(0)):
      map_kernel_371_var.set_args(int32(shape_333), mem_395, mem_397)
      cl.enqueue_nd_range_kernel(queue, map_kernel_371_var,
                                 (asscalar((num_groups_437 * group_size_436)),),
                                 (group_size_436,))
      if synchronous:
        queue.finish()
    if (((height_322 * (width_323 * int32(int32(3)))) * int32(4)) > int32(0)):
      cl.enqueue_copy(queue, mem_391, mem_397,
                      dest_offset=asscalar((((height_322 * (width_323 * int32(int32(3)))) * i_336) * int32(int32(4)))),
                      src_offset=int32(0),
                      byte_count=asscalar(((height_322 * (width_323 * int32(int32(3)))) * int32(4))))
    if synchronous:
      queue.finish()
    if (((height_322 * (width_323 * int32(int32(3)))) * int32(1)) > int32(0)):
      cl.enqueue_copy(queue, double_buffer_mem_401, mem_395,
                      dest_offset=int32(0), src_offset=int32(0),
                      byte_count=asscalar(((height_322 * (width_323 * int32(int32(3)))) * int32(1))))
    if synchronous:
      queue.finish()
    a_mem_size_tmp_430 = shape_331
    a_mem_tmp_431 = double_buffer_mem_401
    a_mem_size_392 = a_mem_size_tmp_430
    a_mem_393 = a_mem_tmp_431
  a_mem_400 = a_mem_393
  a_mem_size_399 = a_mem_size_392
  out_mem_403 = mem_391
  out_memsize_404 = bytes_387
  return (out_memsize_404, out_mem_403)
def main(frames_324, a_mem_377):
  frames_324 = int32(frames_324)
  height_322 = int32(a_mem_377.shape[int32(0)])
  width_323 = int32(a_mem_377.shape[int32(1)])
  assert (int32(3) == a_mem_377.shape[int32(2)]), 'shape dimension is incorrect for the constant dimension'
  a_mem_size_376 = int32(a_mem_377.nbytes)
  a_mem_device_438 = cl.Buffer(ctx, cl.mem_flags.READ_WRITE,
                               asscalar(a_mem_size_376) if (a_mem_size_376 > int32(0)) else int32(1))
  cl.enqueue_copy(queue, a_mem_device_438,
                  a_mem_377[int32(0):(int32(0) + (a_mem_377.nbytes // 1))],
                  device_offset=int32(0), is_blocking=synchronous)
  a_mem_377 = a_mem_device_438
  (out_memsize_404, out_mem_403) = _futhark_main(a_mem_size_376, a_mem_377,
                                                 height_322, width_323,
                                                 frames_324)
  out_mem_device_439 = empty((frames_324, height_322, width_323, int32(3)),
                             dtype=c_int32)
  cl.enqueue_copy(queue,
                  out_mem_device_439[int32(0):(int32(0) + (out_memsize_404 // 4))],
                  out_mem_403, device_offset=int32(0), is_blocking=synchronous)
  out_mem_403 = out_mem_device_439
  return out_mem_403
if (__name__ == "__main__"):
  runtime_file = None
  parser = argparse.ArgumentParser(description="A compiled Futhark program.")
  parser.add_argument("-t", "--write-runtime-to", action="append", default=[])
  parser_result = vars(parser.parse_args(sys.argv[1:]))
  for optarg in parser_result["write_runtime_to"]:
    if runtime_file:
      runtime_file.close()
    runtime_file = open(optarg, "w")
  frames_324 = read_int(sys.stdin)
  a_mem_377 = read_array(sys.stdin, read_int, 3, c_int8)
  try:
    time_start = time.time()
    out_mem_403 = main(frames_324, a_mem_377)
    queue.finish()
    time_end = time.time()
    if runtime_file:
      runtime_file.write(str((int((time_end * int32(1000000))) - int((time_start * int32(1000000))))))
      runtime_file.write("\n")
      runtime_file.close()
  except AssertionError as e:
    sys.exit("Assertion.{} failed".format(e))
  write_array(sys.stdout, out_mem_403, "i32")