
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

        def __init__(self):
         self.pc = 0x00
         self.reg = [0] * 8
         self.reg[SP] = SP_MEM
         self.ram = [0] * 256
         self.instructions = {CMP: self.cmp, JMP: self.jmp, JEQ: self.jeq, JNE: self.jne, LDI: self.ldi, PRN: self.prn,
                             MUL: self.mul, HLT: self.hlt}
         self.flag = 0b0000000

        def load(self):
            program = []
            try:
                with open(sys.argv[1]) as file:
                    for line in file:
                        str_value = line.split('#')[0].strip()
                        if str_value == '':
                            continue
                        value = int(str_value, 2)
                        program = program + [value]

            except FileNotFoundError:
              print('File Not Found')
              exit(1)
            except IndexError:
              print('You need to specify the file to run.')
              exit(1)
            address = 0

            for instruction in program:
                self.ram[address] = instruction
                address += 1

        def trace(self):
          """Handy function to print out the CPU state. You might want to call this
          from run() if you need help debugging."""

          print(f"TRACE: %02X | %02X %02X %02X |" % (
              self.pc,
              # self.fl,
              # self.ie,
              self.ram_read(self.pc),
              self.ram_read(self.pc + 1),
              self.ram_read(self.pc + 2)
          ), end='')

          for i in range(8):
              print(" %02X" % self.reg[i], end='')
          print()
        
        def alu(self, operation, reg1, reg2):

          if operation == "MUL":
            self.reg[reg1] = self.reg[reg1] * self.reg[reg2]
          elif operation == "ADD":
            self.reg[reg1] += self.reg[reg2]
          elif operation == "CMP":
            if self.reg[reg1] == self.reg[reg2]:
              self.flag = bin(1)
            elif self.reg[reg1] < self.reg[reg2]:
              self.flag = bin(1 << 2)
            elif self.reg[reg1] > self.reg[reg2]:
              self.flag = bin(1 << 1)



        def cpuCounter(self, value, compare=0b11000000):
            newValue = value & compare
            newValue = newValue >> 6
            return newValue

        def ram_read(self, address):
            return self.ram[address]

        def ram_write(self, address, value):
             self.ram[address] = value

        def ldi(self):
            address = self.ram[self.pc + 1]
            value = self.ram[self.pc + 2]
            self.reg[address] = value
            count = self.cpuCounter(LDI)
            self.pc += count + 1

        def cmp(self):
            self.alu('CMP', self.ram_read(self.pc + 1),
                     self.ram_read(self.pc + 2))
            counter = self.cpuCounter(CMP)
            self.pc += counter + 1

        def jmp(self):
            self.pc = self.reg[self.ram_read(self.pc + 1)]

        def jeq(self):
          if self.flag != '0b1':
            self.pc += self.cpuCounter(JEQ) + 1
          else:
            self.pc = self.reg[self.ram_read(self.pc + 1)]

        def jne(self):
          if self.flag == '0b1':
            self.pc += self.cpuCounter(JNE) + 1
          else:
            self.pc = self.reg[self.ram_read(self.pc + 1)]

        def mul(self):
          self.alu('MUL', self.ram[self.pc + 1], self.ram[self.pc + 2])
          self.pc += self.cpuCounter(MUL) + 1

        def prn(self):
          address = self.ram[self.pc + 1]
          print(self.reg[address])
          count = self.cpuCounter(PRN)
          self.pc += count + 1

        def hlt(self):
          exit(0)

        def run(self):
          running = True
          while running:
            self.instructions[self.ram[self.pc]]()
