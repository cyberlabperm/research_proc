#Исследовательский микропроцессор, регистры 16-бит, размер памяти ROM 65535 х 16, размер ОЗУ 255 х 16.
class rproc01():
    def __init__(self):
#инициализация регистров
        self.RDX1 = self.REG(0)
        self.RDX2 = self.REG(0)
        self.RDY1 = self.REG(0)
        self.RDY2 = self.REG(0)
        self.RO2 = self.REG(0)
        self.RO1 = self.REG(0)
        self.AC = self.REG(0)
        #инициализируем память RAM
        self.RAM = list()
        for i in range(0,256):
            self.RAM.append(self.REG(0))
        #инициализируем память ROM
        


#функция для работы с двоично-десятичными числами записи десятичных чисел в регистр
    def two_comp_to_int(self,a):
        
    def two_compliment(self,a):
            A = bin (a)
            Ab = str()
            ab = A[2:len(A)]
            for i in range (0,len(ab)):
                if ab[i] == '1':
                    Ab += '0'
                else:
                    Ab += '1' 
            if len(Ab)<=16:
                Ab = Ab.rjust(16,'1')
            else:
                Ab = Ab[(len(Ab)-16):len(Ab)]                
            return Ab
        
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
            ab = self.two_compliment(abs(a))
            return ab
        
#функции чтения/записи памяти
    def RAM_write(self, address, register):
        self.RAM.insert(address, register)
        
    def RAM_read(self, address):
        self.AC = self.RAM[address]
        
        
#функции АЛУ
    def two_points_sum(self):
        Xp = int(self.RDX1,2)
        Yp = int(self.RDX2,2)
        Xq = int(self.RDY1,2)
        Yq = int(self.RDY2,2)
        if Xp != Xq and Yp != Yq:
            m = (Yp - Yq) / (Xp - Xq)
        else:
            m = (3 * Xp ** 2 + a) / (2 * Yp)

        Xr = int(m ** 2 - Xp - Xq)
        Yr = int(Yp + m * (Xr - Xp))
        self.ROX = self.REG(Xr)
        self.ROY = self.REG(Yr)

    def scalar_multiplication(self):
        
proc = rproc01()
proc.RDX1 = proc.REG(1)
proc.RDX2 = proc.REG(2)
proc.RDY1 = proc.REG(3)
proc.RDY2 = proc.REG(4)
proc.two_points_sum()
print (proc.ROX, proc.ROY)

