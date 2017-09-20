import unittest
import tools


class EmulatorTests(unittest.TestCase):
    @staticmethod
    def test_example_11_2():
        binary = bytes([0x3e, 0x49, 0x06, 0x4a, 0x0e, 0x4b, 0x32, 0x85, 0x62, 0x76])
        emulator = tools.SAP2Emulator()
        emulator.load(0x0000, binary)
        emulator.start()
        assert emulator._mem[0x6285] == 0x49
        assert emulator._a == 0x49
        assert emulator._b == 0x4a
        assert emulator._c == 0x4b

    @staticmethod
    def test_example_11_4():
        binary = bytes([0x3e, 0x17, 0x06, 0x2d, 0x80, 0x32, 0x00, 0x56, 0x3c, 0x4f, 0xd3, 0x00, 0x76])
        emulator = tools.SAP2Emulator()
        emulator.load(0x0000, binary)
        emulator.start()
        assert emulator._mem[0x5600] == 0x44
        assert emulator._a == 0x45


if __name__ == "__main__":
    unittest.main()
