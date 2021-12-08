#Исследовательский микропроцессор, регистры 16-бит, размер памяти ROM 65535 х 16, размер ОЗУ 255 х 16.
class rproc01():
    def __init__(self):
#инициализация регистров
        self.RD1 = self.REG(0)
        self.RD2 = self.REG(0)
        self.RO2 = self.REG(0)
        self.RO1 = self.REG(0)
        self.AC = self.REG(0)
        #инициализируем память RAM
        self.RAM = list()
        for i in range(0,256):
            self.RAM.append(self.REG(0))
        #инициализируем память ROM
        


#функция для записи десятичных чисел в регистр
  
    def REG(self, a):
        if a >=0:
            A = bin (a)
            Ab = A[2:len(A)]
            if len(Ab)<=16:
                Ab = Ab.rjust(16,'0')
            else:
                Ab = Ab[(len(Ab)-16):len(Ab)]
            return Ab
        else:
            A = bin (a)
            Ab = A[3:len(A)]
            if len(Ab)<=16:
                Ab = Ab.rjust(16,'0')
            else:
                Ab = Ab[(len(Ab)-16):len(Ab)]
            return Ab
        
#функции чтения/записи памяти
    def RAM_write(self, address, register):
        self.RAM.insert(address, register)
        
    def RAM_read(self, address):
        self.AC = self.RAM[address]
        
        
#функции АЛУ
    def SUB(self):
        a = int(self.RD1,2)
        b = int(self.RD2,2)
        C = a - b
        self.RO1 = self.REG(C)
    
    def SUM(self):
        a = int(self.RD1,2)
        b = int(self.RD2,2)
        C = a + b
        self.RO1 = self.REG(C)

    def AND(self):
        c = str()
        for i in range (0,16):
           if self.RD1[i] == '1' and self.RD2[i] == '1':
               c += '1'
           else:
               c += '0'
        self.RO1 = c

    def OR (self):
        c = str()
        for i in range (0,16):
           if self.RD1[i] == '1' or self.RD2[i] == '1':
               c += '1'
           else:
               c += '0'
        self.RO1 = c

    def XOR (self):
        c = str()
        for i in range (0,16):
           if ((self.RD1[i] == '1' and self.RD2[i] == '0') or
               (self.RD1[i] == '0' and self.RD2[i] == '1')):
               c += '1'
           else:
               c += '0'
        self.RO1 = c
        
    def MULT(self):
        a = int(self.RD1,2)
        b = int(self.RD2,2)
        C = a * b
        self.RO1 = self.REG(C)

    def DEV(self):
        a = int(self.RD1,2)
        b = int(self.RD2,2)
        C = int (a / b)
        ostatok = a % b
        self.RO1 = self.REG(C)
        self.RO2 = self.REG(ostatok)
        
proc = rproc01()
proc.RD1 = proc.REG(1)
proc.RD2 = proc.REG(5)
proc.SUB()
proc.RAM_write(0,proc.RO1)
proc.RD1 = proc.REG(1)
proc.RD2 = proc.REG(3)
proc.SUB()
proc.RAM_write(1,proc.RO1)
proc.RAM_read(0)
proc.RD1 = proc.AC
proc.RAM_read(1)
proc.RD2 = proc.AC
proc.DEV()
print(proc.RO1)
#print (f'R1 = {proc.reg_data1}')
#print (f'R2 = {proc.reg_data2}')
#print(f'RO = {proc.reg_out1}')
#print (f'RD = {proc.reg_out2}')

