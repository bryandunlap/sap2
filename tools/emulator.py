import sys

MEM_SIZE = 0xffff
BYTE_SIZE = 0xff


class SAP2Emulator:
    def __init__(self):
        self._pc = 0x0000
        self._a = 0x00
        self._b = 0x00
        self._c = 0x00
        self._s = False
        self._z = False
        self._mem = bytearray(MEM_SIZE + 1)
        self._halt = False
        self._seg = False

        self._instructions = {
            0x80: self._add_b,
            0x81: self._add_c,
            0xa0: self._ana_b,
            0xa1: self._ana_c,
            0xe6: self._ani,
            0xcd: self._call,
            0x2f: self._cma,
            0x3d: self._dcr_a,
            0x05: self._dcr_b,
            0x0d: self._dcr_c,
            0x76: self._hlt,
            0xdb: self._in,
            0x3c: self._inr_a,
            0x04: self._inr_b,
            0x0c: self._inr_c,
            0xfa: self._jm,
            0xc3: self._jmp,
            0xc2: self._jnz,
            0xca: self._jz,
            0x3a: self._lda,
            0x78: self._mov_ab,
            0x79: self._mov_ac,
            0x47: self._mov_ba,
            0x41: self._mov_bc,
            0x4f: self._mov_ca,
            0x48: self._mov_cb,
            0x3e: self._mvi_a,
            0x06: self._mvi_b,
            0x0e: self._mvi_c,
            0x00: self._nop,
            0xb0: self._ora_b,
            0xb1: self._ora_c,
            0xf6: self._ori,
            0xd3: self._out,
            0x17: self._ral,
            0x1f: self._rar,
            0xc9: self._ret,
            0x32: self._sta,
            0x90: self._sub_b,
            0x91: self._sub_c,
            0xa8: self._xra_b,
            0xa9: self._xra_c,
            0xee: self._xri
        }

    def load(self, start: int, binary: bytes):
        self._mem[start:len(binary)] = binary

    def start(self):
        while not self._halt and not self._seg:
            self._instructions[self._mem[self._pc]]()
        if self._seg:
            raise SegfaultError(self)

    def _increment_pc(self):
        self._pc += 1
        if self._pc > MEM_SIZE:
            self._seg = True
            raise SegfaultError(self)

    def _set_flags(self):
        if self._a == 0:
            self._s = False
            self._z = True
        else:
            self._s = bool(self._a & 0x80)
            self._z = False

    # Instructions
    def _add_b(self):
        self._increment_pc()
        self._a = self._a + self._b
        self._set_flags()

    def _add_c(self):
        self._increment_pc()
        self._a = self._a + self._c
        self._set_flags()

    def _ana_b(self):
        self._increment_pc()
        self._a = self._a & self._b
        self._set_flags()

    def _ana_c(self):
        self._increment_pc()
        self._a = self._a & self._c
        self._set_flags()

    def _ani(self):
        self._increment_pc()
        self._a = self._a & self._mem[self._pc]
        self._increment_pc()
        self._set_flags()

    def _call(self):
        self._increment_pc()
        lsb = self._mem[self._pc]
        self._increment_pc()
        msb = self._mem[self._pc] << 8
        self._increment_pc()
        self._mem[0xfffe] = self._pc & BYTE_SIZE
        self._mem[0xffff] = (self._pc >> 8) & BYTE_SIZE
        self._pc = msb + lsb

    def _cma(self):
        self._increment_pc()
        self._a = -self._a
        self._set_flags()

    def _dcr_a(self):
        self._increment_pc()
        self._a -= 1
        self._set_flags()

    def _dcr_b(self):
        self._a = self._b
        self._dcr_a()

    def _dcr_c(self):
        self._a = self._c
        self._dcr_a()

    def _hlt(self):
        self._halt = True

    def _in(self):
        self._increment_pc()
        self._a = ord(sys.stdin.read()) & BYTE_SIZE

    def _inr_a(self):
        self._increment_pc()
        self._a += 1
        self._set_flags()

    def _inr_b(self):
        self._a = self._b
        self._inr_a()

    def _inr_c(self):
        self._a = self._c
        self._inr_a()

    def _jm(self):
        self._increment_pc()
        lsb = self._mem[self._pc]
        self._increment_pc()
        msb = self._mem[self._pc] << 8
        if self._s:
            self._pc = msb + lsb
        else:
            self._increment_pc()

    def _jmp(self):
        self._increment_pc()
        lsb = self._mem[self._pc]
        self._increment_pc()
        msb = self._mem[self._pc] << 8
        self._pc = msb + lsb

    def _jnz(self):
        self._increment_pc()
        lsb = self._mem[self._pc]
        self._increment_pc()
        msb = self._mem[self._pc] << 8
        if not self._z:
            self._pc = msb + lsb
        else:
            self._increment_pc()

    def _jz(self):
        self._increment_pc()
        lsb = self._mem[self._pc]
        self._increment_pc()
        msb = self._mem[self._pc] << 8
        if self._z:
            self._pc = msb + lsb
        else:
            self._increment_pc()

    def _lda(self):
        self._increment_pc()
        lsb = self._mem[self._pc]
        self._increment_pc()
        msb = self._mem[self._pc] << 8
        self._increment_pc()
        self._a = self._mem[msb + lsb]

    def _mov_ab(self):
        self._increment_pc()
        self._a = self._b
        self._set_flags()

    def _mov_ac(self):
        self._increment_pc()
        self._a = self._c
        self._set_flags()

    def _mov_ba(self):
        self._increment_pc()
        self._b = self._a

    def _mov_bc(self):
        self._increment_pc()
        self._b = self._c

    def _mov_ca(self):
        self._increment_pc()
        self._c = self._a

    def _mov_cb(self):
        self._increment_pc()
        self._c = self._b

    def _mvi_a(self):
        self._increment_pc()
        self._a = self._mem[self._pc]
        self._increment_pc()
        self._set_flags()

    def _mvi_b(self):
        self._increment_pc()
        self._b = self._mem[self._pc]
        self._increment_pc()

    def _mvi_c(self):
        self._increment_pc()
        self._c = self._mem[self._pc]
        self._increment_pc()

    def _nop(self):
        self._increment_pc()

    def _ora_b(self):
        self._increment_pc()
        self._a = self._a | self._b
        self._set_flags()

    def _ora_c(self):
        self._increment_pc()
        self._a = self._a | self._c
        self._set_flags()

    def _ori(self):
        self._increment_pc()
        self._a = self._a | self._mem[self._pc]
        self._increment_pc()
        self._set_flags()

    def _out(self):
        self._increment_pc()
        sys.stdout.write("%s" % self._a)
        self._increment_pc()

    def _ral(self):
        # TODO: IMPLEMENT
        self._increment_pc()

    def _rar(self):
        # TODO: IMPLEMENT
        self._increment_pc()

    def _ret(self):
        self._pc = self._mem[0xffff] + self._mem[0xfffe]

    def _sta(self):
        self._increment_pc()
        lsb = self._mem[self._pc]
        self._increment_pc()
        msb = self._mem[self._pc] << 8
        self._increment_pc()
        self._mem[msb + lsb] = self._a

    def _sub_b(self):
        self._increment_pc()
        self._a = self._a - self._b
        self._set_flags()

    def _sub_c(self):
        self._increment_pc()
        self._a = self._a - self._c
        self._set_flags()

    def _xra_b(self):
        self._increment_pc()
        self._a = self._a ^ self._b
        self._set_flags()

    def _xra_c(self):
        self._increment_pc()
        self._a = self._a ^ self._c
        self._set_flags()

    def _xri(self):
        self._increment_pc()
        self._a = self._a ^ self._mem[self._pc]
        self._increment_pc()
        self._set_flags()


class SegfaultError(Exception):
    def __init__(self, emulator: SAP2Emulator):
        super(SegfaultError, self).__init__(emulator)
