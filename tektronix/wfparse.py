from tektronix import FormatException
import enum
import io
from tektronix import FormatException

class LexState(enum.IntEnum):
    TOKEN_START = 0
    IN_QUOTES = 1
    IN_TOKEN = 2
    ESCAPE = 3
    END_QUOTES = 4

def split_string(v):
    state = LexState.TOKEN_START
    token = io.StringIO()
    token_list = []

    def push_token():
        token_list.append(token.getvalue())
        token.seek(0)
        token.truncate(0)

    for c in v:
        if state == LexState.TOKEN_START:
            if c == '"':
                state = LexState.IN_QUOTES
            elif c == ';':
                state = LexState.TOKEN_START
                push_token()
            else:
                state = LexState.IN_TOKEN
                token.write(c)
        elif state == LexState.IN_TOKEN:
            if c == ';':
                state = LexState.TOKEN_START
                push_token()
            elif c == '"':
                raise FormatException("Quotes in unquoted token")
            else:
                token.write(c)
        elif state == LexState.IN_QUOTES:
            if c == '"':
                state = LexState.END_QUOTES
            elif c == '\\':
                state = LexState.ESCAPE
            else:
                state = LexState.IN_QUOTES
                token.write(c)
        elif state == LexState.ESCAPE:
            if c == '"':
                token.write(c)
                state = LexState.IN_QUOTES
            else:
                raise FormatException("Unknown escape")

        elif state == LexState.END_QUOTES:
            if c == ';':
                push_token()
                state = LexState.TOKEN_START
            else:
                raise FormatException("Extra characters after quote")

    if state in [LexState.TOKEN_START, LexState.END_QUOTES, LexState.IN_TOKEN]:
        push_token()
    else:
        raise FormatException("Unfinished token")

    return token_list

class WfmPresets:
    def __init__(self):
        # BYT_NR
        self.bytes_per_point = None
        # ENCDG
        self.encoding = None # BIN or ASC
        # BN_FMT
        self.signed = None
        # BYT_OR
        self.big_endian = None
        # NR_PT
        self.number_of_points = None
        # WFID
        self.waweform_ident = None
        # PT_FMT
        self.point_format = None # Y or ENV
        # XINCR
        self.x_seconds_per_point = None
        # XZERO
        self.x_zero = None
        # XUNIT
        self.x_unit = None
        # YMULT
        self.y_mult = None
        # YZERO
        self.y_zero = None
        # Y_OFF
        self.y_off = None
        # Y_UNIT
        self.y_unit = None

    def dump(self):
        for k, v in self.__dict__.items():
            print('  {}: {}'.format(k, v))

    @staticmethod
    def parse(str):
        wfm = WfmPresets()
        tokens = split_string(str)
        try:
            wfm.bytes_per_point = int(tokens[0])
            wfm.encoding = tokens[2]
            if wfm.encoding not in ['BIN', 'ASC']:
                raise FormatException('Unknwon encoding')
            wfm.signed = {'RI': True, 'RP': False}[tokens[3]]
            wfm.big_endian = {'MSB': True, 'LSB': False}[tokens[4]]
            wfm.number_of_points = int(tokens[5])
            wfm.waweform_ident = tokens[6]
            wfm.point_format = tokens[7]
            if wfm.point_format not in ['Y', 'ENV']:
                raise FormatException('Unknown point format')
            wfm.x_seconds_per_point = float(tokens[8])
            wfm.x_zero = float(tokens[10])
            wfm.x_unit = tokens[11]
            wfm.y_mult = float(tokens[12])
            wfm.y_zero = float(tokens[13])
            wfm.y_off = float(tokens[14])
            wfm.y_unit = tokens[15]
        except ValueError as ex:
            raise FormatException() from ex
        except KeyError as ex:
            raise FormatException("Unknown value: {}".format(ex.key)) from ex
        return wfm

