#Арифметико-логические устройства РЕГИСТР 16-бит
class rproc01():
    def __init__(self):
#инициализация регистров
        self.reg_data1 = self.REG(0)
        self.reg_data2 = self.REG(0)
        self.reg_com = self.REG(0)
        self.reg_out = self.REG(0)

#функция для записи десятичных чисел в регистр
    def REG(self, a):
        A = bin (a)
        Ab = A[2:len(A)]
        if len(Ab)<16:
            Ab = Ab.rjust(16,'0')
        if len(Ab)>16:
            Ab = Ab[(len(Ab)-16):len(Ab)]
        return Ab

#складываем два числа находящиеся в регистре и записываем результат в регистр
    def SUM(self):
        a = int(self.reg_data1,2)
        b = int(self.reg_data2,2)
        C = a + b
        self.reg_out = self.REG(C)

    def AND(self):
        c = str()
        for i in range (0,16):
           if self.reg_data1[i] == '1' and self.reg_data2[i] == '1':
               c += '1'
           else:
               c += '0'
        self.reg_out = c
        


        
proc = rproc01()
proc.reg_data1 = proc.REG(7)
proc.reg_data2 = proc.REG(2)
proc.AND()
print (proc.reg_data1)
print (proc.reg_data2)
print(proc.reg_out)


