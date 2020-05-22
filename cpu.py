
import sys

CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
LDI = 0b10000010
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
HLT = 0b00000001
PRN = 0b01000111
SP_MEM = 0xf3
CALL = 0b01010000
RET = 0b00010001
SP = 7
ADD = 0b10100000


class CPU:


  def __init_(self):
    self.pc = 0x00
    self.reg = [0] * 8
    self.reg[SP] = SP_MEM
    self.ram = [0] * 256
    self.instructions = {}
    self.flag = 0b0000000

    def loadProgram(self):
        program = []
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    str_value = line.split('#')[0].strip()
                    if str_value == '':
                        continue
                    value = int(str_value, 2)
                    program.append([value])

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1
