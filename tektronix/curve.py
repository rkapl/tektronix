from tektronix import FormatException
import io
import struct

# parse and validate header
def split_header(data):
    data = io.BytesIO(data)
    c = data.read1(1)
    if c != b'#':
        raise FormatException('First character of curve data should be #')

    try:
        c = int(data.read1(1).decode('ascii'))
        data_len = int(data.read1(c).decode('ascii'))
    except ValueError:
        raise FormatException('Invalid header format')

    data = data.read1()
    if len(data) == 0:
        raise FormatException('Missing data')
    if data[len(data) - 1] != 0x0A:
        raise FormatException('Missing terminator')
    data = data[:len(data) - 1]

    if len(data) != data_len:
        raise FormatException('Header does not match data, {} != {}'.format(len(data), data_len))
    return data

def parse_curve_content(data):
    if len(data) % 2 != 0:
        raise FormatException("Curve data is not divisible by 2")
    data_len = int(len(data)/2)
    return list(struct.unpack('>{}h'.format(data_len), data))


def parse_curve(data):
    data = split_header(data)
    return parse_curve_content(data)